"""
This module defines classes and methods for dynamically building WCPS query expressions.

This can be done by:

1. Composing objects of :class:`WCPSExpr` subclasses, e.g. `Sum(Datacube("cube"))`
2. Chaining methods on :class:`WCPSExpr` objects, e.g. `Datacube("cube").sum()`

Each subclass defines the ``__str__`` method, so that executing
``str(Sum(Datacube("cube"))`` returns a valid WCPS query string
that can be sent to a WCPS server.
"""

# postpone evaluations of type annotations
# https://stackoverflow.com/a/33533514
from __future__ import annotations

from collections import deque
from enum import StrEnum
from typing import Union, Optional


class WCPSExpr:
    """
    An abstract class encapsulating a WCPS expression.

    It contains a list of :attr:`operands` (themselves :class:`WCPSExpr`) and a :attr:`parent`.

    Subclasses for each operator exist, e.g. :class:`Add` for binary addition,
    which are applied to the :attr:`operands`. For most
    operators there are also corresponding methods in this class, allowing to build
    an expression by chaining them, e.g
    ``Sum(Datacube("cube1") + Datacube("cube2"))``
    is the same as
    ``Datacube("cube1").add(Datacube("cube2").sum()``. Notable exceptions are :class:`Switch` and
    :class:`Coverage`.

    Various builtin operators are overloaded to allow writing expressions more naturally,
    e.g. ``WCPSExpr * WCPSExpr``. Number/strings are automatically wrapped in a :class:`Scalar`,
    e.g. ``WCPSExpr * 2`` becomes ``WCPSExpr * Scalar(2)``.

    ``__and__``, ``__or__``, ``__xor__``, ``__invert__`` correspond to BITWISE operators,
    not to the logical and, or, and not. They are not overloaded to the logical
    and/or/xor/not in order to avoid confusion.

    :param operands: the operands of this WCPS expression. This object is set
        as the parent of each operand, while its own parent is set to None.
        Scalar operands such as 1, 4.9 or "test" are automatically wrapped in a :class:`Scalar` object.
    """

    def __init__(self, operands: Optional[OperandType | list[OperandType]] = None):
        self.parent: WCPSExpr = None
        """
        A :class:`WCPSExpr` of which this expression is an operand; ``None`` if this is the root expression.
        E.g. in if this expression is the :class:`Datacube` object in ``Datacube("test") * 5``,
        then the ``parent`` is the :class:`Mul` object.
        """
        self.operands: list[WCPSExpr] = []
        """
        A list of :class:`WCPSExpr` operands of this expressions. E.g. in ``Datacube("test") * 5``, this
        expression is a :class:`Mul`, with :class:`Datacube` and :class:`Scalar` operands.
        """
        if operands is not None:
            if not isinstance(operands, list):
                operands = [operands]
            for op in operands:
                self.add_operand(op)

    def get_datacube_operands(self) -> list[Datacube]:
        """
        :return: all unique :class:`Datacube` objects contained within the expression tree
            starting from this :class:`WCPSExpr`, sorted alphabetically by datacube name.
        """
        operands = deque(self.operands)
        datacubes = set()

        while operands:
            op = operands.popleft()
            if isinstance(op, Datacube):
                datacubes.add(op)
            for c in op.operands:
                operands.append(c)

        return sorted(list(datacubes), key=lambda datacube: datacube.name)

    def add_operand(self, op: OperandType):
        """
        Add an operand to the list of operands. Scalar ``op`` such as 1, 4.9 or
        "test" are automatically wrapped in a :class:`Scalar` object.
        :param op: an operand to be added to the list of this expression's operands;
        if ``op`` is ``None`` it will be ignored.
        """
        if op is not None:
            if isinstance(op, WCPSExpr):
                self.operands.append(op)
            elif isinstance(op, ScalarType):
                self.operands.append(Scalar(op))
            else:
                raise WCPSClientException(f"Invalid operand type {op.__class__}, "
                                          f"expected a WCPSExpr or a scalar value.")
            self.operands[-1].parent = self

    def __str__(self):
        """
        :return: A WCPS query string corresponding to this expression.
        """
        if self.parent is not None:
            return ''

        datacubes = self.get_datacube_operands()
        if len(datacubes) == 0:
            raise WCPSClientException("No datacubes have been specified.")
        datacubes = [f'{d} in ({d.name})' for d in datacubes]
        datacubes_str = ', '.join(datacubes)
        ret = f'for {datacubes_str}\nreturn\n  '
        return ret

    # arithmetic

    def add(self, other: OperandType) -> Add:
        """
        Adds the current operand to another operand.

        :param other: The operand to add to the current operand.
        :return: An instance of the :class:`Add` class representing the addition operation.

        Examples:

        - ``Datacube("test1").add(Datacube("test2"))``
        - ``Datacube("test1").add(5)``
        """
        return Add(self, other)

    def __add__(self, other: OperandType) -> Add:
        """
        Allows the use of the '+' operator to add two operands.

        :param other: The operand to add to the current operand.
        :return: An instance of the :class:`Add` class representing the addition operation.

        Examples:

        - ``Datacube("test1") + Datacube("test2")``
        - ``Datacube("test1") + 5``
        """
        return Add(self, other)

    def __radd__(self, other: OperandType) -> Add:
        """
        Allows the use of the '+' operator with the current operand on the right side.

        :param other: The operand to be added to the current operand.
        :return: An instance of the :class:`Add` class representing the addition operation.

        Examples:

        - ``Datacube("test2") + Datacube("test1")``
        - ``5 + Datacube("test1")``
        """
        return Add(other, self)

    def sub(self, other: OperandType) -> Sub:
        """
        Subtracts another operand from the current operand.

        :param other: The operand to subtract from the current operand.
        :return: An instance of the :class:`Sub` class representing the subtraction operation.

        Examples:

        - ``Datacube("test1").sub(Datacube("test2"))``
        - ``Datacube("test1").sub(5)``
        """
        return Sub(self, other)

    def __sub__(self, other: OperandType) -> Sub:
        """
        Allows the use of the '-' operator to subtract one operand from another.

        :param other: The operand to subtract from the current operand.
        :return: An instance of the `Sub` class representing the subtraction operation.

        Examples:

        - ``Datacube("test1") - Datacube("test2")``
        - ``Datacube("test1") - 5``
        """
        return Sub(self, other)

    def __rsub__(self, other: OperandType) -> Sub:
        """
        Allows the use of the '-' operator with the current operand on the right side.

        :param other: The operand from which the current operand is subtracted.
        :return: An instance of the :class:`Sub` class representing the subtraction operation.

        Examples:

        - ``Datacube("test2") - Datacube("test1")``
        - ``5 - Datacube("test1")``
        """
        return Sub(other, self)

    def mul(self, other: OperandType) -> Mul:
        """
        Multiplies the current operand by another operand.

        :param other: The operand to multiply with the current operand.
        :return: An instance of the :class:`Mul` class representing the multiplication operation.

        Examples:

        - ``Datacube("test1").mul(Datacube("test2"))``
        - ``Datacube("test1").mul(5)``
        """
        return Mul(self, other)

    def __mul__(self, other: OperandType) -> Mul:
        """
        Allows the use of the '*' operator to multiply two operands.

        :param other: The operand to multiply with the current operand.
        :return: An instance of the :class:`Mul` class representing the multiplication operation.

        Examples:

        - ``Datacube("test1") * Datacube("test2")``
        - ``Datacube("test1") * 5``
        """
        return Mul(self, other)

    def __rmul__(self, other: OperandType) -> Mul:
        """
        Allows the use of the '*' operator with the current operand on the right side.

        :param other: The operand to be multiplied with the current operand.
        :return: An instance of the :class:`Mul` class representing the multiplication operation.

        Examples:

        - ``Datacube("test1") * Datacube("test2")``
        - ``5 * Datacube("test1")``
        """
        return Mul(other, self)

    def div(self, other: OperandType) -> Div:
        """
        Divides the current operand by another operand.

        :param other: The operand to divide the current operand by.
        :return: An instance of the :class:`Div` class representing the division operation.

        Examples:

        - ``Datacube("test1").div(Datacube("test2"))``
        - ``Datacube("test1").div(5)``
        """
        return Div(self, other)

    def __div__(self, other: OperandType) -> Div:
        """
        Allows the use of the '/' operator to divide one operand by another.

        :param other: The operand to divide the current operand by.
        :return: An instance of the :class:`Div` class representing the division operation.

        Examples:

        - ``Datacube("test1") / Datacube("test2")``
        - ``Datacube("test1") / 5``
        """
        return Div(self, other)

    def __rdiv__(self, other: OperandType) -> Div:
        """
        Allows the use of the '/' operator with the current operand on the right side.

        :param other: The operand to be divided by the current operand.
        :return: An instance of the :class:`Div` class representing the division operation.

        Examples:

        - ``Datacube("test2") / Datacube("test1")``
        - ``5 / Datacube("test1")``
        """
        return Div(other, self)

    def __truediv__(self, other: OperandType) -> Div:
        """
        Allows the use of the '//' operator to perform true division.

        :param other: The operand to divide the current operand by.
        :return: An instance of the :class:`Div` class representing the division operation.

        Examples:

        - ``Datacube("test1") / Datacube("test2")``
        - ``Datacube("test1") / 5``
        """
        return Div(self, other)

    def __rtruediv__(self, other: OperandType) -> Div:
        """
        Allows the use of the '//' operator with the current operand on the right side.

        :param other: The operand to be divided by the current operand.
        :return: An instance of the :class:`Div` class representing the division operation.

        Examples:

        - ``Datacube("test2") / Datacube("test1")``
        - ``5 / Datacube("test1")``
        """
        return Div(other, self)

    def mod(self, other: OperandType) -> Mod:
        """
        Computes the modulus (remainder of the division) of the current operand by another operand.

        :param other: The operand to use as the divisor.
        :return: An instance of the :class:`Mod` class representing the modulus operation.

        Examples:

        - ``Datacube("test1").mod(Datacube("test2"))``
        - ``Datacube("test1").mod(5)``
        """
        return Mod(self, other)

    def __mod__(self, other: OperandType) -> Mod:
        """
        Allows the use of the '%' operator to compute the modulus of two operands.

        :param other: The operand to use as the divisor.
        :return: An instance of the :class:`Mod` class representing the modulus operation.

        Examples:

        - ``Datacube("test1") % Datacube("test2")``
        - ``Datacube("test1") % 5``
        """
        return Mod(self, other)

    def __rmod__(self, other: OperandType) -> Mod:
        """
        Allows the use of the '%' operator with the current operand on the right side.

        :param other: The operand to be divided by the current operand.
        :return: An instance of the :class:`Mod` class representing the modulus operation.

        Examples:

        - ``Datacube("test2") % Datacube("test1")``
        - ``5 % Datacube("test1")``
        """
        return Mod(other, self)

    def abs(self) -> Abs:
        """
        Computes the absolute value of the current operand.

        :return: An instance of the :class:`Abs` class representing the absolute value operation.

        Examples:

        - ``Datacube("test1").abs()``
        """
        return Abs(self)

    def __abs__(self) -> Abs:
        """
        Allows the use of the ``abs()`` function to compute the absolute value of the operand.

        :return: An instance of the :class:`Abs` class representing the absolute value operation.

        Examples:

        - ``abs(Datacube("test1"))``
        """
        return Abs(self)

    def round(self) -> Round:
        """
        Rounds the current operand to the nearest integer.

        :return: An instance of the :class:`Round` class representing the rounding operation.

        Examples:

        - ``Datacube("test1").round()``
        """
        return Round(self)

    def __round__(self) -> Round:
        """
        Allows the use of the ``round()`` function to round the operand to the nearest integer.

        :return: An instance of the :class:`Round` class representing the rounding operation.

        Examples:

        - ``round(Datacube("test1"))``
        """
        return Round(self)

    def floor(self) -> Floor:
        """
        Computes the floor of the current operand (rounds down to the nearest integer).

        :return: An instance of the :class:`Floor` class representing the floor operation.

        Examples:

        - ``Datacube("test1").floor()``
        """
        return Floor(self)

    def __floor__(self) -> Floor:
        """
        Allows the use of the :func:`math.floor` function to compute the floor of the operand.

        :return: An instance of the :class:`Floor` class representing the floor operation.

        Examples:

        - ``math.floor(Datacube("test1"))``
        """
        return Floor(self)

    def ceil(self) -> Ceil:
        """
        Computes the ceiling of the current operand (rounds up to the nearest integer).

        :return: An instance of the :class:`Ceil` class representing the ceiling operation.

        Examples:

        - ``Datacube("test1").ceil()``
        """
        return Ceil(self)

    def __ceil__(self) -> Ceil:
        """
        Allows the use of the :func:`math.ceil` function to compute the ceiling of the operand.

        :return: An instance of the :class:`Ceil` class representing the ceiling operation.

        Examples:

        - ``math.ceil(Datacube("test1"))``
        """
        return Ceil(self)

    # exponential

    def exp(self) -> Exp:
        """
        Computes the exponential (e^x) of the current operand.

        :return: An instance of the :class:`Exp` class representing the exponential operation.

        Examples:

        - ``Datacube("test1").exp()``
        """
        return Exp(self)

    def log(self) -> Log:
        """
        Computes the logarithm (base 10) of the current operand.

        :return: An instance of the :class:`Log` class representing the logarithm operation.

        Examples:

        - ``Datacube("test1").log()``
        """
        return Log(self)

    def ln(self) -> Ln:
        """
        Computes the natural logarithm (base e) of the current operand.

        :return: An instance of the :class:`Ln` class representing the natural logarithm operation.

        Examples:

        - ``Datacube("test1").ln()``
        """
        return Ln(self)

    def sqrt(self) -> Sqrt:
        """
        Computes the square root of the current operand.

        :return: An instance of the :class:`Sqrt` class representing the square root operation.

        Examples:

        - ``Datacube("test1").sqrt()``
        """
        return Sqrt(self)

    def pow(self, other: OperandType) -> Pow:
        """
        Raises the current operand to the power of another operand.

        :param other: The exponent to raise the current operand to.
        :return: An instance of the :class:`Pow` class representing the power operation.

        Examples:

        - ``Datacube("test1").pow(Datacube("test2"))``
        - ``Datacube("test1").pow(5)``
        """
        return Pow(self, other)

    def __pow__(self, other: OperandType) -> Pow:
        """
        Allows the use of the '**' operator to raise one operand to the power of another.

        :param other: The exponent to raise the current operand to.
        :return: An instance of the :class:`Pow` class representing the power operation.

        Examples:

        - ``Datacube("test1") ** Datacube("test2")``
        - ``Datacube("test1") ** 5``
        """
        return Pow(self, other)

    def __rpow__(self, other: OperandType) -> Pow:
        """
        Allows the use of the '**' operator to raise one operand to the power of another.

        :param other: The exponent to raise the current operand to.
        :return: An instance of the :class:`Pow` class representing the power operation.

        Examples:

        - ``Datacube("test1") ** Datacube("test2")``
        - ``5 ** Datacube("test1")``
        """
        return Pow(other, self)

    # trigonometric

    def sin(self) -> Sin:
        """
        Computes the sine of the current operand.

        :return: An instance of the :class:`Sin` class representing the sine operation.

        Examples:

        - ``Datacube("test1").sin()``
        """
        return Sin(self)

    def cos(self) -> Cos:
        """
        Computes the cosine of the current operand.

        :return: An instance of the :class:`Cos` class representing the cosine operation.

        Examples:

        - ``Datacube("test1").cos()``
        """
        return Cos(self)

    def tan(self) -> Tan:
        """
        Computes the tangent of the current operand.

        :return: An instance of the :class:`Tan` class representing the tangent operation.

        Examples:

        - ``Datacube("test1").tan()``
        """
        return Tan(self)

    def sinh(self) -> Sinh:
        """
        Computes the hyperbolic sine of the current operand.

        :return: An instance of the :class:`Sinh` class representing the hyperbolic sine operation.

        Examples:

        - ``Datacube("test1").sinh()``
        """
        return Sinh(self)

    def cosh(self) -> Cosh:
        """
        Computes the hyperbolic cosine of the current operand.

        :return: An instance of the :class:`Cosh` class representing the hyperbolic cosine operation.

        Examples:

        - ``Datacube("test1").cosh()``
        """
        return Cosh(self)

    def tanh(self) -> Tanh:
        """
        Computes the hyperbolic tangent of the current operand.

        :return: An instance of the :class:`Tanh` class representing the hyperbolic tangent operation.

        Examples:

        - ``Datacube("test1").tanh()``
        """
        return Tanh(self)

    def arcsin(self) -> ArcSin:
        """
        Computes the inverse sine (arcsine) of the current operand.

        :return: An instance of the :class:`ArcSin` class representing the arcsine operation.

        Examples:

        - ``Datacube("test1").arcsin()``
        """
        return ArcSin(self)

    def arccos(self) -> ArcCos:
        """
        Computes the inverse cosine (arccosine) of the current operand.

        :return: An instance of the :class:`ArcCos` class representing the arccosine operation.

        Examples:

        - ``Datacube("test1").arccos()``
        """
        return ArcCos(self)

    def arctan(self) -> ArcTan:
        """
        Computes the inverse tangent (arctangent) of the current operand.

        :return: An instance of the :class:`ArcTan` class representing the arctangent operation.

        Examples:

        - ``Datacube("test1").arctan()``
        """
        return ArcTan(self)

    def arctan2(self) -> ArcTan2:
        """
        Computes the two-argument inverse tangent (arctangent2) of the current operand.

        :return: An instance of the :class:`ArcTan2` class representing the arctangent2 operation.

        Examples:

        - ``Datacube("test1").arctan2(Datacube("test2"))``
        """
        return ArcTan2(self)

    # comparison

    def gt(self, other: OperandType) -> Gt:
        """
        Checks if the current operand is greater than another operand.

        :param other: The operand to compare against.
        :return: An instance of the :class:`Gt` class representing the greater-than comparison.

        Examples:

        - ``Datacube("test1").gt(Datacube("test2"))``
        - ``Datacube("test1").gt(10)``
        """
        return Gt(self, other)

    def __gt__(self, other: OperandType) -> Gt:
        """
        Allows the use of the '>' operator to compare two operands.

        :param other: The operand to compare against.
        :return: An instance of the :class:`Gt` class representing the greater-than comparison.

        Examples:

        - ``Datacube("test1") > Datacube("test2")``
        - ``Datacube("test1") > 10``
        """
        return Gt(self, other)

    def lt(self, other: OperandType) -> Lt:
        """
        Checks if the current operand is less than another operand.

        :param other: The operand to compare against.
        :return: An instance of the :class:`Lt` class representing the less-than comparison.

        Examples:

        - ``Datacube("test1").lt(Datacube("test2"))``
        - ``Datacube("test1").lt(10)``
        """
        return Lt(self, other)

    def __lt__(self, other: OperandType) -> Lt:
        """
        Allows the use of the '<' operator to compare two operands.

        :param other: The operand to compare against.
        :return: An instance of the :class:`Lt` class representing the less-than comparison.

        Examples:

        - ``Datacube("test1") < Datacube("test2")``
        - ``Datacube("test1") < 10``
        """
        return Lt(self, other)

    def ge(self, other: OperandType) -> Ge:
        """
        Checks if the current operand is greater than or equal to another operand.

        :param other: The operand to compare against.
        :return: An instance of the :class:`Ge` class representing the greater-than-or-equal-to comparison.

        Examples:

        - ``Datacube("test1").ge(Datacube("test2"))``
        - ``Datacube("test1").ge(10)``
        """
        return Ge(self, other)

    def __ge__(self, other: OperandType) -> Ge:
        """
        Allows the use of the '>=' operator to compare two operands.

        :param other: The operand to compare against.
        :return: An instance of the :class:`Ge` class representing the greater-than-or-equal-to comparison.

        Examples:

        - ``Datacube("test1") >= Datacube("test2")``
        - ``Datacube("test1") >= 10``
        """
        return Ge(self, other)

    def le(self, other: OperandType) -> Le:
        """
        Checks if the current operand is less than or equal to another operand.

        :param other: The operand to compare against.
        :return: An instance of the :class:`Le` class representing the less-than-or-equal-to comparison.

        Examples:

        - ``Datacube("test1").le(Datacube("test2"))``
        - ``Datacube("test1").le(10)``
        """
        return Le(self, other)

    def __le__(self, other: OperandType) -> Le:
        """
        Allows the use of the '<=' operator to compare two operands.

        :param other: The operand to compare against.
        :return: An instance of the :class:`Le` class representing the less-than-or-equal-to comparison.

        Examples:

        - ``Datacube("test1") <= Datacube("test2")``
        - ``Datacube("test1") <= 10``
        """
        return Le(self, other)

    def eq(self, other: OperandType) -> Eq:
        """
        Checks if the current operand is equal to another operand.

        :param other: The operand to compare against.
        :return: An instance of the :class:`Eq` class representing the equality comparison.

        Examples:

        - ``Datacube("test1").eq(Datacube("test2"))``
        - ``Datacube("test1").eq(10)``
        """
        return Eq(self, other)

    def __eq__(self, other: OperandType) -> Eq:
        """
        Allows the use of the '==' operator to compare two operands.

        :param other: The operand to compare against.
        :return: An instance of the :class:`Eq` class representing the equality comparison.

        Examples:

        - ``Datacube("test1") == Datacube("test2")``
        - ``Datacube("test1") == 10``
        """
        return Eq(self, other)

    def ne(self, other: OperandType) -> Ne:
        """
        Checks if the current operand is not equal to another operand.

        :param other: The operand to compare against.
        :return: An instance of the :class:`Ne` class representing the inequality comparison.

        Examples:

        - ``Datacube("test1").ne(Datacube("test2"))``
        - ``Datacube("test1").ne(10)``
        """
        return Ne(self, other)

    def __ne__(self, other: OperandType) -> Ne:
        """
        Allows the use of the '!=' operator to compare two operands.

        :param other: The operand to compare against.
        :return: An instance of the :class:`Ne` class representing the inequality comparison.

        Examples:
        - Datacube("test1") != Datacube("test2")
        - Datacube("test1") != 10
        """
        return Ne(self, other)

    # logical

    def logical_and(self, other: OperandType) -> And:
        """
        Performs a logical AND operation between the current operand and another operand.

        :param other: The operand to perform the AND operation with.
        :return: An instance of the :class:`And` class representing the logical AND operation.

        Examples:

        - ``Datacube("test1").logical_and(Datacube("test2"))``
        - ``Datacube("test1").logical_and(True)``
        """
        return And(self, other)

    def logical_or(self, other: OperandType) -> Or:
        """
        Performs a logical OR operation between the current operand and another operand.

        :param other: The operand to perform the OR operation with.
        :return: An instance of the :class:`Or` class representing the logical OR operation.

        Examples:

        - ``Datacube("test1").logical_or(Datacube("test2"))``
        - ``Datacube("test1").logical_or(False)``
        """
        return Or(self, other)

    def logical_xor(self, other: OperandType) -> Xor:
        """
        Performs a logical XOR operation between the current operand and another operand.

        :param other: The operand to perform the XOR operation with.
        :return: An instance of the :class:`Xor` class representing the logical XOR operation.

        Examples:

        - ``Datacube("test1").logical_xor(Datacube("test2"))``
        - ``Datacube("test1").logical_xor(True)``
        """
        return Xor(self, other)

    def logical_not(self) -> Not:
        """
        Performs a logical NOT operation on the current operand.

        :return: An instance of the :class:`Not` class representing the logical NOT operation.

        Examples:

        - ``Datacube("test1").logical_not()``
        """
        return Not(self)

    def overlay(self, other: OperandType) -> Overlay:
        """
        Performs an overlay operation, placing other operand "on top" of this operand:

        - wherever the second operand’s cell value is not zero and not null, the result value will be this value.
        - wherever the second operand’s cell value is zero or null, the first argument’s cell value will be taken.

        :param other: The operand to perform the overlay operation with.
        :return: An instance of the :class:`Overlay` class representing the overlay operation.

        Examples:

        - ``Datacube("test1").overlay(Datacube("test2"))``
        """
        return Overlay(self, other)

    def bit(self, pos: OperandType) -> Bit:
        """
        Take the bit in this operand's cell values at nonnegative position number pos,
        and put it as a Boolean value into a byte. Position counting starts with 0 and
        runs from least to most significant bit.

        :param pos: The position at which the bit value should be extracted
        :return: An instance of the :class:`Bit` class

        Examples:

        - ``Datacube("test1").bit(5)``
        """
        return Bit(self, pos)

    # multiband

    def band(self, band_name) -> Band:
        """
        Extract the given band ``band_name`` from this multiband object.

        :param band_name: The band name or position (0-based index)
        :return: An instance of the :class:`Band` class

        Examples:

        - ``Datacube("rgb").band("red")``
        - ``Datacube("rgb").band(0)``
        """
        return Band(self, band_name)

    def __getattr__(self, band_name) -> Band:
        """
        Extract the given band ``band_name`` from this multiband object with a '.' operator.

        :param band_name: The band name or position (0-based index)
        :return: An instance of the :class:`Band` class

        Examples:

        - ``Datacube("rgb").red``
        - ``Datacube("rgb").0``
        """
        return Band(self, band_name)

    # subsetting, extend, scale

    def subset(self, axes) -> Subset:
        """
        Extract a spatio-temporal subset from this object as specified by the list of ``axes``.

        :param axes: specifies a spatio-temporal subset as:

        1. a single :class:`Axis` object: ``Axis(axis_name, low, high?, crs?)``
        2. a tuple of multiple :class:`Axis` objects: ``(Axis(..), Axis(..))``
        3. a tuple specifying the axis subset in place: ``(axis_name, low, high?, crs?)``
        4. a tuple of axis subset tuples (see 3.): ``((axis_name, low, high?, crs?), (...), ..)``
        5. a list of :class:`Axis` objects: `[Axis(..), Axis(..), ..]`
        6. a list of axis subset tuples (see 3.): ``[(axis_name, low, high?, crs?), (...), ..]``

        :return: An instance of the :class:`Subset` class

        Examples (with ``cov = Datacube("testcube")``):

        1. ``cov.subset(Axis("X", 5.5, 10.5))``
        2. ``cov.subset(Axis("X", 5.5, 10.5), Axis("Y", 15))``
        3. ``cov.subset("X", 5.5, 10.5)``
        4. ``cov.subset(("X", 5.5, 10.5), ("Y", 15))``
        5. ``cov.subset([Axis("X", 5.5, 10.5), Axis("Y", 15)])``
        6. ``cov.subset([("X", 5.5, 10.5), ("Y", 15)])``
        """
        return Subset(self, axes)

    def __getitem__(self, axes) -> Subset:
        """
        Extract a spatio-temporal subset from this object as specified by the list of ``axes``
        with an index operator ``[..]``.

        :param axes: specifies a spatio-temporal subset as:

        1. a single :class:`Axis` object: ``Axis(axis_name, low, high?, crs?)``
        2. a tuple of multiple :class:`Axis` objects: ``(Axis(..), Axis(..))``
        3. a tuple specifying the axis subset in place: ``(axis_name, low, high?, crs?)``
        4. a tuple of axis subset tuples (see 3.): ``((axis_name, low, high?, crs?), (...), ..)``
        5. a list of :class:`Axis` objects: `[Axis(..), Axis(..), ..]`
        6. a list of axis subset tuples (see 3.): ``[(axis_name, low, high?, crs?), (...), ..]``

        :return: An instance of the :class:`Subset` class

        Examples (with ``cov = Datacube("testcube")``):

        1. ``cov[Axis("X", 5.5, 10.5)]``
        2. ``cov[(Axis("X", 5.5, 10.5), Axis("Y", 15)]``
        3. ``cov["X", 5.5, 10.5]``
        4. ``cov[("X", 5.5, 10.5), ("Y", 15)]``
        5. ``cov[[Axis("X", 5.5, 10.5), Axis("Y", 15)]]``
        6. ``cov[[("X", 5.5, 10.5), ("Y", 15)]]``
        """
        return Subset(self, axes)

    def extend(self, axes) -> Extend:
        """
        Extend this object to a new domain as specified by the list of ``axes``; new areas
        are filled in with null values.

        :param axes: specifies a spatio-temporal subset as:

        1. a single :class:`Axis` object: ``Axis(axis_name, low, high?, crs?)``
        2. a tuple of multiple :class:`Axis` objects: ``(Axis(..), Axis(..))``
        3. a tuple specifying the axis subset in place: ``(axis_name, low, high?, crs?)``
        4. a tuple of axis subset tuples (see 3.): ``((axis_name, low, high?, crs?), (...), ..)``
        5. a list of :class:`Axis` objects: `[Axis(..), Axis(..), ..]`
        6. a list of axis subset tuples (see 3.): ``[(axis_name, low, high?, crs?), (...), ..]``

        :return: An instance of the :class:`Subset` class

        Examples (with ``cov = Datacube("testcube")``):

        1. ``cov.extend(Axis("X", 5.5, 10.5))``
        2. ``cov.extend(Axis("X", 5.5, 10.5), Axis("Y", 15))``
        3. ``cov.extend("X", 5.5, 10.5)``
        4. ``cov.extend(("X", 5.5, 10.5), ("Y", 15))``
        5. ``cov.extend([Axis("X", 5.5, 10.5), Axis("Y", 15)])``
        6. ``cov.extend([("X", 5.5, 10.5), ("Y", 15)])``
        """
        return Extend(self, axes)

    def scale(self, grid_axes=None, another_coverage=None, single_factor=None, axis_factors=None) -> Scale:
        """
        Up or down-scale the current object. Exactly one of the parameters must be specified.

        :param grid_axes: rescale to the grid bounds specified for each axis
        :param another_coverage: rescale to the domain of another coverage operand
        :param single_factor: rescale all axes by the same scale factor;
            factor > 1 for scaling up, 0 < factor < 1 for scaling down
        :param axis_factors: rescale each axis by a specific factor;
            factor > 1 for scaling up, 0 < factor < 1 for scaling down

        :return: An instance of the :class:`Scale` class

        :raise: A :class:`WCPSClientException` in case of error in the provided arguments.

        Examples (with ``cov = Datacube("testcube")``):

        1. ``cov.scale(("X", 0, 100), ("Y", 0, 200))``
        2. ``cov.scale(Datacube("cov2"))``
        3. ``cov.scale(0.5)`` - downscale by 2x
        4. ``cov.scale([0.5, 2])`` - downscale the first axis by 2x, and upscale the second axis by 2x
        """
        nones = sum(1 for item in [grid_axes, another_coverage, single_factor, axis_factors]
                    if item is None)
        if nones != 3:
            raise WCPSClientException(f"scale expects exactly 1 parameter to be specified, "
                                      f"but {4 - nones} were specified.")
        if grid_axes is not None:
            return Scale(self).to_explicit_grid_domain(grid_axes)
        if another_coverage is not None:
            return Scale(self).to_grid_domain_of(another_coverage)
        if single_factor is not None:
            return Scale(self).by_factor(single_factor)
        if axis_factors is not None:
            return Scale(self).by_factor_per_axis(axis_factors)

        raise WCPSClientException("Invalid parameters specified to scale method.")

    # reproject

    def reproject(self, target_crs: str, interpolation_method: str = None,
                  axis_resolutions=None, axis_subsets=None, domain_of_coverage=None) -> Reproject:
        """
        Reproject the current object to a new CRS.

        :param target_crs: the new CRS, e.g. "EPSG:4326"
        :param interpolation_method: an optional interpolation method, one of the constants
            defined by :class:`ResampleAlg`, e.g. :const:`ResampleAlg.BILINEAR`
        :param axis_subsets: crop the result by the specified axis subsets (same syntax as for ``subset(axes)``)
        :param domain_of_coverage: crop the result to the geo domain of another coverage object

        Examples (with ``cov = Datacube("testcube")``):

        1. ``cov.reproject("EPSG:4326")``
        2. ``cov.reproject("EPSG:4326", interpolation_method=ResampleAlg.CUBIC)``
        3. ``cov.reproject("EPSG:4326", axis_resolutions=[0.5, 1.5])``
        4. ``cov.reproject("EPSG:4326", axis_subsets=[("Lat", 30.5, 60.5), ("Lon", 50.5, 70.5)])``
        5. ``cov.reproject("EPSG:4326", axis_resolutions=[0.5, 1.5], domain_of_coverage=Datacube("cov2"))``
        """
        ret = Reproject(self, target_crs, interpolation_method=interpolation_method)
        if axis_resolutions is not None:
            ret = ret.to_axis_resolutions(axis_resolutions)
        if axis_subsets is not None:
            ret = ret.subset_by_axes(axis_subsets)
        elif domain_of_coverage is not None:
            ret = ret.subset_by_coverage_domain(domain_of_coverage)
        return ret

    # casting

    def cast(self, target_type: CastType) -> Cast:
        """
        Cast the cell values of the current operand to a new ``target_type``.

        :param target_type: the new cell type of the result,
            one of the constants in :class:`CastType`, e.g. :const:`CastType.CHAR`.

        Examples:

        - ``cov.cast(Datacube("testcube"), CastType.FLOAT)``
        """
        return Cast(self, target_type)

    # aggregation

    def sum(self) -> Sum:
        """
        Computes the sum of the cell values of the current operand.

        :return: An instance of the :class:`Sum` class representing the sum operation.

        Examples:

        - ``Datacube("test1").sum()``
        """
        return Sum(self)

    def count(self) -> Count:
        """
        Counts the number of *true* values in the current boolean coverage operand.

        :return: An instance of the :class:`Count` class representing the count operation.

        Examples:

        - ``Datacube("test1").count()``
        """
        return Count(self)

    def avg(self) -> Avg:
        """
        Computes the average (mean) of the cell values of the current operand.

        :return: An instance of the :class:`Avg` class representing the average operation.

        Examples:

        - ``Datacube("test1").avg()``
        """
        return Avg(self)

    def min(self) -> Min:
        """
        Finds the minimum value among the elements of the current operand.

        :return: An instance of the :class:`Min` class representing the minimum operation.

        Examples:

        - ``Datacube("test1").min()``
        """
        return Min(self)

    def max(self) -> Max:
        """
        Finds the maximum value among the elements of the current operand.

        :return: An instance of the :class:`Max` class representing the maximum operation.

        Examples:

        - ``Datacube("test1").max()``
        """
        return Max(self)

    def all(self) -> All:
        """
        Checks if all elements in the current operand are true.

        :return: An instance of the :class:`All` class.

        Examples:

        - ``Datacube("test1").all()``
        """
        return All(self)

    def some(self) -> Some:
        """
        Checks if some elements in the current operand are true.

        :return: An instance of the :class:`Some` class.

        Examples:

        - ``Datacube("test1").some()``
        """
        return Some(self)

    def condense(self, condense_op: CondenseOp) -> Condense:
        """
        Condense the cell values of the current operand with the ``condense_op``.
        Iterator variables can be specified with the ``over()`` method, filtering of values
        with ``where()``, and the aggregation expression with ``using()``.

        :param condense_op: a condense operator, one of the constants defined in
            :class:`CondenseOp`, e.g. :const:`CondenseOp.PLUS`.
        :return: An instance of the :class:`Condense` class; at least ``over()`` and the
            ``using()`` methods must be called subsequently on the returned value.

        Examples:

        ```
        cov = Datacube("testcube")
        pt_var = AxisIter('$pt', 'time').of_grid_axis(cov)
        pt_ref = pt_var.ref()
        cov.condense(CondenseOp.PLUS).over(pt_var).where().where(cov["time", pt_ref] > 100).using(cov["time", pt_ref])
        ```
        """
        return Condense(self, condense_op)

    def encode(self, data_format: str = None, format_params: str = None) -> Encode:
        """
        Encode a coverage to some ``data_format``. The data format must be specified
        with the ``to(format)`` method if it isn't provided here.
        Optionally format parameters can be specified to customize the encoding process.

        :param data_format: the data format, e.g. ``"GTiff"``
        :param format_params: additional format parameters the influence the encoding

        Examples:

        ```
        Datacube("testcube").encode("GTiff").params("...")
        ```
        """
        return Encode(self, data_format=data_format, format_params=format_params)


