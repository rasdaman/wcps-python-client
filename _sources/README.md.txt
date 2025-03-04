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
from wcps.model import Datacube

# Slice the time axis (with name ansi) at "2021-04-09",
# and trim on the spatial axes
cov = Datacube("S2_L2A_32631_TCI_60m")[
      "ansi" : "2021-04-09",
      "E" : 669960 : 700000,
      "N" : 4990200 : 5015220 ]

# encode final result to JPEG
query = cov.encode("JPEG")
```

The [Service](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/service/index.html#wcps.service.Service) 
class allows to [execute](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/service/index.html#wcps.service.Service.execute) 
the query on the server and get back a 
[WCPSResult](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/service/index.html#wcps.service.WCPSResult)
object. Optionally, array results can be automatically converted to a numpy array
by passing `convert_to_numpy=True` to the execute method.

```python
from wcps.service import Service

service = Service("https://ows.rasdaman.org/rasdaman/ows")

# if credentials are required:
# service = Service("https://ows.rasdaman.org/rasdaman/ows",
#                   username=..., password=...)

result = service.execute(query)
# or automatically convert the result to a numpy array
result = service.execute(query, convert_to_numpy=True)
```

Alternatively, the result can be saved into a file with the
[download](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/service/index.html#wcps.service.Service.download)
method

```python
service.download(query, output_file='tci.png')
```

or displayed with [show](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/service/index.html#wcps.service.Service.show),
mainly for demo purposes:

```python
service.show(query)
```

Note that calling this method requires the following dependencies:

- `pip install pillow` - for image results
- `pip install netCDF4` - for netcdf results


## Geometry Clipping

Non-rectangular subsetting by a geometry shape can be done with
[Clip](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/model/index.html#wcps.model.Clip).
It expects a WKT string describing the geometry.

Standard ``LineString``, ``Polygon``, ``MultiLineString`` and ``MultiPolygon``
geometries are supported, and libraries such as 
[shapely](https://shapely.readthedocs.io/en/stable/geometry.html)
or [geomet](https://pypi.org/project/geomet/) could be used to help
constructing such geometry strings.

More advanced geometries (non-standard WKT), are also supported in rasdaman,
in particular ``Curtain`` and ``Corridor``; see the
[rasdaman documentation](https://doc.rasdaman.org/05_geo-services-guide.html#polygon-raster-clipping)
for more details.

This example showcases clipping a polygon:

```python
from wcps.model import Datacube, Clip

polygon = """POLYGON(( 51.645 10.772, 51.018 12.551,
                       50.400 11.716, 50.584 10.051,
                       51.222 10.142, 51.551 10.522,
                       51.645 10.772 ))"""
clip = Clip(Datacube("Germany_DTM_4"), polygon)

color_map = ('{"colorMap":{"type":"intervals","colorTable":{'
             '"0":[0,0,255,0],"15":[0,140,0,255],'
             '"30":[0,180,0,255],"50":[255,193,0,255],'
             '"100":[255,154,0,255],"150":[255,116,0,255],'
             '"200":[255,77,0,255],"500":[255,0,0,255]}}}')

from wcps.service import Service
service = Service("https://ows.rasdaman.org/rasdaman/ows")
service.show(clip.encode("image/png").params(color_map))
```

In the next example we extract a trajectory over the Germany DEM.
The result of this WCPS query is a 1-D series of height values along
the specified LineString.

```python
from wcps.model import Datacube, Clip

line = """LineString( 52.8691 7.7124, 50.9861 6.8335,
                      49.5965 7.6904, 48.3562 9.0308, 
                      48.0634 11.9531, 51.0966 13.7988,
                      53.3440 13.5571, 53.8914 12.3926 )"""
clip = Clip(Datacube("Germany_DTM_4"), line)

from wcps.service import Service
service = Service("https://ows.rasdaman.org/rasdaman/ows")
result = service.execute(clip.encode("application/json"))

# visualize the result as a diagram; requires:
# pip install matplotlib
import matplotlib.pyplot as plt
plt.plot(result.value)
plt.title('Height along linestring')
plt.xlabel('Coordinate')
plt.ylabel('Height')
plt.show()
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

