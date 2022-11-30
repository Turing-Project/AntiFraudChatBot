"""
Unit test
"""
import pytest
from wechaty_puppet import WechatyPuppetConfigurationError
from wechaty import Wechaty, WechatyOptions 

def test_constructor():
    with pytest.raises(WechatyPuppetConfigurationError):
        bot = Wechaty()

    options = WechatyOptions(token='fake-token', endpoint='127.0.0.1:8080')
    bot = Wechaty(options=options)
    
    assert bot.puppet.options.token == 'fake-token'
    assert bot.puppet.options.end_point == '127.0.0.1:8080'