# ----------------------------------------------------------------------------------

BoundType = Union[int, float, str, WCPSExpr]
"""A type representing axis bounds (in subsetting, extend, scale, etc)."""
ScalarType = Union[int, float, str, bool]
"""Scalar values can be of one of these types."""
OperandType = Union[WCPSExpr, ScalarType]
"""Type of operands of WCPS expressions."""
AxisTuple = Union[tuple[str, BoundType], tuple[str, BoundType, BoundType], tuple[str, BoundType, BoundType, str]]
"""Axis tuple types: (name, low), (name, low, high), or (name, low, high, crs)"""


class Datacube(WCPSExpr):
    """
    A reference to a datacube (coverage) object on a WCPS server.

    Example: ``Datacube("mycoverage")``.
    """

    def __init__(self, name: str):
        """
        :param name: the datacube (coverage) name.
        """
        super().__init__()
        self.name = name

    def __str__(self):
        return f'${self.name}'

    def __hash__(self):
        return hash(self.name)


class Scalar(WCPSExpr):
    """
    A wrapper for scalar values, e.g. ``5``, ``3.14``, ``"PNG"``.
    """

    def __init__(self, op: ScalarType):
        super().__init__()
        self.op = op

    def __str__(self):
        op_str = f'"{self.op}"' if isinstance(self.op, str) else str(self.op)
        return f'{super().__str__()}{op_str}'


