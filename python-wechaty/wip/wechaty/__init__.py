"""doc"""
from __future__ import annotations

from typing import (
    Optional,
)


class Wechaty:
    """Working In Progress"""

    def __init__(self) -> None:
        """WIP Warning"""
        print('''

Dear Python Wechaty user,

    Thank you very much for using Python Wechaty!

    Wechaty is a RPA SDK for Wechat Individual Account that can help you create a chatbot in 6 lines of Python.
    Our GitHub is at https://github.com/wechaty/python-wechaty

    Today, we are under the process of translating the TypeScript Wechaty to Python Wechaty, please see issue #11 "From TypeScript to Python in Wechaty Way - Internal Modules" at https://github.com/wechaty/python-wechaty/issues/11

    To stay tuned, watch our repository now!

    Please also feel free to leave comments in our issues if you want to contribute, testers, coders, and doc writers are all welcome!

Huan
Author of Wechaty
Mar 15, 2020

        ''')

    def version(self) -> str:
        """version"""
        type(self)
        return '0.0.0'

    def ding(
            self: Wechaty,
            data: Optional[str],
    ) -> None:
        """ding"""
        type(self)
        type(data)


__all__ = [
    'Wechaty',
]
