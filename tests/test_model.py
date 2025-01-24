import math

import pytest

from wcps.model import (Datacube, Exp, Log, Ln, Sqrt, Pow, Sin, Cos, Tan,
                        Sinh, Cosh, Tanh, ArcSin, ArcCos, ArcTan, ArcTan2, And,
                        Or, Xor, Not, Overlay, Bit, Band, MultiBand, Axis, Extend, Scale,
                        Reproject, ResampleAlg, Cast, CastType, Sum, Avg, Count, Min, Max,
                        All, Some, AxisIter, Condense, CondenseOp, Coverage, Switch, Encode,
                        Clip, WCPSClientException)

cov1 = Datacube("cov1")
cov2 = Datacube("cov2")
cov3 = Datacube("cov3")
cov4 = Datacube("cov4")


def test_arithmetic():
    assert str(cov1 + cov2) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 + $cov2)"
    assert str(cov1 + 1) == "for $cov1 in (cov1)\nreturn\n  ($cov1 + 1)"
    assert str(1 + cov1) == "for $cov1 in (cov1)\nreturn\n  (1 + $cov1)"
    assert str(1 + cov1 + 2) == "for $cov1 in (cov1)\nreturn\n  ((1 + $cov1) + 2)"
    assert str(cov1 - cov2) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 - $cov2)"
    assert str(2 - cov2) == "for $cov2 in (cov2)\nreturn\n  (2 - $cov2)"
    assert str(cov1 * cov2) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 * $cov2)"
    assert str(cov1 / cov2) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 / $cov2)"
    assert str(cov1 % cov2) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  mod($cov1, $cov2)"
    assert str(abs(cov1)) == "for $cov1 in (cov1)\nreturn\n  abs($cov1)"
    assert str(round(cov1)) == "for $cov1 in (cov1)\nreturn\n  round($cov1)"
    assert str(math.floor(cov1)) == "for $cov1 in (cov1)\nreturn\n  floor($cov1)"
    assert str(math.ceil(cov1)) == "for $cov1 in (cov1)\nreturn\n  ceil($cov1)"


def test_exponential():
    assert str(Exp(cov1)) == "for $cov1 in (cov1)\nreturn\n  exp($cov1)"
    assert str(Log(cov1)) == "for $cov1 in (cov1)\nreturn\n  log($cov1)"
    assert str(Ln(cov1)) == "for $cov1 in (cov1)\nreturn\n  ln($cov1)"
    assert str(Sqrt(cov1)) == "for $cov1 in (cov1)\nreturn\n  sqrt($cov1)"
    assert str(Pow(cov1, cov2)) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  pow($cov1, $cov2)"
    assert str(Pow(cov1, 2)) == "for $cov1 in (cov1)\nreturn\n  pow($cov1, 2)"
    assert str(Pow(2, cov1)) == "for $cov1 in (cov1)\nreturn\n  pow(2, $cov1)"


def test_trigonometric():
    assert str(Sin(cov1)) == "for $cov1 in (cov1)\nreturn\n  sin($cov1)"
    assert str(cov1 + Sin(2)) == "for $cov1 in (cov1)\nreturn\n  ($cov1 + sin(2))"
    assert str(Cos(cov1)) == "for $cov1 in (cov1)\nreturn\n  cos($cov1)"
    assert str(Tan(cov1)) == "for $cov1 in (cov1)\nreturn\n  tan($cov1)"
    assert str(Sinh(cov1)) == "for $cov1 in (cov1)\nreturn\n  sinh($cov1)"
    assert str(Cosh(cov1)) == "for $cov1 in (cov1)\nreturn\n  cosh($cov1)"
    assert str(Tanh(cov1)) == "for $cov1 in (cov1)\nreturn\n  tanh($cov1)"
    assert str(ArcSin(cov1)) == "for $cov1 in (cov1)\nreturn\n  arcsin($cov1)"
    assert str(ArcCos(cov1)) == "for $cov1 in (cov1)\nreturn\n  arccos($cov1)"
    assert str(ArcTan(cov1)) == "for $cov1 in (cov1)\nreturn\n  arctan($cov1)"
    assert str(ArcTan2(cov1)) == "for $cov1 in (cov1)\nreturn\n  arctan2($cov1)"