service = Service("https://ows.rasdaman.org/rasdaman/ows")
service.show(query)
```

Instead of explicitly writing the NDVI formula (`ndvi = (nir - red) / (nir + red)`),
we can use the
[NDVI](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/spectral/index.html#wcps.spectral.NDVI)
class from the 
[wcps.spectral](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/spectral/index.html)
module. The `wcps.spectral` module defines classes for over 200 spectral indices based on the standardized 
[Awesome Spectral Indices](https://github.com/davemlz/awesome-spectral-indices) list.
Given the required spectral bands, each class automatically applies the
formula to compute the respective index.

```python
from wcps.service import Service
from wcps.model import Datacube, Axis
from wcps.spectral import NDVI

subset = [Axis("ansi", "2021-04-09"),
          Axis("E", 670000, 680000),
          Axis("N", 4990220, 5000220)]

red = Datacube("S2_L2A_32631_B04_10m")[subset]
nir = Datacube("S2_L2A_32631_B08_10m")[subset]

# spectral index class automatically applies the formula 
ndvi = NDVI(N=nir, R=red)

vegetation = ndvi > 0.5
query = vegetation.encode("PNG")

service = Service("https://ows.rasdaman.org/rasdaman/ows")
service.show(query)
```

Alternatively we could also use the [spyndex](https://spyndex.readthedocs.io/) library
which supports the same indices list. Make sure to first install it with
`pip install spyndex pyarrow setuptools`, and then we can perform the NDVI computation with:

```python
import spyndex

ndvi = spyndex.computeIndex("NDVI", {"N": nir, "R": red})
```

## Composites

A [false-color](https://en.wikipedia.org/wiki/False_color) composite can 
be created by providing the corresponding bands in a 
[MultiBand](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/model/index.html#wcps.model.MultiBand)
object:

```python
from wcps.service import Service
from wcps.model import Datacube, MultiBand, rgb

# defined in previous example
subset = ...

green = Datacube("S2_L2A_32631_B03_10m")[subset]
red = Datacube("S2_L2A_32631_B04_10m")[subset]
nir = Datacube("S2_L2A_32631_B08_10m")[subset]

# false-color composite
false_color = MultiBand({"red": nir, "green": red, "blue": green})

# alternatively, use the rgb method shorthand:
false_color = rgb(nir, red, green)

# scale the cell values to fit in the 0-255 range suitable for PNG
scaled = false_color / 17.0

# execute the query on the server and show the result
service = Service("https://ows.rasdaman.org/rasdaman/ows")
service.show(scaled.encode("PNG"))
```

## Matching Resolution / Projection

What if the bands we want to combine come from coverages with different resolutions? We can 
[scale](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/model/index.html#wcps.model.Scale) 
the bands to a common resolution before the operations, e.g. below 
we combine B12 from a 20m coverage, and B8 / B3 from a higher resolution 10m coverage.

```python
from wcps.service import Service
from wcps.model import Datacube, rgb

# defined in previous example
subset = ...

green = Datacube("S2_L2A_32631_B03_10m")[subset]
swir = Datacube("S2_L2A_32631_B12_20m")[subset]
nir = Datacube("S2_L2A_32631_B08_10m")[subset]

# upscale swir to match the resolution of green;
# interpolation is fixed to nearest-neighbour
swir = swir.scale(another_coverage=green)

# false-color composite
composite = rgb(swir, nir, green)

# scale the cell values to fit in the 0-255 range suitable for PNG
scaled = composite / 17.0

# execute the query on the server and show the response
service = Service("https://ows.rasdaman.org/rasdaman/ows")
service.show(scaled.encode("PNG"))
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

Other aggregation functions include `sum()`, `max()`, `min()`, `all()`, `some()`,
``

## Timeseries Aggregation

