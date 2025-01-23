"""
Python classes for spectral indices generated from a standardized list curated at
https://awesome-ee-spectral-indices.readthedocs.io. Each class can be instantiated
with :class:`wcps.model.WCPSExpr` arguments for the respective bands / constants.
Example for applying the NDVI index on red/nir Sentinel-2 bands:

.. code:: python

  from wcps.model import Datacube
  from wcps.spectral import NDVI

  red = Datacube("S2_L2A_32631_B04_10m")
  nir = Datacube("S2_L2A_32631_B08_10m")
  ndvi = NDVI(N=nir, R=red)
  query = ndvi.encode("PNG")
"""

# generated with bin/generate_spectral.py, do not edit manually.

from wcps.model import WCPSExpr, OperandType

class AFRI1600(WCPSExpr):
  """Aerosol Free Vegetation Index (1600 nm)"""
  short_name = "AFRI1600"
  long_name = "Aerosol Free Vegetation Index (1600 nm)"
  bands = ['N', 'S1']
  formula = "(N - 0.66 * S1) / (N + 0.66 * S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/S0034-4257(01)00190-0"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S1": S1})])
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class AFRI2100(WCPSExpr):
  """Aerosol Free Vegetation Index (2100 nm)"""
  short_name = "AFRI2100"
  long_name = "Aerosol Free Vegetation Index (2100 nm)"
  bands = ['N', 'S2']
  formula = "(N - 0.5 * S2) / (N + 0.5 * S2)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/S0034-4257(01)00190-0"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S2": S2})])
    self.N = N
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class ANDWI(WCPSExpr):
  """Augmented Normalized Difference Water Index"""
  short_name = "ANDWI"
  long_name = "Augmented Normalized Difference Water Index"
  bands = ['B', 'G', 'R', 'N', 'S1', 'S2']
  formula = "(B + G + R - N - S1 - S2)/(B + G + R + N + S1 + S2)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.envsoft.2021.105030"
  contributor = "https://github.com/davemlz"

  def __init__(self, B: OperandType, G: OperandType, R: OperandType, N: OperandType, S1: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"B": B, "G": G, "R": R, "N": N, "S1": S1, "S2": S2})])
    self.B = B
    self.G = G
    self.R = R
    self.N = N
    self.S1 = S1
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class ARI(WCPSExpr):
  """Anthocyanin Reflectance Index"""
  short_name = "ARI"
  long_name = "Anthocyanin Reflectance Index"
  bands = ['G', 'RE1']
  formula = "(1 / G) - (1 / RE1)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1562/0031-8655(2001)074%3C0038:OPANEO%3E2.0.CO;2"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "RE1": RE1})])
    self.G = G
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class ARI2(WCPSExpr):
  """Anthocyanin Reflectance Index 2"""
  short_name = "ARI2"
  long_name = "Anthocyanin Reflectance Index 2"
  bands = ['N', 'G', 'RE1']
  formula = "N * ((1 / G) - (1 / RE1))"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1562/0031-8655(2001)074%3C0038:OPANEO%3E2.0.CO;2"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G, "RE1": RE1})])
    self.N = N
    self.G = G
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class ARVI(WCPSExpr):
  """Atmospherically Resistant Vegetation Index"""
  short_name = "ARVI"
  long_name = "Atmospherically Resistant Vegetation Index"
  bands = ['N', 'R', 'gamma', 'B']
  formula = "(N - (R - gamma * (R - B))) / (N + (R - gamma * (R - B)))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1109/36.134076"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, gamma: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "gamma": gamma, "B": B})])
    self.N = N
    self.R = R
    self.gamma = gamma
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class ATSAVI(WCPSExpr):
  """Adjusted Transformed Soil-Adjusted Vegetation Index"""
  short_name = "ATSAVI"
  long_name = "Adjusted Transformed Soil-Adjusted Vegetation Index"
  bands = ['sla', 'N', 'R', 'slb']
  formula = "sla * (N - sla * R - slb) / (sla * N + R - sla * slb + 0.08 * (1 + sla ** 2.0))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/0034-4257(91)90009-U"
  contributor = "https://github.com/davemlz"

  def __init__(self, sla: OperandType, N: OperandType, R: OperandType, slb: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"sla": sla, "N": N, "R": R, "slb": slb})])
    self.sla = sla
    self.N = N
    self.R = R
    self.slb = slb

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class AVI(WCPSExpr):
  """Advanced Vegetation Index"""
  short_name = "AVI"
  long_name = "Advanced Vegetation Index"
  bands = ['N', 'R']
  formula = "(N * (1.0 - R) * (N - R)) ** (1/3)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.465.8749&rep=rep1&type=pdf"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class AWEInsh(WCPSExpr):
  """Automated Water Extraction Index"""
  short_name = "AWEInsh"
  long_name = "Automated Water Extraction Index"
  bands = ['G', 'S1', 'N', 'S2']
  formula = "4.0 * (G - S1) - 0.25 * N + 2.75 * S2"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.rse.2013.08.029"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, S1: OperandType, N: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "S1": S1, "N": N, "S2": S2})])
    self.G = G
    self.S1 = S1
    self.N = N
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class AWEIsh(WCPSExpr):
  """Automated Water Extraction Index with Shadows Elimination"""
  short_name = "AWEIsh"
  long_name = "Automated Water Extraction Index with Shadows Elimination"
  bands = ['B', 'G', 'N', 'S1', 'S2']
  formula = "B + 2.5 * G - 1.5 * (N + S1) - 0.25 * S2"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.rse.2013.08.029"
  contributor = "https://github.com/davemlz"

  def __init__(self, B: OperandType, G: OperandType, N: OperandType, S1: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"B": B, "G": G, "N": N, "S1": S1, "S2": S2})])
    self.B = B
    self.G = G
    self.N = N
    self.S1 = S1
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class BAI(WCPSExpr):
  """Burned Area Index"""
  short_name = "BAI"
  long_name = "Burned Area Index"
  bands = ['R', 'N']
  formula = "1.0 / ((0.1 - R) ** 2.0 + (0.06 - N) ** 2.0)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://digital.csic.es/bitstream/10261/6426/1/Martin_Isabel_Serie_Geografica.pdf"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "N": N})])
    self.R = R
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class BAIM(WCPSExpr):
  """Burned Area Index adapted to MODIS"""
  short_name = "BAIM"
  long_name = "Burned Area Index adapted to MODIS"
  bands = ['N', 'S2']
  formula = "1.0/((0.05 - N) ** 2.0) + ((0.2 - S2) ** 2.0)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.foreco.2006.08.248"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S2": S2})])
    self.N = N
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class BAIS2(WCPSExpr):
  """Burned Area Index for Sentinel 2"""
  short_name = "BAIS2"
  long_name = "Burned Area Index for Sentinel 2"
  bands = ['RE2', 'RE3', 'N2', 'R', 'S2']
  formula = "(1.0 - ((RE2 * RE3 * N2) / R) ** 0.5) * (((S2 - N2)/(S2 + N2) ** 0.5) + 1.0)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.3390/ecrs-2-05177"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, RE3: OperandType, N2: OperandType, R: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "RE3": RE3, "N2": N2, "R": R, "S2": S2})])
    self.RE2 = RE2
    self.RE3 = RE3
    self.N2 = N2
    self.R = R
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class BCC(WCPSExpr):
  """Blue Chromatic Coordinate"""
  short_name = "BCC"
  long_name = "Blue Chromatic Coordinate"
  bands = ['B', 'R', 'G']
  formula = "B / (R + G + B)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/0034-4257(87)90088-5"
  contributor = "https://github.com/davemlz"

  def __init__(self, B: OperandType, R: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"B": B, "R": R, "G": G})])
    self.B = B
    self.R = R
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class BI(WCPSExpr):
  """Bare Soil Index"""
  short_name = "BI"
  long_name = "Bare Soil Index"
  bands = ['S1', 'R', 'N', 'B']
  formula = "((S1 + R) - (N + B))/((S1 + R) + (N + B))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.465.8749&rep=rep1&type=pdf"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, R: OperandType, N: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "R": R, "N": N, "B": B})])
    self.S1 = S1
    self.R = R
    self.N = N
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class BITM(WCPSExpr):
  """Landsat TM-based Brightness Index"""
  short_name = "BITM"
  long_name = "Landsat TM-based Brightness Index"
  bands = ['B', 'G', 'R']
  formula = "(((B**2.0)+(G**2.0)+(R**2.0))/3.0)**0.5"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/S0034-4257(98)00030-3"
  contributor = "https://github.com/davemlz"

  def __init__(self, B: OperandType, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"B": B, "G": G, "R": R})])
    self.B = B
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class BIXS(WCPSExpr):
  """SPOT HRV XS-based Brightness Index"""
  short_name = "BIXS"
  long_name = "SPOT HRV XS-based Brightness Index"
  bands = ['G', 'R']
  formula = "(((G**2.0)+(R**2.0))/2.0)**0.5"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/S0034-4257(98)00030-3"
  contributor = "https://github.com/remi-braun"

  def __init__(self, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R})])
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class BLFEI(WCPSExpr):
  """Built-Up Land Features Extraction Index"""
  short_name = "BLFEI"
  long_name = "Built-Up Land Features Extraction Index"
  bands = ['G', 'R', 'S2', 'S1']
  formula = "(((G+R+S2)/3.0)-S1)/(((G+R+S2)/3.0)+S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1080/10106049.2018.1497094"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, R: OperandType, S2: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R, "S2": S2, "S1": S1})])
    self.G = G
    self.R = R
    self.S2 = S2
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class BNDVI(WCPSExpr):
  """Blue Normalized Difference Vegetation Index"""
  short_name = "BNDVI"
  long_name = "Blue Normalized Difference Vegetation Index"
  bands = ['N', 'B']
  formula = "(N - B)/(N + B)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/S1672-6308(07)60027-4"
  contributor = "https://github.com/MATRIX4284"

  def __init__(self, N: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "B": B})])
    self.N = N
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class BRBA(WCPSExpr):
  """Band Ratio for Built-up Area"""
  short_name = "BRBA"
  long_name = "Band Ratio for Built-up Area"
  bands = ['R', 'S1']
  formula = "R/S1"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://www.omicsonline.org/scientific-reports/JGRS-SR136.pdf"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "S1": S1})])
    self.R = R
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class BWDRVI(WCPSExpr):
  """Blue Wide Dynamic Range Vegetation Index"""
  short_name = "BWDRVI"
  long_name = "Blue Wide Dynamic Range Vegetation Index"
  bands = ['alpha', 'N', 'B']
  formula = "(alpha * N - B) / (alpha * N + B)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.2135/cropsci2007.01.0031"
  contributor = "https://github.com/davemlz"

  def __init__(self, alpha: OperandType, N: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"alpha": alpha, "N": N, "B": B})])
    self.alpha = alpha
    self.N = N
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class BaI(WCPSExpr):
  """Bareness Index"""
  short_name = "BaI"
  long_name = "Bareness Index"
  bands = ['R', 'S1', 'N']
  formula = "R + S1 - N"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1109/IGARSS.2005.1525743"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, S1: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "S1": S1, "N": N})])
    self.R = R
    self.S1 = S1
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class CCI(WCPSExpr):
  """Chlorophyll Carotenoid Index"""
  short_name = "CCI"
  long_name = "Chlorophyll Carotenoid Index"
  bands = ['G1', 'R']
  formula = "(G1 - R)/(G1 + R)"
  platforms = ['MODIS']
  reference = "https://doi.org/10.1073/pnas.1606162113"
  contributor = "https://github.com/joanvlasschaert"

  def __init__(self, G1: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G1": G1, "R": R})])
    self.G1 = G1
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class CIG(WCPSExpr):
  """Chlorophyll Index Green"""
  short_name = "CIG"
  long_name = "Chlorophyll Index Green"
  bands = ['N', 'G']
  formula = "(N / G) - 1.0"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1078/0176-1617-00887"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G})])
    self.N = N
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class CIRE(WCPSExpr):
  """Chlorophyll Index Red Edge"""
  short_name = "CIRE"
  long_name = "Chlorophyll Index Red Edge"
  bands = ['N', 'RE1']
  formula = "(N / RE1) - 1"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1078/0176-1617-00887"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "RE1": RE1})])
    self.N = N
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class CRI550(WCPSExpr):
  """Carotenoid Reflectance Index using 550 nm"""
  short_name = "CRI550"
  long_name = "Carotenoid Reflectance Index using 550 nm"
  bands = ['B', 'G']
  formula = "(1.0 / B) - (1.0 / G)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1562/0031-8655(2002)0750272ACCIPL2.0.CO2"
  contributor = "https://github.com/eomasters-repos"

  def __init__(self, B: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"B": B, "G": G})])
    self.B = B
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class CRI700(WCPSExpr):
  """Carotenoid Reflectance Index using 700 nm"""
  short_name = "CRI700"
  long_name = "Carotenoid Reflectance Index using 700 nm"
  bands = ['B', 'RE1']
  formula = "(1.0 / B) - (1.0 / RE1)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1562/0031-8655(2002)0750272ACCIPL2.0.CO2"
  contributor = "https://github.com/eomasters-repos"

  def __init__(self, B: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"B": B, "RE1": RE1})])
    self.B = B
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class CSI(WCPSExpr):
  """Char Soil Index"""
  short_name = "CSI"
  long_name = "Char Soil Index"
  bands = ['N', 'S2']
  formula = "N/S2"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.rse.2005.04.014"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S2": S2})])
    self.N = N
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class CSIT(WCPSExpr):
  """Char Soil Index Thermal"""
  short_name = "CSIT"
  long_name = "Char Soil Index Thermal"
  bands = ['N', 'S2', 'T']
  formula = "N / (S2 * T / 10000.0)"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.1080/01431160600954704"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S2: OperandType, T: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S2": S2, "T": T})])
    self.N = N
    self.S2 = S2
    self.T = T

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class CVI(WCPSExpr):
  """Chlorophyll Vegetation Index"""
  short_name = "CVI"
  long_name = "Chlorophyll Vegetation Index"
  bands = ['N', 'R', 'G']
  formula = "(N * R) / (G ** 2.0)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1007/s11119-010-9204-3"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "G": G})])
    self.N = N
    self.R = R
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class DBI(WCPSExpr):
  """Dry Built-Up Index"""
  short_name = "DBI"
  long_name = "Dry Built-Up Index"
  bands = ['B', 'T1', 'N', 'R']
  formula = "((B - T1)/(B + T1)) - ((N - R)/(N + R))"
  platforms = ['Landsat-OLI']
  reference = "https://doi.org/10.3390/land7030081"
  contributor = "https://github.com/davemlz"

  def __init__(self, B: OperandType, T1: OperandType, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"B": B, "T1": T1, "N": N, "R": R})])
    self.B = B
    self.T1 = T1
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class DBSI(WCPSExpr):
  """Dry Bareness Index"""
  short_name = "DBSI"
  long_name = "Dry Bareness Index"
  bands = ['S1', 'G', 'N', 'R']
  formula = "((S1 - G)/(S1 + G)) - ((N - R)/(N + R))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3390/land7030081"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, G: OperandType, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "G": G, "N": N, "R": R})])
    self.S1 = S1
    self.G = G
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class DPDD(WCPSExpr):
  """Dual-Pol Diagonal Distance"""
  short_name = "DPDD"
  long_name = "Dual-Pol Diagonal Distance"
  bands = ['VV', 'VH']
  formula = "(VV + VH)/2.0 ** 0.5"
  platforms = ['Sentinel-1 (Dual Polarisation VV-VH)']
  reference = "https://doi.org/10.1016/j.rse.2018.09.003"
  contributor = "https://github.com/davemlz"

  def __init__(self, VV: OperandType, VH: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"VV": VV, "VH": VH})])
    self.VV = VV
    self.VH = VH

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class DSI(WCPSExpr):
  """Drought Stress Index"""
  short_name = "DSI"
  long_name = "Drought Stress Index"
  bands = ['S1', 'N']
  formula = "S1/N"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://www.asprs.org/wp-content/uploads/pers/1999journal/apr/1999_apr_495-501.pdf"
  contributor = "https://github.com/remi-braun"

  def __init__(self, S1: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "N": N})])
    self.S1 = S1
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class DSWI1(WCPSExpr):
  """Disease-Water Stress Index 1"""
  short_name = "DSWI1"
  long_name = "Disease-Water Stress Index 1"
  bands = ['N', 'S1']
  formula = "N/S1"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1080/01431160310001618031"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S1": S1})])
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class DSWI2(WCPSExpr):
  """Disease-Water Stress Index 2"""
  short_name = "DSWI2"
  long_name = "Disease-Water Stress Index 2"
  bands = ['S1', 'G']
  formula = "S1/G"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1080/01431160310001618031"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "G": G})])
    self.S1 = S1
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class DSWI3(WCPSExpr):
  """Disease-Water Stress Index 3"""
  short_name = "DSWI3"
  long_name = "Disease-Water Stress Index 3"
  bands = ['S1', 'R']
  formula = "S1/R"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1080/01431160310001618031"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "R": R})])
    self.S1 = S1
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class DSWI4(WCPSExpr):
  """Disease-Water Stress Index 4"""
  short_name = "DSWI4"
  long_name = "Disease-Water Stress Index 4"
  bands = ['G', 'R']
  formula = "G/R"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1080/01431160310001618031"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R})])
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class DSWI5(WCPSExpr):
  """Disease-Water Stress Index 5"""
  short_name = "DSWI5"
  long_name = "Disease-Water Stress Index 5"
  bands = ['N', 'G', 'S1', 'R']
  formula = "(N + G)/(S1 + R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1080/01431160310001618031"
  contributor = "https://github.com/remi-braun"

  def __init__(self, N: OperandType, G: OperandType, S1: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G, "S1": S1, "R": R})])
    self.N = N
    self.G = G
    self.S1 = S1
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class DVI(WCPSExpr):
  """Difference Vegetation Index"""
  short_name = "DVI"
  long_name = "Difference Vegetation Index"
  bands = ['N', 'R']
  formula = "N - R"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/0034-4257(94)00114-3"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class DVIplus(WCPSExpr):
  """Difference Vegetation Index Plus"""
  short_name = "DVIplus"
  long_name = "Difference Vegetation Index Plus"
  bands = ['lambdaN', 'lambdaR', 'lambdaG', 'G', 'N', 'R']
  formula = "((lambdaN - lambdaR)/(lambdaN - lambdaG)) * G + (1.0 - ((lambdaN - lambdaR)/(lambdaN - lambdaG))) * N - R"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.rse.2019.03.028"
  contributor = "https://github.com/davemlz"

  def __init__(self, lambdaN: OperandType, lambdaR: OperandType, lambdaG: OperandType, G: OperandType, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"lambdaN": lambdaN, "lambdaR": lambdaR, "lambdaG": lambdaG, "G": G, "N": N, "R": R})])
    self.lambdaN = lambdaN
    self.lambdaR = lambdaR
    self.lambdaG = lambdaG
    self.G = G
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class DpRVIHH(WCPSExpr):
  """Dual-Polarized Radar Vegetation Index HH"""
  short_name = "DpRVIHH"
  long_name = "Dual-Polarized Radar Vegetation Index HH"
  bands = ['HV', 'HH']
  formula = "(4.0 * HV)/(HH + HV)"
  platforms = ['Sentinel-1 (Dual Polarisation HH-HV)']
  reference = "https://www.tandfonline.com/doi/abs/10.5589/m12-043"
  contributor = "https://github.com/davemlz"

  def __init__(self, HV: OperandType, HH: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"HV": HV, "HH": HH})])
    self.HV = HV
    self.HH = HH

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class DpRVIVV(WCPSExpr):
  """Dual-Polarized Radar Vegetation Index VV"""
  short_name = "DpRVIVV"
  long_name = "Dual-Polarized Radar Vegetation Index VV"
  bands = ['VH', 'VV']
  formula = "(4.0 * VH)/(VV + VH)"
  platforms = ['Sentinel-1 (Dual Polarisation VV-VH)']
  reference = "https://doi.org/10.3390/app9040655"
  contributor = "https://github.com/davemlz"

  def __init__(self, VH: OperandType, VV: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"VH": VH, "VV": VV})])
    self.VH = VH
    self.VV = VV

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class EBBI(WCPSExpr):
  """Enhanced Built-Up and Bareness Index"""
  short_name = "EBBI"
  long_name = "Enhanced Built-Up and Bareness Index"
  bands = ['S1', 'N', 'T']
  formula = "(S1 - N) / (10.0 * ((S1 + T) ** 0.5))"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.3390/rs4102957"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, N: OperandType, T: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "N": N, "T": T})])
    self.S1 = S1
    self.N = N
    self.T = T

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class EBI(WCPSExpr):
  """Enhanced Bloom Index"""
  short_name = "EBI"
  long_name = "Enhanced Bloom Index"
  bands = ['R', 'G', 'B', 'epsilon']
  formula = "(R + G + B)/((G/B) * (R - B + epsilon))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.isprsjprs.2019.08.006"
  contributor = "https://github.com/geoSanjeeb"

  def __init__(self, R: OperandType, G: OperandType, B: OperandType, epsilon: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "G": G, "B": B, "epsilon": epsilon})])
    self.R = R
    self.G = G
    self.B = B
    self.epsilon = epsilon

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class EMBI(WCPSExpr):
  """Enhanced Modified Bare Soil Index"""
  short_name = "EMBI"
  long_name = "Enhanced Modified Bare Soil Index"
  bands = ['S1', 'S2', 'N', 'G']
  formula = "((((S1 - S2 - N)/(S1 + S2 + N)) + 0.5) - ((G - S1)/(G + S1)) - 0.5)/((((S1 - S2 - N)/(S1 + S2 + N)) + 0.5) + ((G - S1)/(G + S1)) + 1.5)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.jag.2022.102703"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, S2: OperandType, N: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "S2": S2, "N": N, "G": G})])
    self.S1 = S1
    self.S2 = S2
    self.N = N
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class ENDVI(WCPSExpr):
  """Enhanced Normalized Difference Vegetation Index"""
  short_name = "ENDVI"
  long_name = "Enhanced Normalized Difference Vegetation Index"
  bands = ['N', 'G', 'B']
  formula = "((N + G) - (2 * B)) / ((N + G) + (2 * B))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1371/journal.pone.0186193"
  contributor = "https://github.com/gagev"

  def __init__(self, N: OperandType, G: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G, "B": B})])
    self.N = N
    self.G = G
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class EVI(WCPSExpr):
  """Enhanced Vegetation Index"""
  short_name = "EVI"
  long_name = "Enhanced Vegetation Index"
  bands = ['g', 'N', 'R', 'C1', 'C2', 'B', 'L']
  formula = "g * (N - R) / (N + C1 * R - C2 * B + L)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/S0034-4257(96)00112-5"
  contributor = "https://github.com/davemlz"

  def __init__(self, g: OperandType, N: OperandType, R: OperandType, C1: OperandType, C2: OperandType, B: OperandType, L: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"g": g, "N": N, "R": R, "C1": C1, "C2": C2, "B": B, "L": L})])
    self.g = g
    self.N = N
    self.R = R
    self.C1 = C1
    self.C2 = C2
    self.B = B
    self.L = L

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class EVI2(WCPSExpr):
  """Two-Band Enhanced Vegetation Index"""
  short_name = "EVI2"
  long_name = "Two-Band Enhanced Vegetation Index"
  bands = ['g', 'N', 'R', 'L']
  formula = "g * (N - R) / (N + 2.4 * R + L)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.rse.2008.06.006"
  contributor = "https://github.com/davemlz"

  def __init__(self, g: OperandType, N: OperandType, R: OperandType, L: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"g": g, "N": N, "R": R, "L": L})])
    self.g = g
    self.N = N
    self.R = R
    self.L = L

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class EVIv(WCPSExpr):
  """Enhanced Vegetation Index of Vegetation"""
  short_name = "EVIv"
  long_name = "Enhanced Vegetation Index of Vegetation"
  bands = ['N', 'R', 'B']
  formula = "2.5 * ((N - R)/(N + 6 * R - 7.5 * B + 1.0)) * N"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1029/2024JG008240"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "B": B})])
    self.N = N
    self.R = R
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class ExG(WCPSExpr):
  """Excess Green Index"""
  short_name = "ExG"
  long_name = "Excess Green Index"
  bands = ['G', 'R', 'B']
  formula = "2 * G - R - B"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.13031/2013.27838"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, R: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R, "B": B})])
    self.G = G
    self.R = R
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class ExGR(WCPSExpr):
  """ExG - ExR Vegetation Index"""
  short_name = "ExGR"
  long_name = "ExG - ExR Vegetation Index"
  bands = ['G', 'R', 'B']
  formula = "(2.0 * G - R - B) - (1.3 * R - G)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.compag.2008.03.009"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, R: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R, "B": B})])
    self.G = G
    self.R = R
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class ExR(WCPSExpr):
  """Excess Red Index"""
  short_name = "ExR"
  long_name = "Excess Red Index"
  bands = ['R', 'G']
  formula = "1.3 * R - G"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1117/12.336896"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "G": G})])
    self.R = R
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class FAI(WCPSExpr):
  """Floating Algae Index"""
  short_name = "FAI"
  long_name = "Floating Algae Index"
  bands = ['N', 'R', 'S1', 'lambdaN', 'lambdaR', 'lambdaS1']
  formula = "N - (R + (S1 - R)*((lambdaN - lambdaR)/(lambdaS1 - lambdaR)))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.rse.2009.05.012"
  contributor = "https://github.com/emanuelcastanho"

  def __init__(self, N: OperandType, R: OperandType, S1: OperandType, lambdaN: OperandType, lambdaR: OperandType, lambdaS1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "S1": S1, "lambdaN": lambdaN, "lambdaR": lambdaR, "lambdaS1": lambdaS1})])
    self.N = N
    self.R = R
    self.S1 = S1
    self.lambdaN = lambdaN
    self.lambdaR = lambdaR
    self.lambdaS1 = lambdaS1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class FCVI(WCPSExpr):
  """Fluorescence Correction Vegetation Index"""
  short_name = "FCVI"
  long_name = "Fluorescence Correction Vegetation Index"
  bands = ['N', 'R', 'G', 'B']
  formula = "N - ((R + G + B)/3.0)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.rse.2020.111676"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, G: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "G": G, "B": B})])
    self.N = N
    self.R = R
    self.G = G
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GARI(WCPSExpr):
  """Green Atmospherically Resistant Vegetation Index"""
  short_name = "GARI"
  long_name = "Green Atmospherically Resistant Vegetation Index"
  bands = ['N', 'G', 'B', 'R']
  formula = "(N - (G - (B - R))) / (N - (G + (B - R)))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/S0034-4257(96)00072-7"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType, B: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G, "B": B, "R": R})])
    self.N = N
    self.G = G
    self.B = B
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GBNDVI(WCPSExpr):
  """Green-Blue Normalized Difference Vegetation Index"""
  short_name = "GBNDVI"
  long_name = "Green-Blue Normalized Difference Vegetation Index"
  bands = ['N', 'G', 'B']
  formula = "(N - (G + B))/(N + (G + B))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/S1672-6308(07)60027-4"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G, "B": B})])
    self.N = N
    self.G = G
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GCC(WCPSExpr):
  """Green Chromatic Coordinate"""
  short_name = "GCC"
  long_name = "Green Chromatic Coordinate"
  bands = ['G', 'R', 'B']
  formula = "G / (R + G + B)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/0034-4257(87)90088-5"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, R: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R, "B": B})])
    self.G = G
    self.R = R
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GDVI(WCPSExpr):
  """Generalized Difference Vegetation Index"""
  short_name = "GDVI"
  long_name = "Generalized Difference Vegetation Index"
  bands = ['N', 'nexp', 'R']
  formula = "((N ** nexp) - (R ** nexp)) / ((N ** nexp) + (R ** nexp))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.3390/rs6021211"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, nexp: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "nexp": nexp, "R": R})])
    self.N = N
    self.nexp = nexp
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GEMI(WCPSExpr):
  """Global Environment Monitoring Index"""
  short_name = "GEMI"
  long_name = "Global Environment Monitoring Index"
  bands = ['N', 'R']
  formula = "((2.0*((N ** 2.0)-(R ** 2.0)) + 1.5*N + 0.5*R)/(N + R + 0.5))*(1.0 - 0.25*((2.0 * ((N ** 2.0) - (R ** 2)) + 1.5 * N + 0.5 * R)/(N + R + 0.5)))-((R - 0.125)/(1 - R))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "http://dx.doi.org/10.1007/bf00031911"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GLI(WCPSExpr):
  """Green Leaf Index"""
  short_name = "GLI"
  long_name = "Green Leaf Index"
  bands = ['G', 'R', 'B']
  formula = "(2.0 * G - R - B) / (2.0 * G + R + B)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "http://dx.doi.org/10.1080/10106040108542184"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, R: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R, "B": B})])
    self.G = G
    self.R = R
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GM1(WCPSExpr):
  """Gitelson and Merzlyak Index 1"""
  short_name = "GM1"
  long_name = "Gitelson and Merzlyak Index 1"
  bands = ['RE2', 'G']
  formula = "RE2/G"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0176-1617(96)80284-7"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "G": G})])
    self.RE2 = RE2
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GM2(WCPSExpr):
  """Gitelson and Merzlyak Index 2"""
  short_name = "GM2"
  long_name = "Gitelson and Merzlyak Index 2"
  bands = ['RE2', 'RE1']
  formula = "RE2/RE1"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0176-1617(96)80284-7"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "RE1": RE1})])
    self.RE2 = RE2
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GNDVI(WCPSExpr):
  """Green Normalized Difference Vegetation Index"""
  short_name = "GNDVI"
  long_name = "Green Normalized Difference Vegetation Index"
  bands = ['N', 'G']
  formula = "(N - G)/(N + G)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/S0034-4257(96)00072-7"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G})])
    self.N = N
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GOSAVI(WCPSExpr):
  """Green Optimized Soil Adjusted Vegetation Index"""
  short_name = "GOSAVI"
  long_name = "Green Optimized Soil Adjusted Vegetation Index"
  bands = ['N', 'G']
  formula = "(N - G) / (N + G + 0.16)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.2134/agronj2004.0314"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G})])
    self.N = N
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GRNDVI(WCPSExpr):
  """Green-Red Normalized Difference Vegetation Index"""
  short_name = "GRNDVI"
  long_name = "Green-Red Normalized Difference Vegetation Index"
  bands = ['N', 'G', 'R']
  formula = "(N - (G + R))/(N + (G + R))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/S1672-6308(07)60027-4"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G, "R": R})])
    self.N = N
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GRVI(WCPSExpr):
  """Green Ratio Vegetation Index"""
  short_name = "GRVI"
  long_name = "Green Ratio Vegetation Index"
  bands = ['N', 'G']
  formula = "N/G"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.2134/agronj2004.0314"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G})])
    self.N = N
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GSAVI(WCPSExpr):
  """Green Soil Adjusted Vegetation Index"""
  short_name = "GSAVI"
  long_name = "Green Soil Adjusted Vegetation Index"
  bands = ['L', 'N', 'G']
  formula = "(1.0 + L) * (N - G) / (N + G + L)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.2134/agronj2004.0314"
  contributor = "https://github.com/davemlz"

  def __init__(self, L: OperandType, N: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"L": L, "N": N, "G": G})])
    self.L = L
    self.N = N
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class GVMI(WCPSExpr):
  """Global Vegetation Moisture Index"""
  short_name = "GVMI"
  long_name = "Global Vegetation Moisture Index"
  bands = ['N', 'S2']
  formula = "((N + 0.1) - (S2 + 0.02)) / ((N + 0.1) + (S2 + 0.02))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/S0034-4257(02)00037-8"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S2": S2})])
    self.N = N
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class IAVI(WCPSExpr):
  """New Atmospherically Resistant Vegetation Index"""
  short_name = "IAVI"
  long_name = "New Atmospherically Resistant Vegetation Index"
  bands = ['N', 'R', 'gamma', 'B']
  formula = "(N - (R - gamma * (B - R)))/(N + (R - gamma * (B - R)))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://www.jipb.net/EN/abstract/abstract23925.shtml"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, gamma: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "gamma": gamma, "B": B})])
    self.N = N
    self.R = R
    self.gamma = gamma
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class IBI(WCPSExpr):
  """Index-Based Built-Up Index"""
  short_name = "IBI"
  long_name = "Index-Based Built-Up Index"
  bands = ['S1', 'N', 'R', 'L', 'G']
  formula = "(((S1-N)/(S1+N))-(((N-R)*(1.0+L)/(N+R+L))+((G-S1)/(G+S1)))/2.0)/(((S1-N)/(S1+N))+(((N-R)*(1.0+L)/(N+R+L))+((G-S1)/(G+S1)))/2.0)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1080/01431160802039957"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, N: OperandType, R: OperandType, L: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "N": N, "R": R, "L": L, "G": G})])
    self.S1 = S1
    self.N = N
    self.R = R
    self.L = L
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class IKAW(WCPSExpr):
  """Kawashima Index"""
  short_name = "IKAW"
  long_name = "Kawashima Index"
  bands = ['R', 'B']
  formula = "(R - B)/(R + B)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1006/anbo.1997.0544"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "B": B})])
    self.R = R
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class IPVI(WCPSExpr):
  """Infrared Percentage Vegetation Index"""
  short_name = "IPVI"
  long_name = "Infrared Percentage Vegetation Index"
  bands = ['N', 'R']
  formula = "N/(N + R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/0034-4257(90)90085-Z"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class IRECI(WCPSExpr):
  """Inverted Red-Edge Chlorophyll Index"""
  short_name = "IRECI"
  long_name = "Inverted Red-Edge Chlorophyll Index"
  bands = ['RE3', 'R', 'RE1', 'RE2']
  formula = "(RE3 - R) / (RE1 / RE2)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/j.isprsjprs.2013.04.007"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE3: OperandType, R: OperandType, RE1: OperandType, RE2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE3": RE3, "R": R, "RE1": RE1, "RE2": RE2})])
    self.RE3 = RE3
    self.R = R
    self.RE1 = RE1
    self.RE2 = RE2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class LSWI(WCPSExpr):
  """Land Surface Water Index"""
  short_name = "LSWI"
  long_name = "Land Surface Water Index"
  bands = ['N', 'S1']
  formula = "(N - S1)/(N + S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.rse.2003.11.008"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S1": S1})])
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MBI(WCPSExpr):
  """Modified Bare Soil Index"""
  short_name = "MBI"
  long_name = "Modified Bare Soil Index"
  bands = ['S1', 'S2', 'N']
  formula = "((S1 - S2 - N)/(S1 + S2 + N)) + 0.5"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3390/land10030231"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, S2: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "S2": S2, "N": N})])
    self.S1 = S1
    self.S2 = S2
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MBWI(WCPSExpr):
  """Multi-Band Water Index"""
  short_name = "MBWI"
  long_name = "Multi-Band Water Index"
  bands = ['omega', 'G', 'R', 'N', 'S1', 'S2']
  formula = "(omega * G) - R - N - S1 - S2"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.jag.2018.01.018"
  contributor = "https://github.com/davemlz"

  def __init__(self, omega: OperandType, G: OperandType, R: OperandType, N: OperandType, S1: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"omega": omega, "G": G, "R": R, "N": N, "S1": S1, "S2": S2})])
    self.omega = omega
    self.G = G
    self.R = R
    self.N = N
    self.S1 = S1
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MCARI(WCPSExpr):
  """Modified Chlorophyll Absorption in Reflectance Index"""
  short_name = "MCARI"
  long_name = "Modified Chlorophyll Absorption in Reflectance Index"
  bands = ['RE1', 'R', 'G']
  formula = "((RE1 - R) - 0.2 * (RE1 - G)) * (RE1 / R)"
  platforms = ['Sentinel-2']
  reference = "http://dx.doi.org/10.1016/S0034-4257(00)00113-9"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE1: OperandType, R: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE1": RE1, "R": R, "G": G})])
    self.RE1 = RE1
    self.R = R
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MCARI1(WCPSExpr):
  """Modified Chlorophyll Absorption in Reflectance Index 1"""
  short_name = "MCARI1"
  long_name = "Modified Chlorophyll Absorption in Reflectance Index 1"
  bands = ['N', 'R', 'G']
  formula = "1.2 * (2.5 * (N - R) - 1.3 * (N - G))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.rse.2003.12.013"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "G": G})])
    self.N = N
    self.R = R
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MCARI2(WCPSExpr):
  """Modified Chlorophyll Absorption in Reflectance Index 2"""
  short_name = "MCARI2"
  long_name = "Modified Chlorophyll Absorption in Reflectance Index 2"
  bands = ['N', 'R', 'G']
  formula = "(1.5 * (2.5 * (N - R) - 1.3 * (N - G))) / ((((2.0 * N + 1) ** 2) - (6.0 * N - 5 * (R ** 0.5)) - 0.5) ** 0.5)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.rse.2003.12.013"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "G": G})])
    self.N = N
    self.R = R
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MCARI705(WCPSExpr):
  """Modified Chlorophyll Absorption in Reflectance Index (705 and 750 nm)"""
  short_name = "MCARI705"
  long_name = "Modified Chlorophyll Absorption in Reflectance Index (705 and 750 nm)"
  bands = ['RE2', 'RE1', 'G']
  formula = "((RE2 - RE1) - 0.2 * (RE2 - G)) * (RE2 / RE1)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/j.agrformet.2008.03.005"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, RE1: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "RE1": RE1, "G": G})])
    self.RE2 = RE2
    self.RE1 = RE1
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MCARIOSAVI(WCPSExpr):
  """MCARI/OSAVI Ratio"""
  short_name = "MCARIOSAVI"
  long_name = "MCARI/OSAVI Ratio"
  bands = ['RE1', 'R', 'G', 'N']
  formula = "(((RE1 - R) - 0.2 * (RE1 - G)) * (RE1 / R)) / (1.16 * (N - R) / (N + R + 0.16))"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0034-4257(00)00113-9"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE1: OperandType, R: OperandType, G: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE1": RE1, "R": R, "G": G, "N": N})])
    self.RE1 = RE1
    self.R = R
    self.G = G
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MCARIOSAVI705(WCPSExpr):
  """MCARI/OSAVI Ratio (705 and 750 nm)"""
  short_name = "MCARIOSAVI705"
  long_name = "MCARI/OSAVI Ratio (705 and 750 nm)"
  bands = ['RE2', 'RE1', 'G']
  formula = "(((RE2 - RE1) - 0.2 * (RE2 - G)) * (RE2 / RE1)) / (1.16 * (RE2 - RE1) / (RE2 + RE1 + 0.16))"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/j.agrformet.2008.03.005"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, RE1: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "RE1": RE1, "G": G})])
    self.RE2 = RE2
    self.RE1 = RE1
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MGRVI(WCPSExpr):
  """Modified Green Red Vegetation Index"""
  short_name = "MGRVI"
  long_name = "Modified Green Red Vegetation Index"
  bands = ['G', 'R']
  formula = "(G ** 2.0 - R ** 2.0) / (G ** 2.0 + R ** 2.0)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.jag.2015.02.012"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R})])
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MIRBI(WCPSExpr):
  """Mid-Infrared Burn Index"""
  short_name = "MIRBI"
  long_name = "Mid-Infrared Burn Index"
  bands = ['S2', 'S1']
  formula = "10.0 * S2 - 9.8 * S1 + 2.0"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1080/01431160110053185"
  contributor = "https://github.com/davemlz"

  def __init__(self, S2: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S2": S2, "S1": S1})])
    self.S2 = S2
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MLSWI26(WCPSExpr):
  """Modified Land Surface Water Index (MODIS Bands 2 and 6)"""
  short_name = "MLSWI26"
  long_name = "Modified Land Surface Water Index (MODIS Bands 2 and 6)"
  bands = ['N', 'S1']
  formula = "(1.0 - N - S1)/(1.0 - N + S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3390/rs71215805"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S1": S1})])
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MLSWI27(WCPSExpr):
  """Modified Land Surface Water Index (MODIS Bands 2 and 7)"""
  short_name = "MLSWI27"
  long_name = "Modified Land Surface Water Index (MODIS Bands 2 and 7)"
  bands = ['N', 'S2']
  formula = "(1.0 - N - S2)/(1.0 - N + S2)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3390/rs71215805"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S2": S2})])
    self.N = N
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MNDVI(WCPSExpr):
  """Modified Normalized Difference Vegetation Index"""
  short_name = "MNDVI"
  long_name = "Modified Normalized Difference Vegetation Index"
  bands = ['N', 'S2']
  formula = "(N - S2)/(N + S2)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1080/014311697216810"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S2": S2})])
    self.N = N
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MNDWI(WCPSExpr):
  """Modified Normalized Difference Water Index"""
  short_name = "MNDWI"
  long_name = "Modified Normalized Difference Water Index"
  bands = ['G', 'S1']
  formula = "(G - S1) / (G + S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1080/01431160600589179"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "S1": S1})])
    self.G = G
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MNLI(WCPSExpr):
  """Modified Non-Linear Vegetation Index"""
  short_name = "MNLI"
  long_name = "Modified Non-Linear Vegetation Index"
  bands = ['L', 'N', 'R']
  formula = "(1 + L)*((N ** 2) - R)/((N ** 2) + R + L)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1109/TGRS.2003.812910"
  contributor = "https://github.com/davemlz"

  def __init__(self, L: OperandType, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"L": L, "N": N, "R": R})])
    self.L = L
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MRBVI(WCPSExpr):
  """Modified Red Blue Vegetation Index"""
  short_name = "MRBVI"
  long_name = "Modified Red Blue Vegetation Index"
  bands = ['R', 'B']
  formula = "(R ** 2.0 - B ** 2.0)/(R ** 2.0 + B ** 2.0)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.3390/s20185055"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "B": B})])
    self.R = R
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MSAVI(WCPSExpr):
  """Modified Soil-Adjusted Vegetation Index"""
  short_name = "MSAVI"
  long_name = "Modified Soil-Adjusted Vegetation Index"
  bands = ['N', 'R']
  formula = "0.5 * (2.0 * N + 1 - (((2 * N + 1) ** 2) - 8 * (N - R)) ** 0.5)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/0034-4257(94)90134-1"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MSI(WCPSExpr):
  """Moisture Stress Index"""
  short_name = "MSI"
  long_name = "Moisture Stress Index"
  bands = ['S1', 'N']
  formula = "S1/N"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/0034-4257(89)90046-1"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "N": N})])
    self.S1 = S1
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MSR(WCPSExpr):
  """Modified Simple Ratio"""
  short_name = "MSR"
  long_name = "Modified Simple Ratio"
  bands = ['N', 'R']
  formula = "(N / R - 1) / ((N / R + 1) ** 0.5)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1080/07038992.1996.10855178"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MSR705(WCPSExpr):
  """Modified Simple Ratio (705 and 750 nm)"""
  short_name = "MSR705"
  long_name = "Modified Simple Ratio (705 and 750 nm)"
  bands = ['RE2', 'RE1']
  formula = "(RE2 / RE1 - 1) / ((RE2 / RE1 + 1) ** 0.5)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/j.agrformet.2008.03.005"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "RE1": RE1})])
    self.RE2 = RE2
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MTCI(WCPSExpr):
  """MERIS Terrestrial Chlorophyll Index"""
  short_name = "MTCI"
  long_name = "MERIS Terrestrial Chlorophyll Index"
  bands = ['RE2', 'RE1', 'R']
  formula = "(RE2 - RE1) / (RE1 - R)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1080/0143116042000274015"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, RE1: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "RE1": RE1, "R": R})])
    self.RE2 = RE2
    self.RE1 = RE1
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MTVI1(WCPSExpr):
  """Modified Triangular Vegetation Index 1"""
  short_name = "MTVI1"
  long_name = "Modified Triangular Vegetation Index 1"
  bands = ['N', 'G', 'R']
  formula = "1.2 * (1.2 * (N - G) - 2.5 * (R - G))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.rse.2003.12.013"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G, "R": R})])
    self.N = N
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MTVI2(WCPSExpr):
  """Modified Triangular Vegetation Index 2"""
  short_name = "MTVI2"
  long_name = "Modified Triangular Vegetation Index 2"
  bands = ['N', 'G', 'R']
  formula = "(1.5 * (1.2 * (N - G) - 2.5 * (R - G))) / ((((2.0 * N + 1) ** 2) - (6.0 * N - 5 * (R ** 0.5)) - 0.5) ** 0.5)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.rse.2003.12.013"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G, "R": R})])
    self.N = N
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class MuWIR(WCPSExpr):
  """Revised Multi-Spectral Water Index"""
  short_name = "MuWIR"
  long_name = "Revised Multi-Spectral Water Index"
  bands = ['B', 'G', 'N', 'S2', 'S1']
  formula = "-4.0 * ((B - G)/(B + G)) + 2.0 * ((G - N)/(G + N)) + 2.0 * ((G - S2)/(G + S2)) - ((G - S1)/(G + S1))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3390/rs10101643"
  contributor = "https://github.com/davemlz"

  def __init__(self, B: OperandType, G: OperandType, N: OperandType, S2: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"B": B, "G": G, "N": N, "S2": S2, "S1": S1})])
    self.B = B
    self.G = G
    self.N = N
    self.S2 = S2
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NBAI(WCPSExpr):
  """Normalized Built-up Area Index"""
  short_name = "NBAI"
  long_name = "Normalized Built-up Area Index"
  bands = ['S2', 'S1', 'G']
  formula = "(S2 - S1/G)/(S2 + S1/G)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://www.omicsonline.org/scientific-reports/JGRS-SR136.pdf"
  contributor = "https://github.com/davemlz"

  def __init__(self, S2: OperandType, S1: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S2": S2, "S1": S1, "G": G})])
    self.S2 = S2
    self.S1 = S1
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NBLI(WCPSExpr):
  """Normalized Difference Bare Land Index"""
  short_name = "NBLI"
  long_name = "Normalized Difference Bare Land Index"
  bands = ['R', 'T']
  formula = "(R - T)/(R + T)"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.3390/rs9030249"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, T: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "T": T})])
    self.R = R
    self.T = T

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NBLIOLI(WCPSExpr):
  """Normalized Difference Bare Land Index for Landsat-OLI"""
  short_name = "NBLIOLI"
  long_name = "Normalized Difference Bare Land Index for Landsat-OLI"
  bands = ['R', 'T1']
  formula = "(R - T1)/(R + T1)"
  platforms = ['Landsat-OLI']
  reference = "https://doi.org/10.3390/rs9030249"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, T1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "T1": T1})])
    self.R = R
    self.T1 = T1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NBR(WCPSExpr):
  """Normalized Burn Ratio"""
  short_name = "NBR"
  long_name = "Normalized Burn Ratio"
  bands = ['N', 'S2']
  formula = "(N - S2) / (N + S2)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3133/ofr0211"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S2": S2})])
    self.N = N
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NBR2(WCPSExpr):
  """Normalized Burn Ratio 2"""
  short_name = "NBR2"
  long_name = "Normalized Burn Ratio 2"
  bands = ['S1', 'S2']
  formula = "(S1 - S2) / (S1 + S2)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://www.usgs.gov/core-science-systems/nli/landsat/landsat-normalized-burn-ratio-2"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "S2": S2})])
    self.S1 = S1
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NBRSWIR(WCPSExpr):
  """Normalized Burn Ratio SWIR"""
  short_name = "NBRSWIR"
  long_name = "Normalized Burn Ratio SWIR"
  bands = ['S2', 'S1']
  formula = "(S2 - S1 - 0.02)/(S2 + S1 + 0.1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1080/22797254.2020.1738900"
  contributor = "https://github.com/davemlz"

  def __init__(self, S2: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S2": S2, "S1": S1})])
    self.S2 = S2
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NBRT1(WCPSExpr):
  """Normalized Burn Ratio Thermal 1"""
  short_name = "NBRT1"
  long_name = "Normalized Burn Ratio Thermal 1"
  bands = ['N', 'S2', 'T']
  formula = "(N - (S2 * T / 10000.0)) / (N + (S2 * T / 10000.0))"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.1080/01431160500239008"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S2: OperandType, T: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S2": S2, "T": T})])
    self.N = N
    self.S2 = S2
    self.T = T

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NBRT2(WCPSExpr):
  """Normalized Burn Ratio Thermal 2"""
  short_name = "NBRT2"
  long_name = "Normalized Burn Ratio Thermal 2"
  bands = ['N', 'T', 'S2']
  formula = "((N / (T / 10000.0)) - S2) / ((N / (T / 10000.0)) + S2)"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.1080/01431160500239008"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, T: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "T": T, "S2": S2})])
    self.N = N
    self.T = T
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NBRT3(WCPSExpr):
  """Normalized Burn Ratio Thermal 3"""
  short_name = "NBRT3"
  long_name = "Normalized Burn Ratio Thermal 3"
  bands = ['N', 'T', 'S2']
  formula = "((N - (T / 10000.0)) - S2) / ((N - (T / 10000.0)) + S2)"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.1080/01431160500239008"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, T: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "T": T, "S2": S2})])
    self.N = N
    self.T = T
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NBRplus(WCPSExpr):
  """Normalized Burn Ratio Plus"""
  short_name = "NBRplus"
  long_name = "Normalized Burn Ratio Plus"
  bands = ['S2', 'N2', 'G', 'B']
  formula = "(S2 - N2 - G - B)/(S2 + N2 + G + B)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.3390/rs14071727"
  contributor = "https://github.com/davemlz"

  def __init__(self, S2: OperandType, N2: OperandType, G: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S2": S2, "N2": N2, "G": G, "B": B})])
    self.S2 = S2
    self.N2 = N2
    self.G = G
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NBSIMS(WCPSExpr):
  """Non-Binary Snow Index for Multi-Component Surfaces"""
  short_name = "NBSIMS"
  long_name = "Non-Binary Snow Index for Multi-Component Surfaces"
  bands = ['G', 'R', 'N', 'B', 'S2', 'S1']
  formula = "0.36 * (G + R + N) - (((B + S2)/G) + S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3390/rs13142777"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, R: OperandType, N: OperandType, B: OperandType, S2: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R, "N": N, "B": B, "S2": S2, "S1": S1})])
    self.G = G
    self.R = R
    self.N = N
    self.B = B
    self.S2 = S2
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NBUI(WCPSExpr):
  """New Built-Up Index"""
  short_name = "NBUI"
  long_name = "New Built-Up Index"
  bands = ['S1', 'N', 'T', 'R', 'L', 'G']
  formula = "((S1 - N)/(10.0 * (T + S1) ** 0.5)) - (((N - R) * (1.0 + L))/(N - R + L)) - (G - S1)/(G + S1)"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://hdl.handle.net/1959.11/29500"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, N: OperandType, T: OperandType, R: OperandType, L: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "N": N, "T": T, "R": R, "L": L, "G": G})])
    self.S1 = S1
    self.N = N
    self.T = T
    self.R = R
    self.L = L
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class ND705(WCPSExpr):
  """Normalized Difference (705 and 750 nm)"""
  short_name = "ND705"
  long_name = "Normalized Difference (705 and 750 nm)"
  bands = ['RE2', 'RE1']
  formula = "(RE2 - RE1)/(RE2 + RE1)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0034-4257(02)00010-X"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "RE1": RE1})])
    self.RE2 = RE2
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDBI(WCPSExpr):
  """Normalized Difference Built-Up Index"""
  short_name = "NDBI"
  long_name = "Normalized Difference Built-Up Index"
  bands = ['S1', 'N']
  formula = "(S1 - N) / (S1 + N)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "http://dx.doi.org/10.1080/01431160304987"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "N": N})])
    self.S1 = S1
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDBaI(WCPSExpr):
  """Normalized Difference Bareness Index"""
  short_name = "NDBaI"
  long_name = "Normalized Difference Bareness Index"
  bands = ['S1', 'T']
  formula = "(S1 - T) / (S1 + T)"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.1109/IGARSS.2005.1526319"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, T: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "T": T})])
    self.S1 = S1
    self.T = T

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDCI(WCPSExpr):
  """Normalized Difference Chlorophyll Index"""
  short_name = "NDCI"
  long_name = "Normalized Difference Chlorophyll Index"
  bands = ['RE1', 'R']
  formula = "(RE1 - R)/(RE1 + R)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/j.rse.2011.10.016"
  contributor = "https://github.com/kalab-oto"

  def __init__(self, RE1: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE1": RE1, "R": R})])
    self.RE1 = RE1
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDDI(WCPSExpr):
  """Normalized Difference Drought Index"""
  short_name = "NDDI"
  long_name = "Normalized Difference Drought Index"
  bands = ['N', 'R', 'G']
  formula = "(((N - R)/(N + R)) - ((G - N)/(G + N)))/(((N - R)/(N + R)) + ((G - N)/(G + N)))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1029/2006GL029127"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "G": G})])
    self.N = N
    self.R = R
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDGI(WCPSExpr):
  """Normalized Difference Greenness Index"""
  short_name = "NDGI"
  long_name = "Normalized Difference Greenness Index"
  bands = ['lambdaN', 'lambdaR', 'lambdaG', 'G', 'N', 'R']
  formula = "(((lambdaN - lambdaR)/(lambdaN - lambdaG)) * G + (1.0 - ((lambdaN - lambdaR)/(lambdaN - lambdaG))) * N - R)/(((lambdaN - lambdaR)/(lambdaN - lambdaG)) * G + (1.0 - ((lambdaN - lambdaR)/(lambdaN - lambdaG))) * N + R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.rse.2019.03.028"
  contributor = "https://github.com/davemlz"

  def __init__(self, lambdaN: OperandType, lambdaR: OperandType, lambdaG: OperandType, G: OperandType, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"lambdaN": lambdaN, "lambdaR": lambdaR, "lambdaG": lambdaG, "G": G, "N": N, "R": R})])
    self.lambdaN = lambdaN
    self.lambdaR = lambdaR
    self.lambdaG = lambdaG
    self.G = G
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDGlaI(WCPSExpr):
  """Normalized Difference Glacier Index"""
  short_name = "NDGlaI"
  long_name = "Normalized Difference Glacier Index"
  bands = ['G', 'R']
  formula = "(G - R)/(G + R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1080/01431160802385459"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R})])
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDII(WCPSExpr):
  """Normalized Difference Infrared Index"""
  short_name = "NDII"
  long_name = "Normalized Difference Infrared Index"
  bands = ['N', 'S1']
  formula = "(N - S1)/(N + S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://www.asprs.org/wp-content/uploads/pers/1983journal/jan/1983_jan_77-83.pdf"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S1": S1})])
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDISIb(WCPSExpr):
  """Normalized Difference Impervious Surface Index Blue"""
  short_name = "NDISIb"
  long_name = "Normalized Difference Impervious Surface Index Blue"
  bands = ['T', 'B', 'N', 'S1']
  formula = "(T - (B + N + S1) / 3.0)/(T + (B + N + S1) / 3.0)"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.14358/PERS.76.5.557"
  contributor = "https://github.com/davemlz"

  def __init__(self, T: OperandType, B: OperandType, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"T": T, "B": B, "N": N, "S1": S1})])
    self.T = T
    self.B = B
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDISIg(WCPSExpr):
  """Normalized Difference Impervious Surface Index Green"""
  short_name = "NDISIg"
  long_name = "Normalized Difference Impervious Surface Index Green"
  bands = ['T', 'G', 'N', 'S1']
  formula = "(T - (G + N + S1) / 3.0)/(T + (G + N + S1) / 3.0)"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.14358/PERS.76.5.557"
  contributor = "https://github.com/davemlz"

  def __init__(self, T: OperandType, G: OperandType, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"T": T, "G": G, "N": N, "S1": S1})])
    self.T = T
    self.G = G
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDISImndwi(WCPSExpr):
  """Normalized Difference Impervious Surface Index with MNDWI"""
  short_name = "NDISImndwi"
  long_name = "Normalized Difference Impervious Surface Index with MNDWI"
  bands = ['T', 'G', 'S1', 'N']
  formula = "(T - (((G - S1)/(G + S1)) + N + S1) / 3.0)/(T + (((G - S1)/(G + S1)) + N + S1) / 3.0)"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.14358/PERS.76.5.557"
  contributor = "https://github.com/davemlz"

  def __init__(self, T: OperandType, G: OperandType, S1: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"T": T, "G": G, "S1": S1, "N": N})])
    self.T = T
    self.G = G
    self.S1 = S1
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDISIndwi(WCPSExpr):
  """Normalized Difference Impervious Surface Index with NDWI"""
  short_name = "NDISIndwi"
  long_name = "Normalized Difference Impervious Surface Index with NDWI"
  bands = ['T', 'G', 'N', 'S1']
  formula = "(T - (((G - N)/(G + N)) + N + S1) / 3.0)/(T + (((G - N)/(G + N)) + N + S1) / 3.0)"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.14358/PERS.76.5.557"
  contributor = "https://github.com/davemlz"

  def __init__(self, T: OperandType, G: OperandType, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"T": T, "G": G, "N": N, "S1": S1})])
    self.T = T
    self.G = G
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDISIr(WCPSExpr):
  """Normalized Difference Impervious Surface Index Red"""
  short_name = "NDISIr"
  long_name = "Normalized Difference Impervious Surface Index Red"
  bands = ['T', 'R', 'N', 'S1']
  formula = "(T - (R + N + S1) / 3.0)/(T + (R + N + S1) / 3.0)"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.14358/PERS.76.5.557"
  contributor = "https://github.com/davemlz"

  def __init__(self, T: OperandType, R: OperandType, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"T": T, "R": R, "N": N, "S1": S1})])
    self.T = T
    self.R = R
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDMI(WCPSExpr):
  """Normalized Difference Moisture Index"""
  short_name = "NDMI"
  long_name = "Normalized Difference Moisture Index"
  bands = ['N', 'S1']
  formula = "(N - S1)/(N + S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/S0034-4257(01)00318-2"
  contributor = "https://github.com/bpurinton"

  def __init__(self, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S1": S1})])
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDPI(WCPSExpr):
  """Normalized Difference Phenology Index"""
  short_name = "NDPI"
  long_name = "Normalized Difference Phenology Index"
  bands = ['N', 'alpha', 'R', 'S1']
  formula = "(N - (alpha * R + (1.0 - alpha) * S1))/(N + (alpha * R + (1.0 - alpha) * S1))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.rse.2017.04.031"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, alpha: OperandType, R: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "alpha": alpha, "R": R, "S1": S1})])
    self.N = N
    self.alpha = alpha
    self.R = R
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDPolI(WCPSExpr):
  """Normalized Difference Polarization Index"""
  short_name = "NDPolI"
  long_name = "Normalized Difference Polarization Index"
  bands = ['VV', 'VH']
  formula = "(VV - VH)/(VV + VH)"
  platforms = ['Sentinel-1 (Dual Polarisation VV-VH)']
  reference = "https://www.isprs.org/proceedings/XXXVII/congress/4_pdf/267.pdf"
  contributor = "https://github.com/davemlz"

  def __init__(self, VV: OperandType, VH: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"VV": VV, "VH": VH})])
    self.VV = VV
    self.VH = VH

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDPonI(WCPSExpr):
  """Normalized Difference Pond Index"""
  short_name = "NDPonI"
  long_name = "Normalized Difference Pond Index"
  bands = ['S1', 'G']
  formula = "(S1-G)/(S1+G)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.rse.2006.07.012"
  contributor = "https://github.com/CvenGeo"

  def __init__(self, S1: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "G": G})])
    self.S1 = S1
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDREI(WCPSExpr):
  """Normalized Difference Red Edge Index"""
  short_name = "NDREI"
  long_name = "Normalized Difference Red Edge Index"
  bands = ['N', 'RE1']
  formula = "(N - RE1) / (N + RE1)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/1011-1344(93)06963-4"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "RE1": RE1})])
    self.N = N
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDSI(WCPSExpr):
  """Normalized Difference Snow Index"""
  short_name = "NDSI"
  long_name = "Normalized Difference Snow Index"
  bands = ['G', 'S1']
  formula = "(G - S1) / (G + S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1109/IGARSS.1994.399618"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "S1": S1})])
    self.G = G
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDSII(WCPSExpr):
  """Normalized Difference Snow Ice Index"""
  short_name = "NDSII"
  long_name = "Normalized Difference Snow Ice Index"
  bands = ['G', 'N']
  formula = "(G - N)/(G + N)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1080/01431160802385459"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "N": N})])
    self.G = G
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDSIWV(WCPSExpr):
  """WorldView Normalized Difference Soil Index"""
  short_name = "NDSIWV"
  long_name = "WorldView Normalized Difference Soil Index"
  bands = ['G', 'Y']
  formula = "(G - Y)/(G + Y)"
  platforms = []
  reference = "https://www.semanticscholar.org/paper/Using-WorldView-2-Vis-NIR-MSI-Imagery-to-Support-Wolf/5e5063ccc4ee76b56b721c866e871d47a77f9fb4"
  contributor = "https://github.com/remi-braun"

  def __init__(self, G: OperandType, Y: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "Y": Y})])
    self.G = G
    self.Y = Y

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDSInw(WCPSExpr):
  """Normalized Difference Snow Index with no Water"""
  short_name = "NDSInw"
  long_name = "Normalized Difference Snow Index with no Water"
  bands = ['N', 'S1', 'beta']
  formula = "(N - S1 - beta)/(N + S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3390/w12051339"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S1: OperandType, beta: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S1": S1, "beta": beta})])
    self.N = N
    self.S1 = S1
    self.beta = beta

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDSWIR(WCPSExpr):
  """Normalized Difference SWIR"""
  short_name = "NDSWIR"
  long_name = "Normalized Difference SWIR"
  bands = ['N', 'S1']
  formula = "(N - S1)/(N + S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1109/TGRS.2003.819190"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S1": S1})])
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDSaII(WCPSExpr):
  """Normalized Difference Snow and Ice Index"""
  short_name = "NDSaII"
  long_name = "Normalized Difference Snow and Ice Index"
  bands = ['R', 'S1']
  formula = "(R - S1) / (R + S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1080/01431160119766"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "S1": S1})])
    self.R = R
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDSoI(WCPSExpr):
  """Normalized Difference Soil Index"""
  short_name = "NDSoI"
  long_name = "Normalized Difference Soil Index"
  bands = ['S2', 'G']
  formula = "(S2 - G)/(S2 + G)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.jag.2015.02.010"
  contributor = "https://github.com/davemlz"

  def __init__(self, S2: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S2": S2, "G": G})])
    self.S2 = S2
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDTI(WCPSExpr):
  """Normalized Difference Turbidity Index"""
  short_name = "NDTI"
  long_name = "Normalized Difference Turbidity Index"
  bands = ['R', 'G']
  formula = "(R-G)/(R+G)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.rse.2006.07.012"
  contributor = "https://github.com/CvenGeo"

  def __init__(self, R: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "G": G})])
    self.R = R
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDVI(WCPSExpr):
  """Normalized Difference Vegetation Index"""
  short_name = "NDVI"
  long_name = "Normalized Difference Vegetation Index"
  bands = ['N', 'R']
  formula = "(N - R)/(N + R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://ntrs.nasa.gov/citations/19740022614"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDVI705(WCPSExpr):
  """Normalized Difference Vegetation Index (705 and 750 nm)"""
  short_name = "NDVI705"
  long_name = "Normalized Difference Vegetation Index (705 and 750 nm)"
  bands = ['RE2', 'RE1']
  formula = "(RE2 - RE1) / (RE2 + RE1)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0176-1617(11)81633-0"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "RE1": RE1})])
    self.RE2 = RE2
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDVIMNDWI(WCPSExpr):
  """NDVI-MNDWI Model"""
  short_name = "NDVIMNDWI"
  long_name = "NDVI-MNDWI Model"
  bands = ['N', 'R', 'G', 'S1']
  formula = "((N - R)/(N + R)) - ((G - S1)/(G + S1))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1007/978-3-662-45737-5_51"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, G: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "G": G, "S1": S1})])
    self.N = N
    self.R = R
    self.G = G
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDVIT(WCPSExpr):
  """Normalized Difference Vegetation Index Thermal"""
  short_name = "NDVIT"
  long_name = "Normalized Difference Vegetation Index Thermal"
  bands = ['N', 'R', 'T']
  formula = "(N - (R * T / 10000.0))/(N + (R * T / 10000.0))"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.1080/01431160600954704"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, T: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "T": T})])
    self.N = N
    self.R = R
    self.T = T

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDWI(WCPSExpr):
  """Normalized Difference Water Index"""
  short_name = "NDWI"
  long_name = "Normalized Difference Water Index"
  bands = ['G', 'N']
  formula = "(G - N) / (G + N)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1080/01431169608948714"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "N": N})])
    self.G = G
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDWIns(WCPSExpr):
  """Normalized Difference Water Index with no Snow Cover and Glaciers"""
  short_name = "NDWIns"
  long_name = "Normalized Difference Water Index with no Snow Cover and Glaciers"
  bands = ['G', 'alpha', 'N']
  formula = "(G - alpha * N)/(G + N)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.3390/w12051339"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, alpha: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "alpha": alpha, "N": N})])
    self.G = G
    self.alpha = alpha
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NDYI(WCPSExpr):
  """Normalized Difference Yellowness Index"""
  short_name = "NDYI"
  long_name = "Normalized Difference Yellowness Index"
  bands = ['G', 'B']
  formula = "(G - B) / (G + B)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.rse.2016.06.016"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "B": B})])
    self.G = G
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NGRDI(WCPSExpr):
  """Normalized Green Red Difference Index"""
  short_name = "NGRDI"
  long_name = "Normalized Green Red Difference Index"
  bands = ['G', 'R']
  formula = "(G - R) / (G + R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/0034-4257(79)90013-0"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R})])
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NHFD(WCPSExpr):
  """Non-Homogeneous Feature Difference"""
  short_name = "NHFD"
  long_name = "Non-Homogeneous Feature Difference"
  bands = ['RE1', 'A']
  formula = "(RE1 - A) / (RE1 + A)"
  platforms = ['Sentinel-2']
  reference = "https://www.semanticscholar.org/paper/Using-WorldView-2-Vis-NIR-MSI-Imagery-to-Support-Wolf/5e5063ccc4ee76b56b721c866e871d47a77f9fb4"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE1: OperandType, A: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE1": RE1, "A": A})])
    self.RE1 = RE1
    self.A = A

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NIRv(WCPSExpr):
  """Near-Infrared Reflectance of Vegetation"""
  short_name = "NIRv"
  long_name = "Near-Infrared Reflectance of Vegetation"
  bands = ['N', 'R']
  formula = "((N - R) / (N + R)) * N"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1126/sciadv.1602244"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NIRvH2(WCPSExpr):
  """Hyperspectral Near-Infrared Reflectance of Vegetation"""
  short_name = "NIRvH2"
  long_name = "Hyperspectral Near-Infrared Reflectance of Vegetation"
  bands = ['N', 'R', 'k', 'lambdaN', 'lambdaR']
  formula = "N - R - k * (lambdaN - lambdaR)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.rse.2021.112723"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, k: OperandType, lambdaN: OperandType, lambdaR: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "k": k, "lambdaN": lambdaN, "lambdaR": lambdaR})])
    self.N = N
    self.R = R
    self.k = k
    self.lambdaN = lambdaN
    self.lambdaR = lambdaR

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NIRvP(WCPSExpr):
  """Near-Infrared Reflectance of Vegetation and Incoming PAR"""
  short_name = "NIRvP"
  long_name = "Near-Infrared Reflectance of Vegetation and Incoming PAR"
  bands = ['N', 'R', 'PAR']
  formula = "((N - R) / (N + R)) * N * PAR"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.rse.2021.112763"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, PAR: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "PAR": PAR})])
    self.N = N
    self.R = R
    self.PAR = PAR

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NLI(WCPSExpr):
  """Non-Linear Vegetation Index"""
  short_name = "NLI"
  long_name = "Non-Linear Vegetation Index"
  bands = ['N', 'R']
  formula = "((N ** 2) - R)/((N ** 2) + R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1080/02757259409532252"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NMDI(WCPSExpr):
  """Normalized Multi-band Drought Index"""
  short_name = "NMDI"
  long_name = "Normalized Multi-band Drought Index"
  bands = ['N', 'S1', 'S2']
  formula = "(N - (S1 - S2))/(N + (S1 - S2))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1029/2007GL031021"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S1: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S1": S1, "S2": S2})])
    self.N = N
    self.S1 = S1
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NRFIg(WCPSExpr):
  """Normalized Rapeseed Flowering Index Green"""
  short_name = "NRFIg"
  long_name = "Normalized Rapeseed Flowering Index Green"
  bands = ['G', 'S2']
  formula = "(G - S2) / (G + S2)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3390/rs13010105"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "S2": S2})])
    self.G = G
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NRFIr(WCPSExpr):
  """Normalized Rapeseed Flowering Index Red"""
  short_name = "NRFIr"
  long_name = "Normalized Rapeseed Flowering Index Red"
  bands = ['R', 'S2']
  formula = "(R - S2) / (R + S2)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3390/rs13010105"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "S2": S2})])
    self.R = R
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NSDS(WCPSExpr):
  """Normalized Shortwave Infrared Difference Soil-Moisture"""
  short_name = "NSDS"
  long_name = "Normalized Shortwave Infrared Difference Soil-Moisture"
  bands = ['S1', 'S2']
  formula = "(S1 - S2)/(S1 + S2)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3390/land10030231"
  contributor = "https://github.com/davemlz"

  def __init__(self, S1: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "S2": S2})])
    self.S1 = S1
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NSDSI1(WCPSExpr):
  """Normalized Shortwave-Infrared Difference Bare Soil Moisture Index 1"""
  short_name = "NSDSI1"
  long_name = "Normalized Shortwave-Infrared Difference Bare Soil Moisture Index 1"
  bands = ['S1', 'S2']
  formula = "(S1-S2)/S1"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.isprsjprs.2019.06.012"
  contributor = "https://github.com/CvenGeo"

  def __init__(self, S1: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "S2": S2})])
    self.S1 = S1
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NSDSI2(WCPSExpr):
  """Normalized Shortwave-Infrared Difference Bare Soil Moisture Index 2"""
  short_name = "NSDSI2"
  long_name = "Normalized Shortwave-Infrared Difference Bare Soil Moisture Index 2"
  bands = ['S1', 'S2']
  formula = "(S1-S2)/S2"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.isprsjprs.2019.06.012"
  contributor = "https://github.com/CvenGeo"

  def __init__(self, S1: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "S2": S2})])
    self.S1 = S1
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NSDSI3(WCPSExpr):
  """Normalized Shortwave-Infrared Difference Bare Soil Moisture Index 3"""
  short_name = "NSDSI3"
  long_name = "Normalized Shortwave-Infrared Difference Bare Soil Moisture Index 3"
  bands = ['S1', 'S2']
  formula = "(S1-S2)/(S1+S2)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.isprsjprs.2019.06.012"
  contributor = "https://github.com/CvenGeo"

  def __init__(self, S1: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S1": S1, "S2": S2})])
    self.S1 = S1
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NSTv1(WCPSExpr):
  """NIR-SWIR-Temperature Version 1"""
  short_name = "NSTv1"
  long_name = "NIR-SWIR-Temperature Version 1"
  bands = ['N', 'S2', 'T']
  formula = "((N-S2)/(N+S2))*T"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.1016/j.rse.2011.06.010"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S2: OperandType, T: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S2": S2, "T": T})])
    self.N = N
    self.S2 = S2
    self.T = T

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NSTv2(WCPSExpr):
  """NIR-SWIR-Temperature Version 2"""
  short_name = "NSTv2"
  long_name = "NIR-SWIR-Temperature Version 2"
  bands = ['N', 'S2', 'T']
  formula = "(N-(S2+T))/(N+(S2+T))"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.1016/j.rse.2011.06.010"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S2: OperandType, T: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S2": S2, "T": T})])
    self.N = N
    self.S2 = S2
    self.T = T

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NWI(WCPSExpr):
  """New Water Index"""
  short_name = "NWI"
  long_name = "New Water Index"
  bands = ['B', 'N', 'S1', 'S2']
  formula = "(B - (N + S1 + S2))/(B + (N + S1 + S2))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.11873/j.issn.1004-0323.2009.2.167"
  contributor = "https://github.com/davemlz"

  def __init__(self, B: OperandType, N: OperandType, S1: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"B": B, "N": N, "S1": S1, "S2": S2})])
    self.B = B
    self.N = N
    self.S1 = S1
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NormG(WCPSExpr):
  """Normalized Green"""
  short_name = "NormG"
  long_name = "Normalized Green"
  bands = ['G', 'N', 'R']
  formula = "G/(N + G + R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.2134/agronj2004.0314"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "N": N, "R": R})])
    self.G = G
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NormNIR(WCPSExpr):
  """Normalized NIR"""
  short_name = "NormNIR"
  long_name = "Normalized NIR"
  bands = ['N', 'G', 'R']
  formula = "N/(N + G + R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.2134/agronj2004.0314"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G, "R": R})])
    self.N = N
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class NormR(WCPSExpr):
  """Normalized Red"""
  short_name = "NormR"
  long_name = "Normalized Red"
  bands = ['R', 'N', 'G']
  formula = "R/(N + G + R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.2134/agronj2004.0314"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, N: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "N": N, "G": G})])
    self.R = R
    self.N = N
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class OCVI(WCPSExpr):
  """Optimized Chlorophyll Vegetation Index"""
  short_name = "OCVI"
  long_name = "Optimized Chlorophyll Vegetation Index"
  bands = ['N', 'G', 'R', 'cexp']
  formula = "(N / G) * (R / G) ** cexp"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "http://dx.doi.org/10.1007/s11119-008-9075-z"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType, R: OperandType, cexp: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G, "R": R, "cexp": cexp})])
    self.N = N
    self.G = G
    self.R = R
    self.cexp = cexp

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class OSAVI(WCPSExpr):
  """Optimized Soil-Adjusted Vegetation Index"""
  short_name = "OSAVI"
  long_name = "Optimized Soil-Adjusted Vegetation Index"
  bands = ['N', 'R']
  formula = "(N - R) / (N + R + 0.16)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/0034-4257(95)00186-7"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class OSI(WCPSExpr):
  """Oil Spill Index"""
  short_name = "OSI"
  long_name = "Oil Spill Index"
  bands = ['G', 'R', 'B']
  formula = "(G + R)/B"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.mex.2021.101327"
  contributor = "https://github.com/emanuelcastanho"

  def __init__(self, G: OperandType, R: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R, "B": B})])
    self.G = G
    self.R = R
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class PI(WCPSExpr):
  """Plastic Index"""
  short_name = "PI"
  long_name = "Plastic Index"
  bands = ['N', 'R']
  formula = "N/(N + R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.3390/rs12162648"
  contributor = "https://github.com/emanuelcastanho"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class PISI(WCPSExpr):
  """Perpendicular Impervious Surface Index"""
  short_name = "PISI"
  long_name = "Perpendicular Impervious Surface Index"
  bands = ['B', 'N']
  formula = "0.8192 * B - 0.5735 * N + 0.0750"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.3390/rs10101521"
  contributor = "https://github.com/davemlz"

  def __init__(self, B: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"B": B, "N": N})])
    self.B = B
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class PSRI(WCPSExpr):
  """Plant Senescing Reflectance Index"""
  short_name = "PSRI"
  long_name = "Plant Senescing Reflectance Index"
  bands = ['R', 'B', 'RE2']
  formula = "(R - B)/RE2"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1034/j.1399-3054.1999.106119.x"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, B: OperandType, RE2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "B": B, "RE2": RE2})])
    self.R = R
    self.B = B
    self.RE2 = RE2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class QpRVI(WCPSExpr):
  """Quad-Polarized Radar Vegetation Index"""
  short_name = "QpRVI"
  long_name = "Quad-Polarized Radar Vegetation Index"
  bands = ['HV', 'HH', 'VV']
  formula = "(8.0 * HV)/(HH + VV + 2.0 * HV)"
  platforms = []
  reference = "https://doi.org/10.1109/IGARSS.2001.976856"
  contributor = "https://github.com/davemlz"

  def __init__(self, HV: OperandType, HH: OperandType, VV: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"HV": HV, "HH": HH, "VV": VV})])
    self.HV = HV
    self.HH = HH
    self.VV = VV

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class RCC(WCPSExpr):
  """Red Chromatic Coordinate"""
  short_name = "RCC"
  long_name = "Red Chromatic Coordinate"
  bands = ['R', 'G', 'B']
  formula = "R / (R + G + B)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/0034-4257(87)90088-5"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, G: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "G": G, "B": B})])
    self.R = R
    self.G = G
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class RDVI(WCPSExpr):
  """Renormalized Difference Vegetation Index"""
  short_name = "RDVI"
  long_name = "Renormalized Difference Vegetation Index"
  bands = ['N', 'R']
  formula = "(N - R) / ((N + R) ** 0.5)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/0034-4257(94)00114-3"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class REDSI(WCPSExpr):
  """Red-Edge Disease Stress Index"""
  short_name = "REDSI"
  long_name = "Red-Edge Disease Stress Index"
  bands = ['RE3', 'R', 'RE1']
  formula = "((705.0 - 665.0) * (RE3 - R) - (783.0 - 665.0) * (RE1 - R)) / (2.0 * R)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.3390/s18030868"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE3: OperandType, R: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE3": RE3, "R": R, "RE1": RE1})])
    self.RE3 = RE3
    self.R = R
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class RENDVI(WCPSExpr):
  """Red Edge Normalized Difference Vegetation Index"""
  short_name = "RENDVI"
  long_name = "Red Edge Normalized Difference Vegetation Index"
  bands = ['RE2', 'RE1']
  formula = "(RE2 - RE1)/(RE2 + RE1)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0176-1617(11)81633-0"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "RE1": RE1})])
    self.RE2 = RE2
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class RFDI(WCPSExpr):
  """Radar Forest Degradation Index"""
  short_name = "RFDI"
  long_name = "Radar Forest Degradation Index"
  bands = ['HH', 'HV']
  formula = "(HH - HV)/(HH + HV)"
  platforms = ['Sentinel-1 (Dual Polarisation HH-HV)']
  reference = "https://doi.org/10.5194/bg-9-179-2012"
  contributor = "https://github.com/davemlz"

  def __init__(self, HH: OperandType, HV: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"HH": HH, "HV": HV})])
    self.HH = HH
    self.HV = HV

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class RGBVI(WCPSExpr):
  """Red Green Blue Vegetation Index"""
  short_name = "RGBVI"
  long_name = "Red Green Blue Vegetation Index"
  bands = ['G', 'B', 'R']
  formula = "(G ** 2.0 - B * R)/(G ** 2.0 + B * R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.jag.2015.02.012"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, B: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "B": B, "R": R})])
    self.G = G
    self.B = B
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class RGRI(WCPSExpr):
  """Red-Green Ratio Index"""
  short_name = "RGRI"
  long_name = "Red-Green Ratio Index"
  bands = ['R', 'G']
  formula = "R/G"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.jag.2014.03.018"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "G": G})])
    self.R = R
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class RI(WCPSExpr):
  """Redness Index"""
  short_name = "RI"
  long_name = "Redness Index"
  bands = ['R', 'G']
  formula = "(R - G)/(R + G)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://www.documentation.ird.fr/hor/fdi:34390"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "G": G})])
    self.R = R
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class RI4XS(WCPSExpr):
  """SPOT HRV XS-based Redness Index 4"""
  short_name = "RI4XS"
  long_name = "SPOT HRV XS-based Redness Index 4"
  bands = ['R', 'G']
  formula = "(R**2.0)/(G**4.0)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/S0034-4257(98)00030-3"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "G": G})])
    self.R = R
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class RNDVI(WCPSExpr):
  """Reversed Normalized Difference Vegetation Index"""
  short_name = "RNDVI"
  long_name = "Reversed Normalized Difference Vegetation Index"
  bands = ['R', 'N']
  formula = "(R - N)/(R + N)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.3390/rs12162648"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "N": N})])
    self.R = R
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class RVI(WCPSExpr):
  """Ratio Vegetation Index"""
  short_name = "RVI"
  long_name = "Ratio Vegetation Index"
  bands = ['RE2', 'R']
  formula = "RE2 / R"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.2134/agronj1968.00021962006000060016x"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "R": R})])
    self.RE2 = RE2
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class S2REP(WCPSExpr):
  """Sentinel-2 Red-Edge Position"""
  short_name = "S2REP"
  long_name = "Sentinel-2 Red-Edge Position"
  bands = ['RE3', 'R', 'RE1', 'RE2']
  formula = "705.0 + 35.0 * ((((RE3 + R) / 2.0) - RE1) / (RE2 - RE1))"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/j.isprsjprs.2013.04.007"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE3: OperandType, R: OperandType, RE1: OperandType, RE2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE3": RE3, "R": R, "RE1": RE1, "RE2": RE2})])
    self.RE3 = RE3
    self.R = R
    self.RE1 = RE1
    self.RE2 = RE2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class S2WI(WCPSExpr):
  """Sentinel-2 Water Index"""
  short_name = "S2WI"
  long_name = "Sentinel-2 Water Index"
  bands = ['RE1', 'S2']
  formula = "(RE1 - S2)/(RE1 + S2)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.3390/w13121647"
  contributor = "https://github.com/MATRIX4284"

  def __init__(self, RE1: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE1": RE1, "S2": S2})])
    self.RE1 = RE1
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class S3(WCPSExpr):
  """S3 Snow Index"""
  short_name = "S3"
  long_name = "S3 Snow Index"
  bands = ['N', 'R', 'S1']
  formula = "(N * (R - S1)) / ((N + R) * (N + S1))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3178/jjshwr.12.28"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "S1": S1})])
    self.N = N
    self.R = R
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SARVI(WCPSExpr):
  """Soil Adjusted and Atmospherically Resistant Vegetation Index"""
  short_name = "SARVI"
  long_name = "Soil Adjusted and Atmospherically Resistant Vegetation Index"
  bands = ['L', 'N', 'R', 'B']
  formula = "(1 + L)*(N - (R - (R - B))) / (N + (R - (R - B)) + L)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1109/36.134076"
  contributor = "https://github.com/davemlz"

  def __init__(self, L: OperandType, N: OperandType, R: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"L": L, "N": N, "R": R, "B": B})])
    self.L = L
    self.N = N
    self.R = R
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SAVI(WCPSExpr):
  """Soil-Adjusted Vegetation Index"""
  short_name = "SAVI"
  long_name = "Soil-Adjusted Vegetation Index"
  bands = ['L', 'N', 'R']
  formula = "(1.0 + L) * (N - R) / (N + R + L)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/0034-4257(88)90106-X"
  contributor = "https://github.com/davemlz"

  def __init__(self, L: OperandType, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"L": L, "N": N, "R": R})])
    self.L = L
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SAVI2(WCPSExpr):
  """Soil-Adjusted Vegetation Index 2"""
  short_name = "SAVI2"
  long_name = "Soil-Adjusted Vegetation Index 2"
  bands = ['N', 'R', 'slb', 'sla']
  formula = "N / (R + (slb / sla))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1080/01431169008955053"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, slb: OperandType, sla: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "slb": slb, "sla": sla})])
    self.N = N
    self.R = R
    self.slb = slb
    self.sla = sla

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SAVIT(WCPSExpr):
  """Soil-Adjusted Vegetation Index Thermal"""
  short_name = "SAVIT"
  long_name = "Soil-Adjusted Vegetation Index Thermal"
  bands = ['L', 'N', 'R', 'T']
  formula = "(1.0 + L) * (N - (R * T / 10000.0)) / (N + (R * T / 10000.0) + L)"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.1080/01431160600954704"
  contributor = "https://github.com/davemlz"

  def __init__(self, L: OperandType, N: OperandType, R: OperandType, T: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"L": L, "N": N, "R": R, "T": T})])
    self.L = L
    self.N = N
    self.R = R
    self.T = T

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SEVI(WCPSExpr):
  """Shadow-Eliminated Vegetation Index"""
  short_name = "SEVI"
  long_name = "Shadow-Eliminated Vegetation Index"
  bands = ['N', 'R', 'fdelta']
  formula = "(N/R) + fdelta * (1.0/R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1080/17538947.2018.1495770"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, fdelta: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "fdelta": fdelta})])
    self.N = N
    self.R = R
    self.fdelta = fdelta

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SI(WCPSExpr):
  """Shadow Index"""
  short_name = "SI"
  long_name = "Shadow Index"
  bands = ['B', 'G', 'R']
  formula = "((1.0 - B) * (1.0 - G) * (1.0 - R)) ** (1/3)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.465.8749&rep=rep1&type=pdf"
  contributor = "https://github.com/davemlz"

  def __init__(self, B: OperandType, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"B": B, "G": G, "R": R})])
    self.B = B
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SIPI(WCPSExpr):
  """Structure Insensitive Pigment Index"""
  short_name = "SIPI"
  long_name = "Structure Insensitive Pigment Index"
  bands = ['N', 'A', 'R']
  formula = "(N - A) / (N - R)"
  platforms = ['Sentinel-2', 'Landsat-OLI']
  reference = "https://eurekamag.com/research/009/395/009395053.php"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, A: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "A": A, "R": R})])
    self.N = N
    self.A = A
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SLAVI(WCPSExpr):
  """Specific Leaf Area Vegetation Index"""
  short_name = "SLAVI"
  long_name = "Specific Leaf Area Vegetation Index"
  bands = ['N', 'R', 'S2']
  formula = "N/(R + S2)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://www.asprs.org/wp-content/uploads/pers/2000journal/february/2000_feb_183-191.pdf"
  contributor = "https://github.com/geoSanjeeb"

  def __init__(self, N: OperandType, R: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "S2": S2})])
    self.N = N
    self.R = R
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SR(WCPSExpr):
  """Simple Ratio"""
  short_name = "SR"
  long_name = "Simple Ratio"
  bands = ['N', 'R']
  formula = "N/R"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.2307/1936256"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SR2(WCPSExpr):
  """Simple Ratio (800 and 550 nm)"""
  short_name = "SR2"
  long_name = "Simple Ratio (800 and 550 nm)"
  bands = ['N', 'G']
  formula = "N/G"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1080/01431169308904370"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G})])
    self.N = N
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SR3(WCPSExpr):
  """Simple Ratio (860, 550 and 708 nm)"""
  short_name = "SR3"
  long_name = "Simple Ratio (860, 550 and 708 nm)"
  bands = ['N2', 'G', 'RE1']
  formula = "N2/(G * RE1)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0034-4257(98)00046-7"
  contributor = "https://github.com/davemlz"

  def __init__(self, N2: OperandType, G: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N2": N2, "G": G, "RE1": RE1})])
    self.N2 = N2
    self.G = G
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SR555(WCPSExpr):
  """Simple Ratio (555 and 750 nm)"""
  short_name = "SR555"
  long_name = "Simple Ratio (555 and 750 nm)"
  bands = ['RE2', 'G']
  formula = "RE2 / G"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0176-1617(11)81633-0"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "G": G})])
    self.RE2 = RE2
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SR705(WCPSExpr):
  """Simple Ratio (705 and 750 nm)"""
  short_name = "SR705"
  long_name = "Simple Ratio (705 and 750 nm)"
  bands = ['RE2', 'RE1']
  formula = "RE2 / RE1"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0176-1617(11)81633-0"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "RE1": RE1})])
    self.RE2 = RE2
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SWI(WCPSExpr):
  """Snow Water Index"""
  short_name = "SWI"
  long_name = "Snow Water Index"
  bands = ['G', 'N', 'S1']
  formula = "(G * (N - S1)) / ((G + N) * (N + S1))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3390/rs11232774"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "N": N, "S1": S1})])
    self.G = G
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SWM(WCPSExpr):
  """Sentinel Water Mask"""
  short_name = "SWM"
  long_name = "Sentinel Water Mask"
  bands = ['B', 'G', 'N', 'S1']
  formula = "(B + G)/(N + S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://eoscience.esa.int/landtraining2017/files/posters/MILCZAREK.pdf"
  contributor = "https://github.com/davemlz"

  def __init__(self, B: OperandType, G: OperandType, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"B": B, "G": G, "N": N, "S1": S1})])
    self.B = B
    self.G = G
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class SeLI(WCPSExpr):
  """Sentinel-2 LAI Green Index"""
  short_name = "SeLI"
  long_name = "Sentinel-2 LAI Green Index"
  bands = ['N2', 'RE1']
  formula = "(N2 - RE1) / (N2 + RE1)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.3390/s19040904"
  contributor = "https://github.com/davemlz"

  def __init__(self, N2: OperandType, RE1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N2": N2, "RE1": RE1})])
    self.N2 = N2
    self.RE1 = RE1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class TCARI(WCPSExpr):
  """Transformed Chlorophyll Absorption in Reflectance Index"""
  short_name = "TCARI"
  long_name = "Transformed Chlorophyll Absorption in Reflectance Index"
  bands = ['RE1', 'R', 'G']
  formula = "3 * ((RE1 - R) - 0.2 * (RE1 - G) * (RE1 / R))"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0034-4257(02)00018-4"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE1: OperandType, R: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE1": RE1, "R": R, "G": G})])
    self.RE1 = RE1
    self.R = R
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class TCARIOSAVI(WCPSExpr):
  """TCARI/OSAVI Ratio"""
  short_name = "TCARIOSAVI"
  long_name = "TCARI/OSAVI Ratio"
  bands = ['RE1', 'R', 'G', 'N']
  formula = "(3 * ((RE1 - R) - 0.2 * (RE1 - G) * (RE1 / R))) / (1.16 * (N - R) / (N + R + 0.16))"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0034-4257(02)00018-4"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE1: OperandType, R: OperandType, G: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE1": RE1, "R": R, "G": G, "N": N})])
    self.RE1 = RE1
    self.R = R
    self.G = G
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class TCARIOSAVI705(WCPSExpr):
  """TCARI/OSAVI Ratio (705 and 750 nm)"""
  short_name = "TCARIOSAVI705"
  long_name = "TCARI/OSAVI Ratio (705 and 750 nm)"
  bands = ['RE2', 'RE1', 'G']
  formula = "(3 * ((RE2 - RE1) - 0.2 * (RE2 - G) * (RE2 / RE1))) / (1.16 * (RE2 - RE1) / (RE2 + RE1 + 0.16))"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/j.agrformet.2008.03.005"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, RE1: OperandType, G: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "RE1": RE1, "G": G})])
    self.RE2 = RE2
    self.RE1 = RE1
    self.G = G

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class TCI(WCPSExpr):
  """Triangular Chlorophyll Index"""
  short_name = "TCI"
  long_name = "Triangular Chlorophyll Index"
  bands = ['RE1', 'G', 'R']
  formula = "1.2 * (RE1 - G) - 1.5 * (R - G) * (RE1 / R) ** 0.5"
  platforms = ['Sentinel-2']
  reference = "http://dx.doi.org/10.1109/TGRS.2007.904836"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE1: OperandType, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE1": RE1, "G": G, "R": R})])
    self.RE1 = RE1
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class TDVI(WCPSExpr):
  """Transformed Difference Vegetation Index"""
  short_name = "TDVI"
  long_name = "Transformed Difference Vegetation Index"
  bands = ['N', 'R']
  formula = "1.5 * ((N - R)/((N ** 2.0 + R + 0.5) ** 0.5))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1109/IGARSS.2002.1026867"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class TGI(WCPSExpr):
  """Triangular Greenness Index"""
  short_name = "TGI"
  long_name = "Triangular Greenness Index"
  bands = ['R', 'G', 'B']
  formula = "- 0.5 * (190 * (R - G) - 120 * (R - B))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "http://dx.doi.org/10.1016/j.jag.2012.07.020"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, G: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "G": G, "B": B})])
    self.R = R
    self.G = G
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class TRRVI(WCPSExpr):
  """Transformed Red Range Vegetation Index"""
  short_name = "TRRVI"
  long_name = "Transformed Red Range Vegetation Index"
  bands = ['RE2', 'R', 'N']
  formula = "((RE2 - R) / (RE2 + R)) / (((N - R) / (N + R)) + 1.0)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.3390/rs12152359"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, R: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "R": R, "N": N})])
    self.RE2 = RE2
    self.R = R
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class TSAVI(WCPSExpr):
  """Transformed Soil-Adjusted Vegetation Index"""
  short_name = "TSAVI"
  long_name = "Transformed Soil-Adjusted Vegetation Index"
  bands = ['sla', 'N', 'R', 'slb']
  formula = "sla * (N - sla * R - slb) / (sla * N + R - sla * slb)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1109/IGARSS.1989.576128"
  contributor = "https://github.com/davemlz"

  def __init__(self, sla: OperandType, N: OperandType, R: OperandType, slb: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"sla": sla, "N": N, "R": R, "slb": slb})])
    self.sla = sla
    self.N = N
    self.R = R
    self.slb = slb

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class TTVI(WCPSExpr):
  """Transformed Triangular Vegetation Index"""
  short_name = "TTVI"
  long_name = "Transformed Triangular Vegetation Index"
  bands = ['RE3', 'RE2', 'N2']
  formula = "0.5 * ((865.0 - 740.0) * (RE3 - RE2) - (N2 - RE2) * (783.0 - 740))"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.3390/rs12010016"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE3: OperandType, RE2: OperandType, N2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE3": RE3, "RE2": RE2, "N2": N2})])
    self.RE3 = RE3
    self.RE2 = RE2
    self.N2 = N2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class TVI(WCPSExpr):
  """Transformed Vegetation Index"""
  short_name = "TVI"
  long_name = "Transformed Vegetation Index"
  bands = ['N', 'R']
  formula = "(((N - R)/(N + R)) + 0.5) ** 0.5"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://ntrs.nasa.gov/citations/19740022614"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R})])
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class TWI(WCPSExpr):
  """Triangle Water Index"""
  short_name = "TWI"
  long_name = "Triangle Water Index"
  bands = ['RE1', 'RE2', 'G', 'S2', 'B', 'N']
  formula = "(2.84 * (RE1 - RE2) / (G + S2)) + ((1.25 * (G - B) - (N - B)) / (N + 1.25 * G - 0.25 * B))"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.3390/rs14215289"
  contributor = "https://github.com/remi-braun"

  def __init__(self, RE1: OperandType, RE2: OperandType, G: OperandType, S2: OperandType, B: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE1": RE1, "RE2": RE2, "G": G, "S2": S2, "B": B, "N": N})])
    self.RE1 = RE1
    self.RE2 = RE2
    self.G = G
    self.S2 = S2
    self.B = B
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class TriVI(WCPSExpr):
  """Triangular Vegetation Index"""
  short_name = "TriVI"
  long_name = "Triangular Vegetation Index"
  bands = ['N', 'G', 'R']
  formula = "0.5 * (120 * (N - G) - 200 * (R - G))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "http://dx.doi.org/10.1016/S0034-4257(00)00197-8"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "G": G, "R": R})])
    self.N = N
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class UI(WCPSExpr):
  """Urban Index"""
  short_name = "UI"
  long_name = "Urban Index"
  bands = ['S2', 'N']
  formula = "(S2 - N)/(S2 + N)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://www.isprs.org/proceedings/XXXI/congress/part7/321_XXXI-part7.pdf"
  contributor = "https://github.com/davemlz"

  def __init__(self, S2: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"S2": S2, "N": N})])
    self.S2 = S2
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VARI(WCPSExpr):
  """Visible Atmospherically Resistant Index"""
  short_name = "VARI"
  long_name = "Visible Atmospherically Resistant Index"
  bands = ['G', 'R', 'B']
  formula = "(G - R) / (G + R - B)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/S0034-4257(01)00289-9"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, R: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R, "B": B})])
    self.G = G
    self.R = R
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VARI700(WCPSExpr):
  """Visible Atmospherically Resistant Index (700 nm)"""
  short_name = "VARI700"
  long_name = "Visible Atmospherically Resistant Index (700 nm)"
  bands = ['RE1', 'R', 'B']
  formula = "(RE1 - 1.7 * R + 0.7 * B) / (RE1 + 1.3 * R - 1.3 * B)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0034-4257(01)00289-9"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE1: OperandType, R: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE1": RE1, "R": R, "B": B})])
    self.RE1 = RE1
    self.R = R
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VDDPI(WCPSExpr):
  """Vertical Dual De-Polarization Index"""
  short_name = "VDDPI"
  long_name = "Vertical Dual De-Polarization Index"
  bands = ['VV', 'VH']
  formula = "(VV + VH)/VV"
  platforms = ['Sentinel-1 (Dual Polarisation VV-VH)']
  reference = "https://doi.org/10.1016/j.rse.2018.09.003"
  contributor = "https://github.com/davemlz"

  def __init__(self, VV: OperandType, VH: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"VV": VV, "VH": VH})])
    self.VV = VV
    self.VH = VH

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VHVVD(WCPSExpr):
  """VH-VV Difference"""
  short_name = "VHVVD"
  long_name = "VH-VV Difference"
  bands = ['VH', 'VV']
  formula = "VH - VV"
  platforms = ['Sentinel-1 (Dual Polarisation VV-VH)']
  reference = "https://doi.org/10.3390/app9040655"
  contributor = "https://github.com/davemlz"

  def __init__(self, VH: OperandType, VV: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"VH": VH, "VV": VV})])
    self.VH = VH
    self.VV = VV

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VHVVP(WCPSExpr):
  """VH-VV Product"""
  short_name = "VHVVP"
  long_name = "VH-VV Product"
  bands = ['VH', 'VV']
  formula = "VH * VV"
  platforms = ['Sentinel-1 (Dual Polarisation VV-VH)']
  reference = "https://doi.org/10.1109/IGARSS47720.2021.9554099"
  contributor = "https://github.com/davemlz"

  def __init__(self, VH: OperandType, VV: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"VH": VH, "VV": VV})])
    self.VH = VH
    self.VV = VV

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VHVVR(WCPSExpr):
  """VH-VV Ratio"""
  short_name = "VHVVR"
  long_name = "VH-VV Ratio"
  bands = ['VH', 'VV']
  formula = "VH/VV"
  platforms = ['Sentinel-1 (Dual Polarisation VV-VH)']
  reference = "https://doi.org/10.1109/IGARSS47720.2021.9554099"
  contributor = "https://github.com/davemlz"

  def __init__(self, VH: OperandType, VV: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"VH": VH, "VV": VV})])
    self.VH = VH
    self.VV = VV

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VI6T(WCPSExpr):
  """VI6T Index"""
  short_name = "VI6T"
  long_name = "VI6T Index"
  bands = ['N', 'T']
  formula = "(N - T/10000.0)/(N + T/10000.0)"
  platforms = ['Landsat-TM', 'Landsat-ETM+']
  reference = "https://doi.org/10.1080/01431160500239008"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, T: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "T": T})])
    self.N = N
    self.T = T

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VI700(WCPSExpr):
  """Vegetation Index (700 nm)"""
  short_name = "VI700"
  long_name = "Vegetation Index (700 nm)"
  bands = ['RE1', 'R']
  formula = "(RE1 - R) / (RE1 + R)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0034-4257(01)00289-9"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE1: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE1": RE1, "R": R})])
    self.RE1 = RE1
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VIBI(WCPSExpr):
  """Vegetation Index Built-up Index"""
  short_name = "VIBI"
  long_name = "Vegetation Index Built-up Index"
  bands = ['N', 'R', 'S1']
  formula = "((N-R)/(N+R))/(((N-R)/(N+R)) + ((S1-N)/(S1+N)))"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "http://dx.doi.org/10.1080/01431161.2012.687842"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "S1": S1})])
    self.N = N
    self.R = R
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VIG(WCPSExpr):
  """Vegetation Index Green"""
  short_name = "VIG"
  long_name = "Vegetation Index Green"
  bands = ['G', 'R']
  formula = "(G - R) / (G + R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/S0034-4257(01)00289-9"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R})])
    self.G = G
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VVVHD(WCPSExpr):
  """VV-VH Difference"""
  short_name = "VVVHD"
  long_name = "VV-VH Difference"
  bands = ['VV', 'VH']
  formula = "VV - VH"
  platforms = ['Sentinel-1 (Dual Polarisation VV-VH)']
  reference = "https://doi.org/10.1109/IGARSS47720.2021.9554099"
  contributor = "https://github.com/davemlz"

  def __init__(self, VV: OperandType, VH: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"VV": VV, "VH": VH})])
    self.VV = VV
    self.VH = VH

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VVVHR(WCPSExpr):
  """VV-VH Ratio"""
  short_name = "VVVHR"
  long_name = "VV-VH Ratio"
  bands = ['VV', 'VH']
  formula = "VV/VH"
  platforms = ['Sentinel-1 (Dual Polarisation VV-VH)']
  reference = "https://doi.org/10.3390/app9040655"
  contributor = "https://github.com/davemlz"

  def __init__(self, VV: OperandType, VH: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"VV": VV, "VH": VH})])
    self.VV = VV
    self.VH = VH

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VVVHS(WCPSExpr):
  """VV-VH Sum"""
  short_name = "VVVHS"
  long_name = "VV-VH Sum"
  bands = ['VV', 'VH']
  formula = "VV + VH"
  platforms = ['Sentinel-1 (Dual Polarisation VV-VH)']
  reference = "https://doi.org/10.1109/IGARSS47720.2021.9554099"
  contributor = "https://github.com/davemlz"

  def __init__(self, VV: OperandType, VH: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"VV": VV, "VH": VH})])
    self.VV = VV
    self.VH = VH

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VgNIRBI(WCPSExpr):
  """Visible Green-Based Built-Up Index"""
  short_name = "VgNIRBI"
  long_name = "Visible Green-Based Built-Up Index"
  bands = ['G', 'N']
  formula = "(G - N)/(G + N)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.ecolind.2015.03.037"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "N": N})])
    self.G = G
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class VrNIRBI(WCPSExpr):
  """Visible Red-Based Built-Up Index"""
  short_name = "VrNIRBI"
  long_name = "Visible Red-Based Built-Up Index"
  bands = ['R', 'N']
  formula = "(R - N)/(R + N)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/j.ecolind.2015.03.037"
  contributor = "https://github.com/davemlz"

  def __init__(self, R: OperandType, N: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"R": R, "N": N})])
    self.R = R
    self.N = N

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class WDRVI(WCPSExpr):
  """Wide Dynamic Range Vegetation Index"""
  short_name = "WDRVI"
  long_name = "Wide Dynamic Range Vegetation Index"
  bands = ['alpha', 'N', 'R']
  formula = "(alpha * N - R) / (alpha * N + R)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1078/0176-1617-01176"
  contributor = "https://github.com/davemlz"

  def __init__(self, alpha: OperandType, N: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"alpha": alpha, "N": N, "R": R})])
    self.alpha = alpha
    self.N = N
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class WDVI(WCPSExpr):
  """Weighted Difference Vegetation Index"""
  short_name = "WDVI"
  long_name = "Weighted Difference Vegetation Index"
  bands = ['N', 'sla', 'R']
  formula = "N - sla * R"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1016/0034-4257(89)90076-X"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, sla: OperandType, R: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "sla": sla, "R": R})])
    self.N = N
    self.sla = sla
    self.R = R

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class WI1(WCPSExpr):
  """Water Index 1"""
  short_name = "WI1"
  long_name = "Water Index 1"
  bands = ['G', 'S2']
  formula = "(G - S2) / (G + S2)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3390/rs11182186"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "S2": S2})])
    self.G = G
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class WI2(WCPSExpr):
  """Water Index 2"""
  short_name = "WI2"
  long_name = "Water Index 2"
  bands = ['B', 'S2']
  formula = "(B - S2) / (B + S2)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.3390/rs11182186"
  contributor = "https://github.com/davemlz"

  def __init__(self, B: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"B": B, "S2": S2})])
    self.B = B
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class WI2015(WCPSExpr):
  """Water Index 2015"""
  short_name = "WI2015"
  long_name = "Water Index 2015"
  bands = ['G', 'R', 'N', 'S1', 'S2']
  formula = "1.7204 + 171 * G + 3 * R - 70 * N - 45 * S1 - 71 * S2"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1016/j.rse.2015.12.055"
  contributor = "https://github.com/remi-braun"

  def __init__(self, G: OperandType, R: OperandType, N: OperandType, S1: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R, "N": N, "S1": S1, "S2": S2})])
    self.G = G
    self.R = R
    self.N = N
    self.S1 = S1
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class WRI(WCPSExpr):
  """Water Ratio Index"""
  short_name = "WRI"
  long_name = "Water Ratio Index"
  bands = ['G', 'R', 'N', 'S1']
  formula = "(G + R)/(N + S1)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1109/GEOINFORMATICS.2010.5567762"
  contributor = "https://github.com/davemlz"

  def __init__(self, G: OperandType, R: OperandType, N: OperandType, S1: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"G": G, "R": R, "N": N, "S1": S1})])
    self.G = G
    self.R = R
    self.N = N
    self.S1 = S1

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class bNIRv(WCPSExpr):
  """Blue Near-Infrared Reflectance of Vegetation"""
  short_name = "bNIRv"
  long_name = "Blue Near-Infrared Reflectance of Vegetation"
  bands = ['N', 'B']
  formula = "((N - B)/(N + B)) * N"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1029/2024JG008240"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, B: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "B": B})])
    self.N = N
    self.B = B

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class kEVI(WCPSExpr):
  """Kernel Enhanced Vegetation Index"""
  short_name = "kEVI"
  long_name = "Kernel Enhanced Vegetation Index"
  bands = ['g', 'kNN', 'kNR', 'C1', 'C2', 'kNB', 'kNL']
  formula = "g * (kNN - kNR) / (kNN + C1 * kNR - C2 * kNB + kNL)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1126/sciadv.abc7447"
  contributor = "https://github.com/davemlz"

  def __init__(self, g: OperandType, kNN: OperandType, kNR: OperandType, C1: OperandType, C2: OperandType, kNB: OperandType, kNL: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"g": g, "kNN": kNN, "kNR": kNR, "C1": C1, "C2": C2, "kNB": kNB, "kNL": kNL})])
    self.g = g
    self.kNN = kNN
    self.kNR = kNR
    self.C1 = C1
    self.C2 = C2
    self.kNB = kNB
    self.kNL = kNL

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class kIPVI(WCPSExpr):
  """Kernel Infrared Percentage Vegetation Index"""
  short_name = "kIPVI"
  long_name = "Kernel Infrared Percentage Vegetation Index"
  bands = ['kNN', 'kNR']
  formula = "kNN/(kNN + kNR)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1126/sciadv.abc7447"
  contributor = "https://github.com/davemlz"

  def __init__(self, kNN: OperandType, kNR: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"kNN": kNN, "kNR": kNR})])
    self.kNN = kNN
    self.kNR = kNR

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class kNDVI(WCPSExpr):
  """Kernel Normalized Difference Vegetation Index"""
  short_name = "kNDVI"
  long_name = "Kernel Normalized Difference Vegetation Index"
  bands = ['kNN', 'kNR']
  formula = "(kNN - kNR)/(kNN + kNR)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1126/sciadv.abc7447"
  contributor = "https://github.com/davemlz"

  def __init__(self, kNN: OperandType, kNR: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"kNN": kNN, "kNR": kNR})])
    self.kNN = kNN
    self.kNR = kNR

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class kRVI(WCPSExpr):
  """Kernel Ratio Vegetation Index"""
  short_name = "kRVI"
  long_name = "Kernel Ratio Vegetation Index"
  bands = ['kNN', 'kNR']
  formula = "kNN / kNR"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1126/sciadv.abc7447"
  contributor = "https://github.com/davemlz"

  def __init__(self, kNN: OperandType, kNR: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"kNN": kNN, "kNR": kNR})])
    self.kNN = kNN
    self.kNR = kNR

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class kVARI(WCPSExpr):
  """Kernel Visible Atmospherically Resistant Index"""
  short_name = "kVARI"
  long_name = "Kernel Visible Atmospherically Resistant Index"
  bands = ['kGG', 'kGR', 'kGB']
  formula = "(kGG - kGR) / (kGG + kGR - kGB)"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS', 'Planet-Fusion']
  reference = "https://doi.org/10.1126/sciadv.abc7447"
  contributor = "https://github.com/davemlz"

  def __init__(self, kGG: OperandType, kGR: OperandType, kGB: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"kGG": kGG, "kGR": kGR, "kGB": kGB})])
    self.kGG = kGG
    self.kGR = kGR
    self.kGB = kGB

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class mND705(WCPSExpr):
  """Modified Normalized Difference (705, 750 and 445 nm)"""
  short_name = "mND705"
  long_name = "Modified Normalized Difference (705, 750 and 445 nm)"
  bands = ['RE2', 'RE1', 'A']
  formula = "(RE2 - RE1)/(RE2 + RE1 - A)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0034-4257(02)00010-X"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, RE1: OperandType, A: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "RE1": RE1, "A": A})])
    self.RE2 = RE2
    self.RE1 = RE1
    self.A = A

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class mSR705(WCPSExpr):
  """Modified Simple Ratio (705 and 445 nm)"""
  short_name = "mSR705"
  long_name = "Modified Simple Ratio (705 and 445 nm)"
  bands = ['RE2', 'A']
  formula = "(RE2 - A)/(RE2 + A)"
  platforms = ['Sentinel-2']
  reference = "https://doi.org/10.1016/S0034-4257(02)00010-X"
  contributor = "https://github.com/davemlz"

  def __init__(self, RE2: OperandType, A: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"RE2": RE2, "A": A})])
    self.RE2 = RE2
    self.A = A

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class sNIRvLSWI(WCPSExpr):
  """SWIR-enhanced Near-Infrared Reflectance of Vegetation for LSWI"""
  short_name = "sNIRvLSWI"
  long_name = "SWIR-enhanced Near-Infrared Reflectance of Vegetation for LSWI"
  bands = ['N', 'S2']
  formula = "((N - S2)/(N + S2)) * N"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1029/2024JG008240"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "S2": S2})])
    self.N = N
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class sNIRvNDPI(WCPSExpr):
  """SWIR-enhanced Near-Infrared Reflectance of Vegetation for NDPI"""
  short_name = "sNIRvNDPI"
  long_name = "SWIR-enhanced Near-Infrared Reflectance of Vegetation for NDPI"
  bands = ['N', 'alpha', 'R', 'S2']
  formula = "(N - (alpha * R + (1.0 - alpha) * S2))/(N + (alpha * R + (1.0 - alpha) * S2)) * N"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1029/2024JG008240"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, alpha: OperandType, R: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "alpha": alpha, "R": R, "S2": S2})])
    self.N = N
    self.alpha = alpha
    self.R = R
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class sNIRvNDVILSWIP(WCPSExpr):
  """SWIR-enhanced Near-Infrared Reflectance of Vegetation for the NDVI-LSWI Product"""
  short_name = "sNIRvNDVILSWIP"
  long_name = "SWIR-enhanced Near-Infrared Reflectance of Vegetation for the NDVI-LSWI Product"
  bands = ['N', 'R', 'S2']
  formula = "((N - R)/(N + R)) * ((N - S2)/(N + S2)) * N"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1029/2024JG008240"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "S2": S2})])
    self.N = N
    self.R = R
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class sNIRvNDVILSWIS(WCPSExpr):
  """SWIR-enhanced Near-Infrared Reflectance of Vegetation for the NDVI-LSWI Sum"""
  short_name = "sNIRvNDVILSWIS"
  long_name = "SWIR-enhanced Near-Infrared Reflectance of Vegetation for the NDVI-LSWI Sum"
  bands = ['N', 'R', 'S2']
  formula = "(((N - R)/(N + R)) + ((N - S2)/(N + S2))) * N"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1029/2024JG008240"
  contributor = "https://github.com/davemlz"

  def __init__(self, N: OperandType, R: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "S2": S2})])
    self.N = N
    self.R = R
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


class sNIRvSWIR(WCPSExpr):
  """SWIR-enhanced Near-Infrared Reflectance of Vegetation"""
  short_name = "sNIRvSWIR"
  long_name = "SWIR-enhanced Near-Infrared Reflectance of Vegetation"
  bands = ['N', 'R', 'S2']
  formula = "((N - R - S2 ** 2.0)/(N + R + S2 ** 2.0)) * N"
  platforms = ['Sentinel-2', 'Landsat-OLI', 'Landsat-TM', 'Landsat-ETM+', 'MODIS']
  reference = "https://doi.org/10.1029/2024JG008240"
  contributor = "https://github.com/MartinuzziFrancesco"

  def __init__(self, N: OperandType, R: OperandType, S2: OperandType):
    super().__init__(operands=[eval(self.formula, {}, {"N": N, "R": R, "S2": S2})])
    self.N = N
    self.R = R
    self.S2 = S2

  def __str__(self):
    return super().__str__() + str(self.operands[0])