def test_comparison():
    assert str(cov1 > cov2) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 > $cov2)"
    assert str(cov1 > 1) == "for $cov1 in (cov1)\nreturn\n  ($cov1 > 1)"
    assert str(1 < cov1) == "for $cov1 in (cov1)\nreturn\n  ($cov1 > 1)"
    assert str(cov1 < cov2) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 < $cov2)"
    assert str(cov1 >= cov2) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 >= $cov2)"
    assert str(cov1 <= cov2) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 <= $cov2)"
    assert str(cov1 == cov2) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 = $cov2)"
    assert str(cov1 != cov2) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 != $cov2)"


def test_logical():
    assert str(And(cov1, cov2)) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 and $cov2)"
    assert str(Or(cov1, cov2)) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 or $cov2)"
    assert str(Xor(cov1, cov2)) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 xor $cov2)"
    assert str(Not(cov1)) == "for $cov1 in (cov1)\nreturn\n  (not $cov1)"
    assert str(Overlay(cov1, cov2)) == "for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  ($cov1 overlay $cov2)"
    assert str(Bit(cov1, 2)) == "for $cov1 in (cov1)\nreturn\n  bit($cov1, 2)"


def test_multiband():
    assert str(Band(cov1, 2)) == "for $cov1 in (cov1)\nreturn\n  $cov1.2"
    assert str(Band(cov1, "red")) == "for $cov1 in (cov1)\nreturn\n  $cov1.red"
    assert str(MultiBand({"red": cov1, "blue": cov2})) == \
           'for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  {red: $cov1; blue: $cov2}'
    assert str(MultiBand({"red": cov1, "blue": 2})) == \
           'for $cov1 in (cov1)\nreturn\n  {red: $cov1; blue: 2}'


def test_subsetting():
    assert str(Axis("X", 15, crs="EPSG:4326")) == 'X:"EPSG:4326"(15)'
    assert str(Axis("X", 15.0, 30.0)) == 'X(15.0:30.0)'
    assert str(Axis("X", 15.0, 30.0, crs="EPSG:4326")) == 'X:"EPSG:4326"(15.0:30.0)'
    assert str(Axis("X", "15", "30", crs="EPSG:4326")) == 'X:"EPSG:4326"("15":"30")'
    assert str(cov1[Axis("X", 15.0, 30.0)]) == \
           'for $cov1 in (cov1)\nreturn\n  $cov1[X(15.0:30.0)]'
    assert str(cov1[Axis("X", 15.0, 30.0), Axis("Y", 15.0, 30.0)]) == \
           'for $cov1 in (cov1)\nreturn\n  $cov1[X(15.0:30.0), Y(15.0:30.0)]'
    assert str(cov1[("X", 15.0, 30.0)]) == \
           'for $cov1 in (cov1)\nreturn\n  $cov1[X(15.0:30.0)]'
    assert str(cov1[("X", 15.0, Axis.MAX)]) == \
           'for $cov1 in (cov1)\nreturn\n  $cov1[X(15.0:*)]'
    assert str(cov1[("X", Axis.MIN, Axis.MAX)]) == \
           'for $cov1 in (cov1)\nreturn\n  $cov1[X(*:*)]'
    assert str(cov1[("X", 15.0, 30.0), ("Y", 15.0, 30.0, 'EPSG:4326')]) == \
           'for $cov1 in (cov1)\nreturn\n  $cov1[X(15.0:30.0), Y:"EPSG:4326"(15.0:30.0)]'
    assert str(cov1[("X", 15.0, 30.0), ("Y", 15.0, 30.0, 'EPSG:4326')]) == \
           'for $cov1 in (cov1)\nreturn\n  $cov1[X(15.0:30.0), Y:"EPSG:4326"(15.0:30.0)]'


