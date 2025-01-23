"""
Utility script to generate wcps/spectral.py
"""
import requests
import os


def load_indices() -> dict[str, dict]:
    """
    Retrieves and parses the JSON from
    https://raw.githubusercontent.com/davemlz/awesome-ee-spectral-indices/main/output/spectral-indices-dict.json

    :return: a dict of index name -> dict with index details, e.g.

        .. code:: json

            {
              "AFRI1600": {
                "application_domain": "vegetation",
                "bands": ["N","S1"],
                "contributor": "https://github.com/davemlz",
                "date_of_addition": "2021-11-17",
                "formula": "(N - 0.66 * S1) / (N + 0.66 * S1)",
                "long_name": "Aerosol Free Vegetation Index (1600 nm)",
                "platforms": ["Sentinel-2","Landsat-OLI",
                    "Landsat-TM","Landsat-ETM+","MODIS"],
                "reference": "https://doi.org/10.1016/S0034-4257(01)00190-0",
                "short_name": "AFRI1600"
              },
              "NDVI": {
                "application_domain": "vegetation",
                "bands": ["N","R"],
                "contributor": "https://github.com/davemlz",
                "date_of_addition": "2021-04-07",
                "formula": "(N - R)/(N + R)",
                "long_name": "Normalized Difference Vegetation Index",
                "platforms": ["Sentinel-2","Landsat-OLI","Landsat-TM",
                    "Landsat-ETM+","MODIS","Planet-Fusion"],
                "reference": "https://ntrs.nasa.gov/citations/19740022614",
                "short_name": "NDVI"
              }
            }
    """
    url = "https://raw.githubusercontent.com/awesome-spectral-indices/awesome-spectral-indices/main/output/spectral-indices-dict.json"
    indices = requests.get(url).json()
    print(f"loaded indices from {url}")
    return indices['SpectralIndices']


def generate_spectral_py(indices, filename='spectral.py'):
    """
    Given a dict returned by :meth:`load_indices`, generate a Python files
    with classes for each index, e.g:

    .. code:: python

        class NDVI(WCPSExpr):
          short_name = "NDVI"
          long_name = "Normalized Difference Vegetation Index"
          bands = ['N', 'R']
          formula = "(N - R)/(N + R)"
          platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
          reference = "https://ntrs.nasa.gov/citations/19740022614"
          contributor = "https://github.com/davemlz"

          def __init__(self, N: OperandType, R: OperandType):
            super().__init__(operands=['N', 'R'])
            self.N = N
            self.R = R

          def __str__(self):
            return str(eval(self.formula, {}, {"N": self.N, "R": self.R}))

    :param indices: a dict of index name -> dict with index details
    :param filename: the Python filename in which the output will be saved
    """

    # get absolute filepath in the wcps dir
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.normpath(os.path.join(curr_dir, '..', 'wcps', filename))

    print(f"generating {filepath}")

    with open(filepath, 'w') as f:
        f.write('"""\n'
                'Python classes for spectral indices generated from a standardized list curated at\n'
                'https://awesome-ee-spectral-indices.readthedocs.io. Each class can be instantiated\n'
                'with :class:`wcps.model.OperandType` arguments for the respective bands / constants.\n'
                'Example for applying the NDVI index on red/nir Sentinel-2 bands:\n\n'
                '.. code:: python\n\n'
                '  from wcps.model import Datacube\n'
                '  from wcps.spectral import NDVI\n\n'
                '  red = Datacube("S2_L2A_32631_B04_10m")\n'
                '  nir = Datacube("S2_L2A_32631_B08_10m")\n'
                '  ndvi = NDVI(N=nir, R=red)\n'
                '  query = ndvi.encode("PNG")\n'
                '"""\n\n')
        f.write('# generated with bin/generate_spectral.py, do not edit manually.\n\n')

        f.write("from wcps.model import WCPSExpr, OperandType\n\n")

        for short_name, details in indices.items():
            class_name = short_name  # Using the key as the class name
            bands = details['bands']

            f.write(f'class {class_name}(WCPSExpr):\n')
            f.write(f'  """{details["long_name"]}"""\n')
            f.write(f'  short_name = "{details["short_name"]}"\n')
            f.write(f'  long_name = "{details["long_name"]}"\n')
            f.write(f'  bands = {details["bands"]}\n')
            f.write(f'  formula = "{details["formula"]}"\n')
            f.write(f'  platforms = {details["platforms"]}\n')
            f.write(f'  reference = "{details["reference"]}"\n')
            f.write(f'  contributor = "{details["contributor"]}"\n\n')

            band_params = ', '.join([band + ': OperandType' for band in bands])
            eval_params = ', '.join([f'"{band}": {band}' for band in bands])
            f.write(f'  def __init__(self, {band_params}):\n')
            f.write(f'    super().__init__(operands=[eval(self.formula, {{}}, {{{eval_params}}})])\n')
            for band in bands:
                f.write(f'    self.{band} = {band}\n')
            f.write('\n')

            f.write('  def __str__(self):\n')
            f.write('    return super().__str__() + str(self.operands[0])\n')
            f.write('\n\n')

    print(f"done generating {filepath}")

if __name__ == '__main__':
    generate_spectral_py(load_indices())