A more advanced expression is the 
[general condenser](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/model/index.html#wcps.model.Condense) 
(aggregation) operation. The example calculates a map with maximum cell values across all time slices 
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
This can be done with a
[coverage constructor](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/model/index.html#wcps.model.Condense),
which will iterate over all dates 
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
result = service.execute(query)

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


## Convolution

The [coverage constructor](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/model/index.html#wcps.model.Condense)
supports also enumerating the cell values in place as a list of numbers.
This allows to specify small arrays such as
[convolution kernels](https://en.wikipedia.org/wiki/Kernel_(image_processing)),
enabling more advanced image processing operation. The example below uses a
[Sobel operator](https://en.wikipedia.org/wiki/Sobel_operator)
to perform edge detection on an image on the server, before downloading the result.

```python
from wcps.service import Service
from wcps.model import Datacube, Coverage, Condense, \
    AxisIter, CondenseOp

# kernels
x = AxisIter('$x', 'x').interval(-1, 1)
y = AxisIter('$y', 'y').interval(-1, 1)
kernel1 = (Coverage('kernel1').over([x, y])
           .value_list([1, 0, -1, 2, 0, -2, 1, 0, -1]))
kernel2 = (Coverage('kernel2').over([x, y])
           .value_list([1, 2, 1, 0, 0, 0, -1, -2, -1]))

# coverage axis iterators
cov = Datacube("NIR")
subset = [( "i", 10, 500 ), ( "j", 10, 500 )]
cx = AxisIter('$px', 'i').of_grid_axis(cov[subset])
cy = AxisIter('$py', 'j').of_grid_axis(cov[subset])

# kernel axis iterators
kx = AxisIter('$kx', 'x').interval(-1, 1)
ky = AxisIter('$ky', 'y').interval(-1, 1)

gx = (Coverage('Gx').over([cx, cy])
      .values(Condense(CondenseOp.PLUS).over([kx, ky])
              .using(kernel1["x": kx.ref(), "y": ky.ref()] *
                     cov.green["i": cx.ref() + kx.ref(),
                               "j": cy.ref() + ky.ref()])
              )
      ).pow(2.0)

gy = (Coverage('Gy').over([cx, cy])
      .values(Condense(CondenseOp.PLUS).over([kx, ky])
              .using(kernel2["x": kx.ref(), "y": ky.ref()] *
                     cov.green["i": cx.ref() + kx.ref(),
                               "j": cy.ref() + ky.ref()])
              )
      ).pow(2.0)

query = (gx + gy).sqrt().encode("image/jpeg")

service = Service("https://ows.rasdaman.org/rasdaman/ows")
service.download(query, 'convolution.png')
```

## Case Distinction

Conditional evaluation is possible with
[Switch](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/model/index.html#wcps.model.Switch):

```python
from wcps.service import Service
from wcps.model import Datacube, Switch, rgb

cov = Datacube("AvgLandTemp")["ansi": "2014-07",
                              "Lat": 35: 75,
                              "Long": -20: 40]
switch = (Switch()
          .case(cov == 99999).then(rgb(255, 255, 255))
          .case(cov < 18).then(rgb(0, 0, 255))
          .case(cov < 23).then(rgb(255, 255, 0))
          .case(cov < 30).then(rgb(255, 140, 0))
          .default(rgb(255, 0, 0)))

query = switch.encode("image/png")

service = Service("https://ows.rasdaman.org/rasdaman/ows")
service.show(query)
```

## User-Defined Functions (UDF)

UDFs can be executed with the 
[Udf](https://rasdaman.github.io/wcps-python-client/autoapi/wcps/model/index.html#wcps.model.Udf)
object:

```python
from wcps.service import Service
from wcps.model import Datacube, Udf

cov = Datacube("S2_L2A_32631_B04_10m")[
      "ansi" : "2021-04-09",
      "E" : 670000 : 680000,
      "N" : 4990220 : 5000220 ]

# Apply the image.stretch(cov) UDF to stretch the values of
# cov in the [0-255] range, so it can be encoded in JPEG
stretched = Udf('image.stretch', [cov]).encode("JPEG")

# execute the query on the server and show the result
service = Service("https://ows.rasdaman.org/rasdaman/ows")
service.show(stretched)
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