def test_extend():
    assert str(Extend(cov1, [("X", 15.0, 30.0), ("Y", 15.0, 30.0, 'EPSG:4326')])) == \
           'for $cov1 in (cov1)\nreturn\n  extend($cov1, { X(15.0:30.0), Y:"EPSG:4326"(15.0:30.0) })'


def test_scale():
    assert str(Scale(cov1).to_explicit_grid_domain([("X", 15, 30), ("Y", 20, 40)])) == \
           'for $cov1 in (cov1)\nreturn\n  scale($cov1, { X(15:30), Y(20:40) })'
    assert str(Scale(cov1).to_grid_domain_of(cov2)) == \
           'for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  scale($cov1, { imageCrsDomain($cov2) })'
    assert str(Scale(cov1).by_factor(2.0)) == \
           'for $cov1 in (cov1)\nreturn\n  scale($cov1, 2.0)'
    assert str(Scale(cov1).by_factor_per_axis([("X", 1.5), ("Y", 2)])) == \
           'for $cov1 in (cov1)\nreturn\n  scale($cov1, { X(1.5), Y(2) })'


def test_reproject():
    assert str(Reproject(cov1, "EPSG:4326", ResampleAlg.AVERAGE)) == \
           'for $cov1 in (cov1)\nreturn\n  crsTransform($cov1, "EPSG:4326", { average })'
    assert str(Reproject(cov1, "EPSG:4326").subset_by_coverage_domain(cov2)) == \
           'for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  crsTransform($cov1, "EPSG:4326", { domain($cov2) })'
    assert str(Reproject(cov1, "EPSG:4326", ResampleAlg.AVERAGE).to_axis_resolutions([("X", 1.5), ("Y", 2)])) == \
           'for $cov1 in (cov1)\nreturn\n  crsTransform($cov1, "EPSG:4326", { average }, { X:1.5, Y:2 })'
    assert str(Reproject(cov1, "EPSG:4326").subset_by_axes([("X", 1.5, 2.5), ("Y", 2, 4)])) == \
           'for $cov1 in (cov1)\nreturn\n  crsTransform($cov1, "EPSG:4326", { X(1.5:2.5), Y(2:4) })'


def test_cast():
    assert str(Cast(cov1, CastType.INT)) == "for $cov1 in (cov1)\nreturn\n  ((int) $cov1)"
    assert str(Cast(cov1, CastType.UNSIGNED_CHAR)) == "for $cov1 in (cov1)\nreturn\n  ((unsigned char) $cov1)"


def test_reduce():
    assert str(Sum(cov1)) == "for $cov1 in (cov1)\nreturn\n  sum($cov1)"
    assert str(Avg(cov1)) == "for $cov1 in (cov1)\nreturn\n  avg($cov1)"
    assert str(Count(cov1)) == "for $cov1 in (cov1)\nreturn\n  count($cov1)"
    assert str(Min(cov1)) == "for $cov1 in (cov1)\nreturn\n  min($cov1)"
    assert str(Max(cov1)) == "for $cov1 in (cov1)\nreturn\n  max($cov1)"
    assert str(All(cov1)) == "for $cov1 in (cov1)\nreturn\n  all($cov1)"
    assert str(Some(cov1)) == "for $cov1 in (cov1)\nreturn\n  some($cov1)"


def test_condense():
    pt_var = AxisIter('$pt', 'time').of_grid_axis(cov1)
    pt_ref = pt_var.ref()
    assert str(Condense(CondenseOp.PLUS).over(pt_var).using(cov1 + pt_ref)) == \
           ("for $cov1 in (cov1)\nreturn\n  "
            "(condense + over $pt time(imageCrsDomain($cov1, time)) using ($cov1 + $pt))")
    assert str(Condense(CondenseOp.PLUS).over(pt_var).using(cov1[('time', pt_ref)])) == \
           ("for $cov1 in (cov1)\nreturn\n  "
            "(condense + over $pt time(imageCrsDomain($cov1, time)) using $cov1[time($pt)])")
    px_var = AxisIter('$px', 'X').of_geo_axis(cov1)
    px_ref = px_var.ref()
    assert str(Condense(CondenseOp.MULTIPLY).over(pt_var).over(px_var).using(cov1[('time', pt_ref)] * px_ref)) == \
           ("for $cov1 in (cov1)\nreturn\n  "
            "(condense * over $pt time(imageCrsDomain($cov1, time)), $px X(domain($cov1, X)) "
            "using ($cov1[time($pt)] * $px))")