class UnaryOp(WCPSExpr):
    """
    A base class for unary operators, e.g. logical NOT.
    """

    def __init__(self, op: WCPSExpr, operator: str):
        super().__init__(operands=[op])
        self.operator = operator

    def __str__(self):
        return f'{super().__str__()}({self.operator} {self.operands[0]})'


class BinaryOp(WCPSExpr):
    """
    A base class for binary operators, e.g. logical AND.
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr, operator: str):
        super().__init__(operands=[op1, op2])
        self.operator = operator

    def __str__(self):
        return f'{super().__str__()}({self.operands[0]} {self.operator} {self.operands[1]})'


class UnaryFunc(WCPSExpr):
    """
    A base class for unary functions, e.g. :class:`Abs`.
    """

    def __init__(self, op: WCPSExpr, func: str):
        super().__init__(operands=[op])
        self.func = func

    def __str__(self):
        return f'{super().__str__()}{self.func}({self.operands[0]})'


class BinaryFunc(WCPSExpr):
    """
    A base class for binary functions, e.g. :class:`Pow`.
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr, func: str):
        super().__init__(operands=[op1, op2])
        self.func = func

    def __str__(self):
        return f'{super().__str__()}{self.func}({self.operands[0]}, {self.operands[1]})'


# ---------------------------------------------------------------------------------
# arithmetic

