"""Validation helpers for BDD tests for isshub entities."""

from typing import Any, List, Optional, Tuple, Type

import pytest
from factory import Factory

from isshub.domain.utils.entity import BaseModel


ValuesValidation = List[Tuple[Any, Optional[Type[Exception]]]]

integer_only: ValuesValidation = [
    ("foo", TypeError),
    (-123, ValueError),
    (-1.5, TypeError),
    (-1, ValueError),
    (-0.001, TypeError),
    (0.001, TypeError),
    (1, None),
    (1.5, TypeError),
    (123, None),
]

no_zero: ValuesValidation = [(0, ValueError)]

positive_integer_only: ValuesValidation = integer_only + no_zero

string_only: ValuesValidation = [("foo", None), (1, TypeError), (-0.1, TypeError)]


def check_field(obj: BaseModel, field_name: str) -> None:
    """Assert that the given `obj` has an attribute named `field_name`.

    Parameters
    ----------
    obj : BaseModel
        The object to test
    field_name : str
        The field name to search for

    Raises
    ------
    AssertionError
        If `obj` does not contain any attribute named `field_name`

    """
    assert hasattr(obj, field_name)


def check_field_value(
    factory: Type[Factory],
    field_name: str,
    value: Any,
    exception: Optional[Type[Exception]],
    **factory_kwargs: Any,
) -> None:
    """Assert that an object can or cannot have a specific value for a specific field.

    Parameters
    ----------
    factory : Type[Factory]
        The factory to use to create the object to test
    field_name : str
        The name of the field to check
    value : Any
        The value to set to the field
    exception :  Optional[Type[Exception]]
        The exception expected to be raised. If ``None``, no exception is expected to be raised.
    factory_kwargs : Any
        Any kwargs to pass to the factory to create the object

    Raises
    ------
    AssertionError
        If an exception is raised when setting the `value` to the field when creating or updating
        an object (when calling ``validate`` in case of updating), and `exception` is ``None``,
        or if no exception is raised if `exception` is not ``None`` (or the wrong exception).

    """
    if exception:
        # When creating an instance
        with pytest.raises(exception):
            factory(**{field_name: value}, **factory_kwargs)
        # When updating the value
        obj = factory(**factory_kwargs)
        setattr(obj, field_name, value)
        with pytest.raises(exception):
            obj.validate()
    else:
        # When creating an instance
        factory(**{field_name: value}, **factory_kwargs)
        # When updating the value
        obj = factory(**factory_kwargs)
        setattr(obj, field_name, value)
        obj.validate()


def check_field_not_nullable(
    factory: Type[Factory], field_name: str, **factory_kwargs: Any
) -> None:
    """Assert that an object cannot have a specific field set to ``None``.

    Parameters
    ----------
    factory : Type[Factory]
        The factory to use to create the object to test
    field_name : str
        The name of the field to check
    factory_kwargs : Any
        Any kwargs to pass to the factory to create the object

    Raises
    ------
    AssertionError
        If the field can be set to ``None`` while creating or updating an object (when calling
        ``validate`` in case of updating)

    """
    # When creating an instance
    with pytest.raises(TypeError):
        factory(**{field_name: None}, **factory_kwargs)

    # When updating the value
    obj = factory(**factory_kwargs)
    setattr(obj, field_name, None)
    with pytest.raises(TypeError):
        obj.validate()


def check_field_nullable(
    factory: Type[Factory], field_name: str, **factory_kwargs: Any
) -> None:
    """Assert that an object can have a specific field set to ``None``.

    Parameters
    ----------
    factory : Type[Factory]
        The factory to use to create the object to test
    field_name : str
        The name of the field to check
    factory_kwargs : Any
        Any kwargs to pass to the factory to create the object

    Raises
    ------
    AssertionError
        If the field cannot be set to ``None`` while creating or updating an object (when calling
        ``validate`` in case of updating)

    """
    # When creating an instance
    try:
        factory(**{field_name: None}, **factory_kwargs)
    except TypeError:
        pytest.fail(f"DID RAISE {TypeError}")

    # When updating the value
    obj = factory(**factory_kwargs)
    setattr(obj, field_name, None)
    try:
        obj.validate()
    except TypeError:
        pytest.fail(f"DID RAISE {TypeError}")