# -------------------------------------------------------------------------------------
# Coverage

def test_coverage_of_geo_axis():
    plat_var = AxisIter('$pLat', 'Lat').of_geo_axis(cov1['Lat', -30, -28.5])
    plon_var = AxisIter('$pLon', 'Lon').of_geo_axis(cov1['Lon', 111.975, 113.475])
    cov_expr = (Coverage('targetCoverage')
                .over(plat_var).over(plon_var)
                .values(cov1[('Lat', plat_var.ref()), ('Lon', plon_var.ref())]))
    assert (str(cov_expr) ==
            "for $cov1 in (cov1)\nreturn\n  ("
            "coverage targetCoverage "
            "over $pLat Lat(domain($cov1[Lat(-30:-28.5)], Lat)), "
            "$pLon Lon(domain($cov1[Lon(111.975:113.475)], Lon)) "
            "values $cov1[Lat($pLat), Lon($pLon)])")


def test_coverage_with_interval():
    time_var = AxisIter('$pt', 'time').interval(0, 10)
    cov_expr = (Coverage('intervalCoverage')
                .over(time_var)
                .values(cov1['time', time_var.ref()]))

    assert str(cov_expr) == (
        "for $cov1 in (cov1)\nreturn\n  "
        "(coverage intervalCoverage over $pt time(0 : 10) values $cov1[time($pt)])"
    )


def test_coverage_with_interval_and_params():
    time_var = AxisIter('$pt', 'time').interval(0, 10)

    # Create a Coverage expression with additional parameters
    cov_expr = ((Coverage('intervalCoverage')
                 .over(time_var)
                 .values(cov1['time', time_var.ref()]))
                .encode('GTiff')
                .params('{ "configOptions": { "GDAL_CACHEMAX": "64" } }'))
    expected_query = (
        'for $cov1 in (cov1)\nreturn\n  '
        'encode((coverage intervalCoverage over $pt time(0 : 10) values $cov1[time($pt)]), '
        '"GTiff", "{ \\"configOptions\\": { \\"GDAL_CACHEMAX\\": \\"64\\" } }")'
    )

    assert str(cov_expr) == expected_query


def test_coverage_no_axes():
    with pytest.raises(WCPSClientException):
        str(Coverage('noAxesCoverage').values(cov1))


def test_coverage_no_values():
    lat_var = AxisIter('$pLat', 'Lat').of_geo_axis(cov1['Lat', -30, -28.5])
    with pytest.raises(WCPSClientException):
        str(Coverage('noValuesCoverage').over(lat_var))

# -------------------------------------------------------------------------------------
# Clip

def test_clip_linestring1():
    wkt_linestring = ('LINESTRING("2008-01-01T02:01:20.000Z" 75042.7273594 5094865.55794,'
                      ' "2008-01-08T00:02:58.000Z" 705042.727359 5454865.55794)')
    clip_expr = Clip(cov1, wkt_linestring)
    expected_query = ("for $cov1 in (cov1)\nreturn\n  "
                      "clip($cov1, LINESTRING(\"2008-01-01T02:01:20.000Z\" 75042.7273594 5094865.55794, "
                      "\"2008-01-08T00:02:58.000Z\" 705042.727359 5454865.55794))")
    assert str(clip_expr) == expected_query


def test_clip_invalid_wkt():
    invalid_wkt = "INVALID_WKT"
    with pytest.raises(WCPSClientException, match="WKT does not contain a valid geometry type"):
        Clip(cov1, invalid_wkt)

# -------------------------------------------------------------------------------------
# Encode

