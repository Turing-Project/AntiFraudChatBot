"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright Wechaty

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations
from datetime import datetime


def timestamp_to_date(timestamp: float) -> datetime:
    """convert different timestamp precision to python format

    Python2.7: https://docs.python.org/2.7/library/datetime.html#datetime.datetime
        Python3+ ：https://docs.python.org/3.7/library/datetime.html#datetime.datetime
        for datetime.fromtimestamp. It’s common for this to be restricted to years from 1970 through 2038. 
        2145888000 is 2038-01-01 00:00:00 UTC for second
        2145888000 is 1970-01-26 04:04:48 UTC for millisecond

    Args:
        timestamp (float): from different source, so, has different
            timestamp precision
    """
    if timestamp > 2145888000:
        timestamp = timestamp / 1000
    return datetime.fromtimestamp(timestamp)
