"""add type check utils"""
from typing import Union, Optional


def type_check(obj: object, type_name: str) -> bool:
    """
    circulation dependency problems can be resolved by TYPE_CHECKING,
    but this can not resolve NO type linting problems. eg:
        if isinstance(msg, Contact):
            pass
    in this problem, program don't import Contact at running time. So, it will
        throw a Exception, which will not be threw
    :param obj:
    :param type_name:
    :return:
    """
    if hasattr(obj, '__class__') and hasattr(obj.__class__, '__name__'):
        return obj.__class__.__name__ == type_name
    return False


def default_str(obj: Union[str, Optional[str]]) -> str:
    if obj:
        return obj
    return ''