class Add(BinaryOp):
    """
    Adds ``op1`` to ``op2``.

    Examples:

    - ``Add(Datacube("test1"), Datacube("test2"))``
    - ``Add(Datacube("test1"), 5)``
    - ``Add(5, Datacube("test1"))``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, '+')


class Sub(BinaryOp):
    """
    Subtracts ``op2`` from ``op1``.

    Examples:

    - ``Sub(Datacube("test1"), Datacube("test2"))``
    - ``Sub(Datacube("test1"), 5)``
    - ``Sub(5, Datacube("test1"))``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, '-')


class Mul(BinaryOp):
    """
    Multiplies ``op1`` by ``op2``.

    Examples:

    - ``Mul(Datacube("test1"), Datacube("test2"))``
    - ``Mul(Datacube("test1"), 5)``
    - ``Mul(5, Datacube("test1"))``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, '*')


class Div(BinaryOp):
    """
    Divides ``op1`` by ``op2``.

    Examples:

    - ``Div(Datacube("test1"), Datacube("test2"))``
    - ``Div(Datacube("test1"), 5)``
    - ``Div(5, Datacube("test1"))``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, '/')


class Mod(BinaryFunc):
    """
    Computes the modulus (remainder of the division) of ``op1`` by ``op2``.

    Examples:

    - ``Mod(Datacube("test1"), Datacube("test2"))``
    - ``Mod(Datacube("test1"), 5)``
    - ``Mod(5, Datacube("test1"))``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, 'mod')


class Abs(UnaryFunc):
    """
    Computes the absolute value of ``op``.

    Examples:

    - ``Abs(Datacube("test1"))``
    - ``Abs(-5)``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'abs')