def test_encode():
    assert str(Encode(cov1, "PNG")) == 'for $cov1 in (cov1)\nreturn\n  encode($cov1, "PNG")'
    assert str(Encode(cov1, "PNG", "params")) == \
           'for $cov1 in (cov1)\nreturn\n  encode($cov1, "PNG", "params")'


def test_encode_to_png():
    encode_expr = Encode(cov1, "PNG")
    expected_query = "for $cov1 in (cov1)\nreturn\n  encode($cov1, \"PNG\")"
    assert str(encode_expr) == expected_query


def test_encode_with_params():
    encode_expr = Encode(cov1, "PNG").params('{"compression":"lzw"}')
    expected_query = 'for $cov1 in (cov1)\nreturn\n  encode($cov1, "PNG", "{\\"compression\\":\\"lzw\\"}")'
    assert str(encode_expr) == expected_query


def test_encode_no_format():
    with pytest.raises(WCPSClientException):
        str(Encode(cov1))


# -------------------------------------------------------------------------------------
# Switch

def test_switch():
    assert str(Switch().case(cov1 > 5).then(cov2).default(cov1)) == \
           ('for $cov1 in (cov1), $cov2 in (cov2)\nreturn\n  '
            '(switch case ($cov1 > 5) return $cov2 default return $cov1)')


def test_switch_no_default():
    # Creating a Switch expression without a default case should raise an exception
    with pytest.raises(WCPSClientException):
        str(Switch().case(cov1 > 5).then(cov2))


def test_switch_multiple_cases():
    switch_expr = (Switch()
                   .case(cov1 > 5).then(cov2)
                   .case(cov1 < 3).then(cov3)
                   .default(cov1))
    expected_query = ("for $cov1 in (cov1), $cov2 in (cov2), $cov3 in (cov3)\n"
                      "return\n  (switch "
                      "case ($cov1 > 5) return $cov2 "
                      "case ($cov1 < 3) return $cov3 "
                      "default return $cov1)")
    assert str(switch_expr) == expected_query


def test_switch_invalid_order():
    with pytest.raises(WCPSClientException):
        Switch().default(cov1).case(cov1 > 5).then(cov1)


def test_nested_switch_expression():
    switch_expr = (Switch()
                   .case(cov1 > 5)
                   .then(Switch()
                         .case(cov2 > 10)
                         .then(cov3)
                         .default(cov4))
                   .default(cov1))
    expected_query = ("for $cov1 in (cov1), $cov2 in (cov2), $cov3 in (cov3), $cov4 in (cov4)\n"
                      "return\n  "
                      "(switch case ($cov1 > 5) return "
                      "(switch case ($cov2 > 10) return $cov3 default return $cov4) "
                      "default return $cov1)")
    assert str(switch_expr) == expected_query


def test_nested_switch_invalid_default_order():
    with pytest.raises(WCPSClientException):
        Switch().case(cov1 > 5).then(
            Switch().default(cov2).case(cov1 < 3).then(cov2)
        ).default(cov1)


def test_scalar_case_input():
    switch_expr = Switch().case(5).then(cov1).default(cov2)
    expected_query = ("for $cov1 in (cov1), $cov2 in (cov2)\n"
                      "return\n  (switch "
                      "case 5 return $cov1 "
                      "default return $cov2)")
    assert str(switch_expr) == expected_query


def test_scalar_then_input():
    switch_expr = Switch().case(cov1).then(5).default(cov2)
    expected_query = ("for $cov1 in (cov1), $cov2 in (cov2)\n"
                      "return\n  (switch "
                      "case $cov1 return 5 "
                      "default return $cov2)")
    assert str(switch_expr) == expected_query


def test_scalar_default_input():
    switch_expr = Switch().case(cov1).then(cov2).default(5)
    expected_query = ("for $cov1 in (cov1), $cov2 in (cov2)\n"
                      "return\n  (switch "
                      "case $cov1 return $cov2 "
                      "default return 5)")
    assert str(switch_expr) == expected_query
