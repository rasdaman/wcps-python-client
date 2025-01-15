# Overview

The [OGC Web Coverage Processing Service (WCPS) standard](https://www.ogc.org/standards/wcps)
defines a protocol-independent declarative query language for the extraction,
processing, and analysis of multi-dimensional coverages (datacubes) representing 
sensor, image, or statistics data.

This Python library allows to dynamically build WCPS queries and execute on a WCPS server.

# Installation

    pip install wcps

# Examples

Derive an [NDVI](https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index) 
map from red and near-infrared bands of a Sentinel-2 datacube, threshold the very
green areas (values greater than 0.5) as true values (white in a PNG), and save 
the result as a PNG image.

```python
from wcps.service import Service
from wcps.model import Datacube

# Let S2_L2A be a 3D coverage with nir and red bands;
# slice it at "2025-01-15" on the time axis, getting a 2D map
cov = Datacube("S2_L2A")["time", "2025-01-15"]
# NDVI formula
ndvi = (cov.nir - cov.red) / (cov.nir + cov.red)
# threshold NDVI values to highlight areas with high vegetation
vegetation = ndvi > 0.5
# encode final result to PNG
query = vegetation.encode("PNG")

service = Service("https://ows.rasdaman.org/rasdaman/ows")

# execute the query on the server and get back the response
response = service.execute(query)

# alternatively, save the content of the response into a file
response = service.execute(query,
                           output_file='vegetation.png')
```

We can calculate the average NDVI as follows:

```python
cov = ...
# NDVI formula
ndvi = (cov.nir - cov.red) / (cov.nir + cov.red)
# get average NDVI value
query = ndvi.avg()

service = ...
response = service.execute(query)

print(f'The average NDVI is {response.content}')
```

# Contributing

The directory structure is as follows:

- `wcps` - the main library code
- `tests` - testing code
- `docs` - documentation in reStructuredText format

## Tests

To run the tests execute:

```
pytest
```

## Documentation

To build the documentation:

```
# install needed dependencies
pip install wcps[docs]

cd docs
make html
```

The built documentation can be found in the `docs/_build/html/` subdir.