class Round(UnaryFunc):
    """
    Rounds ``op`` to the nearest integer.

    Examples:

    - ``Round(Datacube("test1"))``
    - ``Round(-5.4)``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'round')


class Floor(UnaryFunc):
    """
    Computes the floor of ``op`` (rounds down to the nearest integer).

    Examples:

    - ``Floor(Datacube("test1"))``
    - ``Floor(-5.4)``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'floor')


class Ceil(UnaryFunc):
    """
    Computes the ceiling of ``op`` (rounds up to the nearest integer).

    Examples:

    - ``Ceil(Datacube("test1"))``
    - ``Ceil(-5.4)``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'ceil')


# ---------------------------------------------------------------------------------
# exponential

class Exp(UnaryFunc):
    """
    Computes the exponential (e^x) of ``op``.

    Examples:

    - ``Exp(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'exp')


class Log(UnaryFunc):
    """
    Computes the logarithm (base 10) of ``op``.

    Examples:

    - ``Log(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'log')


class Ln(UnaryFunc):
    """
    Computes the natural logarithm (base e) of ``op``.

    Examples:

    - ``Ln(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'ln')


class Sqrt(UnaryFunc):
    """
    Computes the square root of ``op``.

    Examples:

    - ``Sqrt(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'sqrt')


class Pow(BinaryFunc):
    """
    Raises ``op1`` to the power of ``op2``.

    Examples:

    - ``Pow(Datacube("test1"), Datacube("test2"))``
    - ``Pow(Datacube("test1"), 5)``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, 'pow')


# ---------------------------------------------------------------------------------
# trigonometric

class Sin(UnaryFunc):
    """
    Computes the sine of ``op``.

    Examples:

    - ``Sin(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'sin')


class Cos(UnaryFunc):
    """
    Computes the cosine of ``op``.

    Examples:

    - ``Cos(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'cos')


class Tan(UnaryFunc):
    """
    Computes the tangent of ``op``.

    Examples:

    - ``Tan(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'tan')


class Sinh(UnaryFunc):
    """
    Computes the hyperbolic sine of ``op``.

    Examples:

    - ``Sinh(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'sinh')


class Cosh(UnaryFunc):
    """
    Computes the hyperbolic cosine of ``op``.

    Examples:

    - ``Cosh(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'cosh')


class Tanh(UnaryFunc):
    """
    Computes the hyperbolic tangent of ``op``.

    Examples:

    - ``Tanh(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'tanh')


class ArcSin(UnaryFunc):
    """
    Computes the inverse sine of ``op``.

    Examples:

    - ``ArcSin(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'arcsin')


class ArcCos(UnaryFunc):
    """
    Computes the inverse cosine of ``op``.

    Examples:

    - ``ArcCos(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'arccos')


class ArcTan(UnaryFunc):
    """
    Computes the inverse tangent of ``op``.

    Examples:

    - ``ArcTan(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'arctan')


class ArcTan2(UnaryFunc):
    """
    Computes the two-argument inverse tangent of ``op``.

    Examples:

    - ``ArcTan2(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'arctan2')


# ---------------------------------------------------------------------------------
# comparison

class Gt(BinaryOp):
    """
    Checks if ``op1`` is greater than ``op2``.

    Examples:

    - ``Gt(Datacube("test1"), Datacube("test2"))``
    - ``Gt(Datacube("test1"), 10)``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, '>')


class Lt(BinaryOp):
    """
    Checks if ``op1`` is less than ``op2``.

    Examples:

    - ``Lt(Datacube("test1"), Datacube("test2"))``
    - ``Lt(Datacube("test1"), 10)``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, '<')


class Ge(BinaryOp):
    """
    Checks if ``op1`` is greater than or equal to ``op2``.

    Examples:

    - ``Ge(Datacube("test1"), Datacube("test2"))``
    - ``Ge(Datacube("test1"), 10)``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, '>=')


class Le(BinaryOp):
    """
    Checks if ``op1`` is less than or equal to ``op2``.

    Examples:

    - ``Le(Datacube("test1"), Datacube("test2"))``
    - ``Le(Datacube("test1"), 10)``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, '<=')


class Eq(BinaryOp):
    """
    Checks if ``op1`` is equal to ``op2``.

    Examples:

    - ``Eq(Datacube("test1"), Datacube("test2"))``
    - ``Eq(Datacube("test1"), 10)``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, '=')


class Ne(BinaryOp):
    """
    Checks if ``op1`` is not equal to ``op2``.

    Examples:

    - ``Ne(Datacube("test1"), Datacube("test2"))``
    - ``Ne(Datacube("test1"), 10)``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, '!=')


# ---------------------------------------------------------------------------------
# logical

class And(BinaryOp):
    """
    Performs a logical AND operation between ``op1`` and ``op2``.

    Examples:

    - ``And(Datacube("test1"), Datacube("test2"))``
    - ``And(Datacube("test1"), True)``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, 'and')


class Or(BinaryOp):
    """
    Performs a logical OR operation between ``op1`` and ``op2``.

    Examples:

    - ``Or(Datacube("test1"), Datacube("test2"))``
    - ``Or(Datacube("test1"), False)``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, 'or')


class Xor(BinaryOp):
    """
    Performs a logical XOR operation between ``op1`` and ``op2``.

    Examples:

    - ``Xor(Datacube("test1"), Datacube("test2"))``
    - ``Xor(Datacube("test1"), True)``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, 'xor')


class Not(UnaryOp):
    """
    Performs a logical Not operation on ``op``.

    Examples:

    - ``Not(Datacube("test1"))``
    - ``Not(True)``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'not')


class Overlay(BinaryOp):
    """
    Performs an overlay operation, placing ``op2`` "on top" of ``op1``:

    - wherever the cell value of ``op2`` is not zero and not null, the result value will be this value.
    - wherever the cell value of ``op2`` is zero or null, the cell value of ``op1`` will be taken.

    Examples:

    - ``Overlay(Datacube("test1"), Datacube("test2"))``
    """

    def __init__(self, op1: WCPSExpr, op2: WCPSExpr):
        super().__init__(op1, op2, 'overlay')


class Bit(BinaryFunc):
    """
    Take the bit in the cell values of ``op`` at nonnegative position number ``pos``,
    and put it as a Boolean value into a byte. Position counting starts with 0 and
    runs from least to most significant bit.

    :param pos: The position at which the bit value should be extracted

    Examples:

    - ``Bit(Datacube("test1", 5)``
    """

    def __init__(self, op: WCPSExpr, pos: WCPSExpr):
        super().__init__(op, pos, 'bit')


# ---------------------------------------------------------------------------------
# multiband

class Band(WCPSExpr):
    """
    Select a field (band, channel) from a multiband operand.
    """

    def __init__(self, op: WCPSExpr, field: [str | int]):
        super().__init__(operands=[op])
        self.field = field

    def __str__(self):
        return f'{super().__str__()}{self.operands[0]}.{self.field}'


class MultiBand(WCPSExpr):
    """
    Create a multiband value.
    :param bands: a dictionary of (band name, value), e.g. {"red": cov1, "blue": 2}
    """

    def __init__(self, bands: dict):
        super().__init__(operands=list(bands.values()))
        self.bands = bands

    def __str__(self):
        bands = [f'{k}: {v}' for k, v in self.bands.items()]
        return f'{super().__str__()}{{{'; '.join(bands)}}}'


# ---------------------------------------------------------------------------------
# subsetting, extend, scale

