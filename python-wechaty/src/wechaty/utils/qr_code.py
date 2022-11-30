# -*- coding: utf-8 -*-
"""
qr_code helper utils
"""
from typing import Any
import qrcode


def qr_terminal(data: str, version: Any = None) -> None:
    """print the qrcode to the terminal using the python-qrcode tools

    https://github.com/lincolnloop/python-qrcode

    Args:
        data (str): the data of the qrcode
        version (Any, optional): the qrcode version. Defaults to None.
    """
    qr = qrcode.QRCode(version, border=2)
    qr.add_data(data)
    if version:
        qr.make()
    else:
        qr.make(fit=True)
    qr.print_ascii(invert=True)
