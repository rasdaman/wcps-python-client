from model import MultiBand

# Overview

The [OGC Web Coverage Processing Service (WCPS) standard](https://www.ogc.org/standards/wcps)
defines a protocol-independent declarative query language for the extraction,
processing, and analysis of multi-dimensional coverages (datacubes) representing 
sensor, image, or statistics data.

This Python library allows to dynamically build WCPS queries and execute on a WCPS server.
To query a WCS server for information on available data, check the
[WCS Python Client](https://rasdaman.github.io/wcs-python-client/).

# Installation

    pip install wcps

# Examples

## Subsetting

Extracting spatio-temporal can be done with the subscripting operator `[]`, by specifying
lower and upper bounds for the axes we want to *trim*, or a single bound to
*slice* the axis at a particular index.

```python
from wcps.service import Service
from wcps.model import Datacube

# Slice the time axis (with name ansi) at "2021-04-09",
# and trim on the spatial axes
cov = Datacube("S2_L2A_32631_TCI_60m")[
      "ansi" : "2021-04-09",
      "E" : 669960 : 700000,
      "N" : 4990200 : 5015220 ]

# encode final result to JPEG
query = cov.encode("JPEG")

# execute the query on the server and get back a WCPSResult
service = Service("https://ows.rasdaman.org/rasdaman/ows")
result = service.execute(query)

# show the returned image; requires to install pillow:
# pip install pillow
from PIL import Image
from io import BytesIO
Image.open(BytesIO(result.value)).show()

# alternatively, save the content of the response into a file
service.download(query, output_file='vegetation.png')
```

## Band Math

Derive an [NDVI](https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index) 
map from red and near-infrared bands of a Sentinel-2 datacube, threshold the very
green areas (values greater than 0.5) as true values (white in a PNG), and save 
the result as a PNG image.

```python
from wcps.service import Service
from wcps.model import Datacube, Axis

subset = [Axis("ansi", "2021-04-09"),
          Axis("E", 670000, 680000),
          Axis("N", 4990220, 5000220)]

red = Datacube("S2_L2A_32631_B04_10m")[subset]
nir = Datacube("S2_L2A_32631_B08_10m")[subset]

# NDVI formula
ndvi = (nir - red) / (nir + red)
# threshold NDVI values to highlight areas with high vegetation
vegetation = ndvi > 0.5
# encode final result to PNG
query = vegetation.encode("PNG")

# execute the query on the server and get back the response
service = Service("https://ows.rasdaman.org/rasdaman/ows")
result = service.execute(query)

# show the returned image; requires to install pillow:
# pip install pillow
from PIL import Image
from io import BytesIO
Image.open(BytesIO(result.value)).show()

# similar to above, but automatically convert the PNG result 
# to a numpy array
result = service.execute(query, convert_to_numpy=True)
```

## Composites

A [false-color](https://en.wikipedia.org/wiki/False_color) composite can 
be created by providing the corresponding bands in a 
[MultiBand](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/model/index.html#wcps.model.MultiBand)
object:

```python
from wcps.service import Service
from wcps.model import Datacube, MultiBand

# defined in previous example
subset = ...

green = Datacube("S2_L2A_32631_B03_10m")[subset]
red = Datacube("S2_L2A_32631_B04_10m")[subset]
nir = Datacube("S2_L2A_32631_B08_10m")[subset]

# false-color composite
false_color = MultiBand({"red": nir, "green": red, "blue": green})

# scale the cell values to fit in the 0-255 range suitable for PNG
scaled = false_color / 17.0

# execute the query on the server and get back the response
service = Service("https://ows.rasdaman.org/rasdaman/ows")
result = service.execute(scaled.encode("PNG"))

# show the returned image; requires to install pillow:
# pip install pillow
from PIL import Image
from io import BytesIO
Image.open(BytesIO(result.value)).show()
```

## Matching Resolution / Projection

What if the bands we want to combine come from coverages with different resolutions? We can 
[scale](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/model/index.html#wcps.model.Scale) 
the bands to a common resolution before the operations, e.g. below 
we combine B12 from a 20m coverage, and B8 / B3 from a higher resolution 10m coverage.

```python
from wcps.service import Service
from wcps.model import Datacube, MultiBand

# defined in previous example
subset = ...

green = Datacube("S2_L2A_32631_B03_10m")[subset]
swir = Datacube("S2_L2A_32631_B12_20m")[subset]
nir = Datacube("S2_L2A_32631_B08_10m")[subset]

# upscale swir to match the resolution of green
swir = swir.scale(another_coverage=green)

# false-color composite
composite = MultiBand({"red": swir, "green": nir, "blue": green})

# scale the cell values to fit in the 0-255 range suitable for PNG
scaled = composite / 17.0

# execute the query on the server and get back the response
service = Service("https://ows.rasdaman.org/rasdaman/ows")
result = service.execute(scaled.encode("PNG"))

# show the returned image; requires to install pillow:
# pip install pillow
from PIL import Image
from io import BytesIO
Image.open(BytesIO(result.value)).show()
```

Matching different CRS projections can be done by 
[reprojecting](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/model/index.html#wcps.model.WCPSExpr.reproject)
the operands to a common target CRS.

## Basic Aggregation

We can calculate the average NDVI as follows:

```python
nir = ...
red = ...
# NDVI formula
ndvi = (nir - red) / (nir + red)
# get average NDVI value
query = ndvi.avg()

service = ...
result = service.execute(query)
print(f'The average NDVI is {result.value}')
```

Other reduce methods include `sum()`, `max()`, `min()`, `all()`, `some()`.

## Timeseries Aggregation

A more advanced expression is the *general condenser* (aggregation)
operation. The example calculates a map with maximum cell values across all time slices 
from a 3D datacube between "2015-01-01" and "2015-07-01", considering only the
time slices with an average greater than 20:

```python
from wcps.model import Datacube, AxisIter, Condense, CondenseOp
from wcps.service import Service

cov = Datacube("AvgTemperatureColorScaled")

# iterator named ansi_iter over the subset of a temporal axis ansi
ansi_iter = AxisIter("ansi_iter", "ansi") \
            .of_geo_axis(cov["ansi" : "2015-01-01" : "2015-07-01"])

max_map = (Condense(CondenseOp.MAX)
           .over( ansi_iter )
           .where( cov["ansi": ansi_iter.ref()].avg() > 20 )
           .using( cov["ansi": ansi_iter.ref()] ))

query = max_map.encode("PNG")

service = Service("https://ows.rasdaman.org/rasdaman/ows")
service.download(query, 'max_map.png')
```

How about calculating the average of each time slice between two dates? 
This can be done with a *coverage constructor*, which will iterate over all dates 
between the two given dates, resulting in a 1D array of average NDVI values;
notice that the slicing on the time axis ansi is done with the "iterator" variable `ansi_iter`
like in the previous example. The 1D array is encoded as JSON in the end.

```python
from wcps.model import Datacube, AxisIter, Coverage
from wcps.service import Service

# same as in the previous example
cov = Datacube("AvgTemperatureColorScaled")
ansi_iter = AxisIter("ansi_iter", "ansi") \
            .of_geo_axis(cov["ansi" : "2015-01-01" : "2015-07-01"])
ansi_iter_ref = ansi_iter.ref()

# compute averages per time slice
averages = Coverage("average_per_date") \
           .over( ansi_iter ) \
           .values( cov["ansi": ansi_iter_ref].Red.avg() )

query = averages.encode("JSON")

service = Service("https://ows.rasdaman.org/rasdaman/ows")
result = service.execute(query, query)

# print result
print(result.value)

# visualize the result as a diagram; requires:
# pip install matplotlib
import matplotlib.pyplot as plt
plt.plot(result.value, marker='o')
plt.title('Average per Date')
plt.xlabel('Date Index')
plt.ylabel('Average')
plt.show()
```

The returned JSON list contains only the average values, and not the
datetimes to which these correspond. As a result, the "Date Index" on the
X axis are just numbers from 0 to 6.

To get the date values, we can use the 
[WCS Python Client](https://rasdaman.github.io/wcs-python-client/).
Make sure to install it first with `pip install wcs`.

```python
from wcs.service import WebCoverageService

# get a coverage object that can be inspected for information
endpoint = "https://ows.rasdaman.org/rasdaman/ows"
wcs_service = WebCoverageService(endpoint)
cov = wcs_service.list_full_info('AvgTemperatureColorScaled')

# ansi is an irregular axis in this coverage, and we can get the
# coefficients within the subset above with the [] operator
subset_dates = cov.bbox.ansi["2015-01-01" : "2015-07-01"]

# visualize the result as a diagram
import matplotlib.pyplot as plt

plt.plot(subset_dates, result.value)
plt.title('Average per Date')
plt.xlabel('Date')
plt.ylabel('Average')
plt.show()
```


# Contributing

The directory structure is as follows:

- `wcps` - the main library code
- `tests` - testing code
- `docs` - documentation in reStructuredText format

## Tests

To run the tests:

```
# install dependencies
pip install wcps[tests]

pytest
```

## Documentation

To build the documentation:

```
# install dependencies
pip install wcps[docs]

cd docs
make html
```

The built documentation can be found in the `docs/_build/html/` subdir.

# Acknowledgments

Created in project [EU FAIRiCUBE](https://fairicube.nilu.no/), with funding from the 
Horizon Europe programme under grant agreement No 101059238.