class Axis(WCPSExpr):
    """
    An axis subset, e.g. X:"EPSG:4326"(15.0:20.0)
    """

    MIN = '*'
    MAX = '*'

    def __init__(self, axis_name: str, low: BoundType, high: BoundType = None, crs: str = None):
        super().__init__(operands=[low, high])
        self.axis_name = axis_name
        self.low = low
        self.high = high
        self.crs = crs

    def __str__(self):
        ret = self.axis_name
        if self.crs is not None:
            ret += f':"{self.crs}"'
        operands = [str(op) for op in self.operands]
        operands = [op if op != '"*"' else '*' for op in operands]
        ret += f'({':'.join(operands)})'
        return ret

    @staticmethod
    def get_axis_list(axes: Union[Axis, slice, tuple[Axis], AxisTuple, tuple[AxisTuple],
    tuple[slice], list[Axis], list[AxisTuple]]) -> list[Axis]:
        """
        Normalizes ``axes`` into a list of Axis objects.
        :param axes: may be:

            - a single Axis, e.g. ``Axis("X", 0, 100.5, "EPSG:4326")``
            - a single slice, e.g. ``"X":1``, or ``"X":1:15.3``
            - a tuple of Axis objects, e.g. ``(Axis(..), Axis(..), ..)``
            - a single in-place axis tuple, e.g. ``("X", 0, 100.5, "EPSG:4326")``
            - a tuple of axis tuples, e.g. ``(("X", 0, 100.5), (..), ..)``
            - a tuple of slices, e.g. ``("X":1, "Y":0:100.5)``
            - a list of Axis objects, e.g. ``[Axis(..), Axis(..), ..]``
            - a list of axis tuples, e.g. ``[("X", 0, 100.5), (..), ..]``

        :raise: a :class:`WCPSClientException` in case ``axes`` is in invalid shape.
        """
        if isinstance(axes, Axis):
            # $c[Axis(..)]
            return [axes]
        if isinstance(axes, slice):
            return [Axis(axis_name=axes.start, low=axes.stop, high=axes.step)]
        if isinstance(axes, tuple):
            if isinstance(axes[0], Axis):
                # $c[Axis(..), Axis(..), ..]
                return list(axes)
            if isinstance(axes[0], str):
                # $c[("X", ..)]
                return [Axis(*axes)]
            if isinstance(axes[0], tuple):
                # $c[("X", ..), ("Y", ..), ..]
                return [Axis(*axis) for axis in axes]
            if isinstance(axes[0], slice):
                return [Axis(axis_name=axis.start, low=axis.stop, high=axis.step)
                        for axis in axes]
        if isinstance(axes, list):
            if isinstance(axes[0], Axis):
                # $c[Axis(..), Axis(..), ..]
                return axes
            if isinstance(axes[0], tuple):
                # $c[("X", ..), ("Y", ..), ..]
                return [Axis(*axis) for axis in axes]

        raise WCPSClientException("Invalid subsetting operation, expected one or more Axis objects, "
                                  "or tuples of the shape: (axis_name, low, high, crs)")


class Subset(WCPSExpr):
    """
    Select a spatio-temporal area from a coverage operand.
    """

    def __init__(self, op: WCPSExpr, axes):
        super().__init__(operands=[op] + Axis.get_axis_list(axes))

    def __str__(self):
        axis_subsets = [str(op) for op in self.operands[1:]]
        axis_subsets_str = ', '.join(axis_subsets)
        return f'{super().__str__()}{self.operands[0]}[{axis_subsets_str}]'


class Extend(WCPSExpr):
    """
    Enlarge a coverage with new areas set to null values.
    """

    def __init__(self, op: WCPSExpr, axes):
        super().__init__(operands=[op] + Axis.get_axis_list(axes))

    def __str__(self):
        axis_subsets = [str(op) for op in self.operands[1:]]
        axis_subsets_str = ', '.join(axis_subsets)
        return f'{super().__str__()}extend({self.operands[0]}, {{ {axis_subsets_str} }})'


class Scale(WCPSExpr):
    """
    Resamples the coverage values to fit a new domain. The target domain can be:

    1. An explicit grid domain for each axis with :meth:`to_explicit_grid_domain`: ::

            Scale(cov).to_explicit_grid_domain(
                [("X", 15, 30), ("Y", 20, 40)])

    2. A grid domain matching another coverage with :meth:`to_grid_domain_of`: ::

            Scale(cov).to_grid_domain_of(cov2)

    3. A scale factor equally applied to all axes with :meth:`by_factor`: ::

            Scale(cov).by_factor(0.5)

    3. A scale factor per axis with :meth:`by_factor_per_axis`: ::

            Scale(cov).by_factor_per_axis([0.5, 2])
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(operands=[op])
        self.axis_subsets = None
        self.another_coverage = None
        self.scale_factor = None
        self.scale_factors = None

    def __str__(self):
        ret = f'{super().__str__()}scale({self.operands[0]}, {{ '

        if self.axis_subsets is not None:
            axis_subsets = [str(op) for op in self.operands[1:]]
            ret += ', '.join(axis_subsets)
        elif self.another_coverage is not None:
            ret += f'imageCrsDomain({self.another_coverage})'
        elif self.scale_factor is not None:
            return f'{super().__str__()}scale({self.operands[0]}, {self.scale_factor})'
        elif self.scale_factors is not None:
            axis_subsets = [str(op) for op in self.operands[1:]]
            ret += ', '.join(axis_subsets)

        ret += ' })'
        return ret

    def to_explicit_grid_domain(self, grid_axes):
        """
        Scale to fit the grid domain specified by the ``grid_axes``.

        :param grid_axes: a list of :class:`Axis`
        """
        self.axis_subsets = Axis.get_axis_list(grid_axes)
        for axis in self.axis_subsets:
            self.add_operand(axis)
        return self

    def to_grid_domain_of(self, another_coverage: WCPSExpr):
        """
        Scale to fit the grid domain of ``another_coverage``.

        :param another_coverage: a coverage expression
        """
        self.another_coverage = another_coverage
        self.add_operand(another_coverage)
        return self

    def by_factor(self, scale_factor):
        """
        :param scale_factor: factor > 1 for scaling up, 0 < factor < 1 for scaling down
        """
        self.scale_factor = scale_factor
        self.add_operand(self.scale_factor)
        return self

    def by_factor_per_axis(self, scale_factors):
        """
        :param scale_factors: a list of Axis(name, factor)
        """
        self.scale_factors = Axis.get_axis_list(scale_factors)
        for axis in self.scale_factors:
            self.add_operand(axis)
            if axis.high is not None:
                raise WCPSClientException("When scaling by axis factors only a single factor "
                                          "per axis should be specified.")
            if axis.crs is not None:
                raise WCPSClientException("When scaling by axis factors a CRS must not be specified.")
        return self


# ---------------------------------------------------------------------------------
# reprojection

class ResampleAlg(StrEnum):
    """
    Possible interpolation methods for :class:`Reproject`.
    """
    NEAR = 'near'
    BILINEAR = 'bilinear'
    CUBIC = 'cubic'
    CUBICSPLINE = 'cubicspline'
    LANCZOS = 'lanczos'
    AVERAGE = 'average'
    MODE = 'mode'
    MAX = 'max'
    MIN = 'min'
    MED = 'med'
    Q1 = 'q1'
    Q3 = 'q3'


class Reproject(WCPSExpr):
    """
    Reproject a coverage to a different CRS.

    :param op: the coverage value to be reprojected.
    :param target_crs: the CRS to which ``op`` should be reprojected. It can be in one of these formats:

        - Full CRS URL, e.g. ``http://localhost:8080/rasdaman/def/crs/EPSG/0/4326`` (OGC standard format)
        - Shorthand CRS with authority, version and code, e.g. ``EPSG/0/4326``
        - Shorthand CRS with authority and code, e.g. ``EPSG:4326``

    :param interpolation_method: one of the :class:`ResampleAlg` constants,
        e.g. :const:`ResampleAlg.BILINEAR`.
    """

    def __init__(self, op: WCPSExpr, target_crs: str,
                 interpolation_method: ResampleAlg = None):
        super().__init__(operands=[op])
        self.target_crs: str = target_crs
        self.interpolation_method = interpolation_method
        self.axis_resolutions: Optional[list[Axis]] = None
        self.axis_subsets: Optional[list[Axis]] = None
        self.subset_domain: Optional[WCPSExpr] = None

    def __str__(self):
        ret = f'{super().__str__()}crsTransform({self.operands[0]}, "{self.target_crs}"'

        if self.interpolation_method is not None:
            ret += ', { ' + str(self.interpolation_method) + ' }'
        if self.axis_resolutions is not None:
            axis_subsets = [f'{axis.axis_name}:{axis.low}' for axis in self.axis_resolutions]
            axis_subsets_str = ', '.join(axis_subsets)
            ret += f', {{ {axis_subsets_str} }}'
        if self.axis_subsets is not None:
            axis_subsets = [str(axis) for axis in self.axis_subsets]
            axis_subsets_str = ', '.join(axis_subsets)
            ret += f', {{ {axis_subsets_str} }}'
        elif self.subset_domain is not None:
            ret += f', {{ domain({self.subset_domain}) }}'

        ret += ')'
        return ret

    def to_axis_resolutions(self, axis_resolutions) -> Reproject:
        """
        The reprojected result will be resampled to these resolutions.

        :param axis_resolutions: a list of :class:`Axis` objects with only
            the axis name and low bound (corresponding to a resolution) specified.

        :raise: :class:`WCPSClientException` if an axis object has the :attr:`Axis.high` or :attr:`Axis.crs` set.

        Example: ::

            cov1 = Datacube("cov1")
            Reproject(cov1, "EPSG:4326", ResampleAlg.AVERAGE)
                .to_axis_resolutions([("X", 1.5), ("Y", 2)])
        """
        self.axis_resolutions = Axis.get_axis_list(axis_resolutions)
        for axis in self.axis_resolutions:
            self.add_operand(axis)
            if axis.high is not None:
                raise WCPSClientException("When reprojecting to axis resolutions only a single "
                                          "resolution per axis should be specified.")
            if axis.crs is not None:
                raise WCPSClientException("When reprojecting to axis resolutions a CRS must not be specified.")
        return self

    def subset_by_axes(self, axis_subsets) -> Reproject:
        """
        The reprojected result will be cropped to the specified axis subsets.

        :param axis_subsets: a list of :class:`Axis` objects.

        :raise: :class:`WCPSClientException` if an axis object does not have the :attr:`Axis.high` set,
            or it has the :attr:`Axis.crs` set.

        Example: ::

            cov1 = Datacube("cov1")
            Reproject(cov1, "EPSG:4326")
                .subset_by_axes([("X", 1.5, 2.5), ("Y", 2, 4)])
        """
        self.axis_subsets = Axis.get_axis_list(axis_subsets)
        for axis in self.axis_subsets:
            self.add_operand(axis)
            if axis.high is None:
                raise WCPSClientException("When reprojecting, an axis subset must include "
                                          "both lower and upper bounds.")
            if axis.crs is not None:
                raise WCPSClientException("When reprojecting, an axis subset must not include a CRS.")
        return self

    def subset_by_coverage_domain(self, subset_domain) -> Reproject:
        """
        The reprojected result will be cropped to the domain of a coverage expression ``subset_domain``.

        :param subset_domain: a coverage expression

        Example: ::

            cov1 = Datacube("cov1")
            cov2 = Datacube("cov2")
            Reproject(cov1, "EPSG:4326")
                .subset_by_coverage_domain(cov2)
        """
        self.subset_domain = subset_domain
        self.add_operand(self.subset_domain)
        return self


# ---------------------------------------------------------------------------------
# casting

class CastType(StrEnum):
    """
    Possible cell types to which a value can be casted.
    """
    BOOLEAN = "boolean"
    CHAR = "char"
    UNSIGNED_CHAR = "unsigned char"
    SHORT = "short"
    UNSIGNED_SHORT = "unsigned short"
    INT = "int"
    UNSIGNED_INT = "unsigned int"
    LONG = "long"
    UNSIGNED_LONG = "unsigned long"
    FLOAT = "float"
    DOUBLE = "double"
    CINT16 = "cint16"
    CINT32 = "cint32"
    COMPLEX = "complex"
    COMPLEX2 = "complex2"


class Cast(WCPSExpr):
    """
    Cast a value to a new type. The type can be specified with the :meth:`to` method.

    :param op: the operand to be casted.
    :param target_type: must be one of the :class:`CastType` constants, e.g. :const:`CastType.CHAR`.

    Examples:

    - ``Cast(Datacube("test"), CastType.CHAR)``
    """

    def __init__(self, op, target_type: CastType = None):
        super().__init__(operands=[op])
        self.target_type = target_type

    def __str__(self):
        """
        :return: A WCPS query string corresponding to this expression.
        :raise: :class:`WCPSClientException` if no :attr:`target_type` has been set.
        """
        if self.target_type is None:
            raise WCPSClientException("No target type to which to cast the operand was provided.")
        return f'{super().__str__()}(({self.target_type}) {self.operands[0]})'

    def to(self, target_type: str) -> Cast:
        """
        Specify the type to which to cast this operand.
        :param target_type: must be one of the :class:`CastType` constants, e.g. :const:`CastType.CHAR`.
        """
        self.target_type = target_type
        return self


# ---------------------------------------------------------------------------------
# aggregation

class Sum(UnaryFunc):
    """
    Computes the sum of the cell values of the operand ``op``.

    Examples:

    - ``Sum(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'sum')


class Count(UnaryFunc):
    """
    Counts the number of *true* values in the boolean operand ``op``.

    Examples:

    - ``Count(Datacube("test1") > 5)``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'count')


class Avg(UnaryFunc):
    """
    Computes the average (mean) of the cell values of the operand ``op``.

    Examples:

    - ``Avg(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'avg')


class Min(UnaryFunc):
    """
    Returns the minimum value among the elements of the operand ``op``.

    Examples:

    - ``Min(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'min')


class Max(UnaryFunc):
    """
    Returns the maximum value among the elements of the operand ``op``.

    Examples:

    - ``Max(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'max')


class All(UnaryFunc):
    """
    Returns true if all elements in the operand ``op`` are true.

    Examples:

    - ``All(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'all')


class Some(UnaryFunc):
    """
    Returns true if some elements in the operand ``op`` are true.

    Examples:

    - ``Some(Datacube("test1"))``
    """

    def __init__(self, op: WCPSExpr):
        super().__init__(op, 'some')


class CondenseOp(StrEnum):
    """
    Possible general :class:`Condense` operators.
    """
    PLUS = '+'
    MULTIPLY = '*'
    MIN = 'min'
    MAX = 'max'
    AND = 'and'
    OR = 'or'
    OVERLAY = 'overlay'


class AxisIter(WCPSExpr):
    """
    An axis iterator expression set in a :meth:`Condense.over` or a :meth:`Coverage.over` methods.
    The iteration can be over an integer grid :meth:`interval`, :meth:`of_grid_axis` domain
    of a particular coverage, or :meth:`of_of_geo_axis` domain of a coverage.

    The :meth:`ref` method should be used to get a reference to an :class:`AxisIter` that
    can be used in expressions for the :meth:`Condense.where`, :meth:`Condense.using`, or
    :meth:`Coverage.values` clauses.

    :param var_name: unique iterator variable name.
    :param axis_name: an axis over which it iterates.

    Examples:

    - ``AxisIter('$x', 'X').interval(0, 100)`` - iterate from 0 to 100, inclusive
    - ``AxisIter('$pt', 'time').of_grid_axis(Datacube("timeseries"))``
    - ``AxisIter('$plat', 'Lat').of_geo_axis(Datacube("cov"))``
    """

    def __init__(self, var_name: str, axis_name: str):
        super().__init__()
        self.var_name = var_name
        """unique iterator variable name"""
        self.axis_name = axis_name
        """an axis over which it iterates"""
        self.low = None
        """optional lower iteration bound"""
        self.high = None
        """optional upper iteration bound"""
        self.grid_axis = None
        """iterator over a grid axis domain of a coverage"""
        self.geo_axis = None
        """iterator over a geo axis domain of a coverage"""

    def interval(self, low: int, high: int):
        """
        Iterate in the [low, high] interval.
        """
        self.low = low
        self.high = high
        return self

    def of_grid_axis(self, cov_expr: WCPSExpr):
        """
        Iterate over the grid axis domain of a coverage ``cov_expr``.
        """
        self.grid_axis = cov_expr
        self.add_operand(cov_expr)
        return self

    def of_geo_axis(self, cov_expr: WCPSExpr):
        """
        Iterate over the geo axis domain of a coverage ``cov_expr``.
        """
        self.geo_axis = cov_expr
        self.add_operand(cov_expr)
        return self

    def ref(self) -> AxisIterRef:
        """
        :return: a reference object that can be used in expressions set in the
            :meth:`Condense.where`, :meth:`Condense.using`, or :meth:`Coverage.values` methods.
        """
        return AxisIterRef(self)

    def __str__(self):
        iter_spec = ''
        if self.low is not None and self.high is not None:
            iter_spec = f'{self.low}:{self.high}'
        elif self.grid_axis is not None:
            iter_spec = f'imageCrsDomain({self.grid_axis}, {self.axis_name})'
        elif self.geo_axis is not None:
            iter_spec = f'domain({self.geo_axis}, {self.axis_name})'
        return f'${self.var_name} {self.axis_name}({iter_spec})'


class AxisIterRef(WCPSExpr):
    """
    Reference to an :class:`AxisIter` object, to be used in expressions set in the
        :meth:`Condense.where`, :meth:`Condense.using`, or :meth:`Coverage.values` methods.
    """

    def __init__(self, iter_var: AxisIter):
        super().__init__()
        self.iter_var = iter_var

    def __str__(self):
        return f'${self.iter_var.var_name}'


class Condense(WCPSExpr):
    """
    A general coverage condense (aggregation) operation. It aggregates values :meth:`over`
    an iteration domain formed of a list of :class:`AxisIter`, with a condenser operation
    (one of ``+``, ``*``, ``max``, ``min``, ``and``, or ``or``). For each coordinate in
    the iteration domain defined by the over clause, the :meth:`using` expression is
    evaluated and added to the final aggregated result; the optional :meth:`where` expression
    allows to filter values from the aggregation.

    It corresponds to a WCPS expression of the following form: ::

        condense op
        over $iterVar axis(lo:hi), ...
        [ where boolScalarExpr ]
        using scalarExpr

    Typically, the iterator variable iterates through a grid domain (:meth:`AxisIter.interval` or
    :meth:`AxisIter.of_grid_axis`). However, iteration over a geo domain is also supported
    with :meth:`AxisIter.of_geo_axis`.

    :param condense_op: one of the :class:`CondenseOp` constants, e.g. :const:`CondenseOp.PLUS`
    :param over: a list of axis iterators
    :param using: an expression that aggregates into the final value
    :param where: an optional expression to filter which expression values are evaluated

    For example, to sum the values of a coverage ``mycov`` (same as using the :class:`Sum` shorthand): ::

        cov = Datacube("mycov")
        pt_var = AxisIter('$pt', 'time').of_grid_axis(cov)
        pt_ref = pt_var.ref()
        Condense(CondenseOp.PLUS)
            .over(pt_var)
            .using(cov1[('time', pt_ref)])
    """

    def __init__(self, condense_op: CondenseOp, over: list = None,
                 using: WCPSExpr = None, where: WCPSExpr = None):
        operands = [where, using]
        if over is not None:
            operands += over
        super().__init__(operands=operands)
        self.condense_op = condense_op
        """
        One of the :class:`CondenseOp` constants, e.g. :const:`CondenseOp.PLUS`
        """
        self.iter_vars = over if over is not None else []
        """
        A list of :class:`AxisIter` forming the iteration domain for aggregation.
        """
        self.using_clause = using
        self.where_where = where

    def __str__(self):
        """
        :return: A WCPS query string corresponding to this expression.
        :raise: :class:`WCPSClientException` if no iterator variables or a using expression have been set.
        """
        self._validate()
        over = ', '.join(str(axis_iter) for axis_iter in self.iter_vars)
        ret = f'{super().__str__()}(condense {self.condense_op} over {over}'
        if self.where_where is not None:
            ret += f' where {self.where_where}'
        ret += f' using {self.using_clause})'
        return ret

    def _validate(self):
        """
        :meta private:
        """
        if len(self.iter_vars) == 0:
            raise WCPSClientException("An OVER clause is mandatory in a CONDENSE operation, none was specified.")
        if self.using_clause is None:
            raise WCPSClientException("A USING clause is mandatory in a CONDENSE operation, none was specified.")

    def over(self, iter_var: AxisIter) -> Condense:
        """
        Add an iterator variable to a `Condense` or a `Coverage` operand.
        Calling this method on another object type will raise a `WCPSClientException`.

        :param iter_var: an iterator variable
        :return: the same object with the iter_var appended to its iterator variables list

        Examples: ::

            cov = Datacube("testcube")
            pt_var = AxisIter('$pt', 'time').of_grid_axis(cov)
            px_var = AxisIter('$px', 'X').interval(0, 100)
            cov.condense(CondenseOp.PLUS).over(pt_var).over(px_var)
        """
        self.iter_vars.append(iter_var)
        self.add_operand(iter_var)
        return self

    def using(self, using: WCPSExpr) -> Condense:
        """
        Specify an aggregation expression, evaluated for each point in the :meth:`over`
        domain and aggregated into the final result with the :attr:`condense_op`.
        """
        self.using_clause = using
        self.add_operand(using)
        return self

    def where(self, where: WCPSExpr) -> Condense:
        """
        Specify a filtering expression, evaluated for each point in the :meth:`over`
        domain. If its result is false at that point then the :meth:`using` expression
        is not executed.
        """
        self.where_where = where
        self.add_operand(where)
        return self


class Coverage(WCPSExpr):
    """
    A general coverage constructor operation. It allows to create a coverage :meth:`over` a
    spatio-temporal domain, where for each coordinate in the domain the value is
    dynamically calculated from a :meth:`values` expression which potentially references
    the iterator variables set in the :meth:`over` method. It corresponds to a WCPS
    expression of the following form: ::

        coverage covName
        over $iterVar axis(lo:hi), ...
        values scalarExpr

    Typically, the iterator variable iterates through a grid domain (:meth:`AxisIter.interval` or
    :meth:`AxisIter.of_grid_axis`). However, iteration over a geo domain is also supported
    with :meth:`AxisIter.of_geo_axis`.

    :param name: a name for the new coverage
    :param over: a list of axis iterators
    :param values_clause: an expression evaluating to a value for each point in the over domain

    For example, to create a 2D geo-referenced coverage with
    Lat and Lon axes, based on an existing geo-referenced coverage ``mycov``: ::

        cov = Datacube("mycov")
        plat_var = AxisIter('$pLat', 'Lat')
                        .of_geo_axis(cov['Lat', -30, -28.5])
        plon_var = AxisIter('$pLon', 'Lon')
                        .of_geo_axis(cov['Lon', 111.975, 113.475])
        Coverage("copy_of_mycov")
            .over(plat_var).over(plon_var)
            .values(cov1[('Lat', plat_var.ref()),
                         ('Lon', plon_var.ref())]))
    """

    def __init__(self, name: str, over: list = None, values_clause: WCPSExpr = None):
        operands = [values_clause]
        if over is not None:
            operands += over
        super().__init__(operands=operands)
        self.name = name
        """
        Name of the created coverage (datacube).
        """
        self.iter_vars = over if over is not None else []
        """
        A list of :class:`AxisIter` forming the created coverage domain.
        """
        self.values_clause = values_clause
        """
        An expression evaluated for each point in the coverage domain.
        """

    def __str__(self):
        """
        :return: A WCPS query string corresponding to this expression.
        :raise: :class:`WCPSClientException` if no iterator variables or a values expression have been set.
        """
        self._validate()
        ret = super().__str__()
        over = ', '.join(str(axis_iter) for axis_iter in self.iter_vars)
        ret += f'(coverage {self.name} over {over} values {self.values_clause})'
        return ret

    def _validate(self):
        """
        :meta private:
        """
        if len(self.iter_vars) == 0:
            raise WCPSClientException("An OVER clause is mandatory in a COVERAGE operation, none was specified.")
        if self.values_clause is None:
            raise WCPSClientException("A VALUES clause is mandatory in a COVERAGE operation, none was specified.")

    def over(self, iter_var: AxisIter) -> Coverage:
        """
        Add an iterator variable to the coverage constructor.

        :param iter_var: an iterator variable
        :return: the same object with the ``iter_var`` appended to its iterator variables list

        Examples: ::

            cov = Datacube("testcube")
            pt_var = AxisIter('$pt', 'time').of_grid_axis(cov)
            px_var = AxisIter('$px', 'X').interval(0, 100)
            cov.condense(CondenseOp.PLUS).over(pt_var).over(px_var)
        """
        self.iter_vars.append(iter_var)
        self.add_operand(iter_var)
        return self

    def values(self, values_clause) -> Coverage:
        """
        Specify a VALUES expression, evaluated for each point in the :meth:`over` domain.
        """
        self.values_clause = values_clause
        self.add_operand(values_clause)
        return self


# ---------------------------------------------------------------------------------
# switch

class Switch(WCPSExpr):
    """
    Perform a switch operation for conditional evaluation. This produces a WCPS query
    fragment of the format: ::

        switch
        case boolCovExpr return covExpr
        case boolCovExpr return covExpr
        ...
        default return covExpr

    Use pairs of :meth:`case` and :meth:`then` method calls to specify
    case/return branches. Finally make a :meth:`default` method call to specify
    a default case executed when none of the case conditions are satisfied.

    Examples: ::

        cov1 = Datacube("cube1")
        cov2 = Datacube("cube2")
        Switch().case(cov1 > 5).then(cov2).default(cov1)
    """

    def __init__(self):
        super().__init__()
        self.case_expr: list[WCPSExpr] = []
        self.then_expr: list[WCPSExpr] = []
        self.default_expr = None

    def __str__(self):
        """
        :return: A WCPS query string corresponding to this expression.
        :raise: :class:`WCPSClientException` if no case or default expressions have been specified.
        """
        if len(self.then_expr) == 0:
            raise WCPSClientException("No case expressions have been specified for the switch expression.")
        if self.default_expr is None:
            raise WCPSClientException("No default expression has been specified for the switch expression.")
        ret = f'{super().__str__()}(switch'
        for case_expr, then_expr in zip(self.case_expr, self.then_expr):
            ret += f' case {case_expr} return {then_expr}'
        ret += f' default return {self.default_expr})'
        return ret

    def case(self, case_expr: WCPSExpr) -> Switch:
        """
        Specify a condition expression.
        :param case_expr: the boolean case expression.
        :raise: :class:`WCPSClientException` if there is a mismatch between the number of case/then expressions.
        """
        if len(self.case_expr) != len(self.then_expr):
            raise WCPSClientException("A switch consists of alternating if_case/then expressions, "
                                      "finalized with a default expression.")
        self.add_operand(case_expr)
        self.case_expr.append(case_expr)
        return self

    def then(self, then_expr: WCPSExpr) -> Switch:
        """
        Specify an expression to be evaluated when the previously set ``case`` expression is true.

        :param then_expr: the then expression.

        :raise: :class:`WCPSClientException` if there is a mismatch between
            the number of case/then expressions.
        """
        if len(self.case_expr) - 1 != len(self.then_expr):
            raise WCPSClientException("A switch consists of alternating if_case/then expressions, "
                                      "finalized with a default expression.")
        self.add_operand(then_expr)
        self.then_expr.append(then_expr)
        return self

    def default(self, default_expr: WCPSExpr) -> Switch:
        """
        Specify a default expressions executed when none of the case conditions are satisfied.

        :param default_expr: the default expression.

        :raise: :class:`WCPSClientException` if no case expressions have been specified,
            or if a default expression has already been set.
        """
        if len(self.then_expr) == 0:
            raise WCPSClientException("In a switch first the if_case/then expressions must be specified, "
                                      "followed by the default expression.")
        if self.default_expr is not None:
            raise WCPSClientException("A default expression has already been specified for this "
                                      "switch expression.")
        self.default_expr = default_expr
        self.add_operand(default_expr)
        return self


# ---------------------------------------------------------------------------------
# data encode/decode

class Encode(WCPSExpr):
    """
    Encode a coverage to some data format. The data format must be specified
    with the :meth:`to` method if it isn't provided here. Format parameters can
    be specified with the :meth:`params` method.

    Examples:

    - ``Encode(Datacube("test")).to("GTiff")``
    - ``Encode(Datacube("test"), "GTiff")``
    - ``Encode(Datacube("test"), "GTiff", "...")``
    """

    def __init__(self, op: WCPSExpr, data_format: str = None, format_params: str = None):
        """
        :param op: the coverage expression to encode.
        :param data_format: the data format, e.g. "GTiff"
        :param format_params: additional format parameters the influence the encoding
        """
        super().__init__(operands=[op])
        self.data_format = data_format
        self.format_params = format_params

    def to(self, data_format: str) -> Encode:
        """
        Set the encoding data format.

        :param data_format: the data format, e.g. "GTiff"
        """
        self.data_format = data_format
        return self

    def params(self, format_params: str) -> Encode:
        """
        Set the encoding format parameters.

        :param format_params: additional format parameters the influence the encoding
        """
        self.format_params = format_params
        return self

    def __str__(self):
        if self.data_format is None:
            raise WCPSClientException("No target format to which to encode the operand was provided.")
        ret = f'{super().__str__()}encode({self.operands[0]}, "{self.data_format}"'
        if self.format_params is not None:
            ret += f', "{self.format_params}"'
        ret += ')'
        return ret


class WCPSClientException(Exception):
    """
    An exception thrown by this library.
    """
