# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io

import pint

from . import defs
from . import text

_ureg = pint.UnitRegistry()

_SYNC = b"""
Checksum	&
"""

_BLOCK = b"""PID	0xA042
FW	153
SER#	HQ1949I8BGA
V	12110
I	0
VPV	13590
PPV	0
CS	3
MPPT	2
ERR	0
LOAD	ON
IL	0
H19	43
H20	2
H21	34
H22	1
H23	4
HSDS	7
Checksum	&
"""


def test_parse():
    block = (_SYNC + _BLOCK).replace(b'\n', b'\r\n')
    src = io.BytesIO(block)
    parser = text.parse(src)
    want = {
        'PID': '0xA042',
        'FW': '1.53',
        'SER#': 'HQ1949I8BGA',
        'V': 12.110 * _ureg.volt,
        'I': 0 * _ureg.amp,
        'VPV': 13.590 * _ureg.volt,
        'PPV': 0 * _ureg.watt,
        'CS': defs.State.BULK,
        'MPPT': defs.MPPTMode.ACTIVE,
        'ERR': defs.Err.NO_ERROR,
        'LOAD': defs.Load.ON,
        'IL': 0 * _ureg.amp,
        'H19': 430 * _ureg.watt * _ureg.hour,
        'H20': 20 * _ureg.watt * _ureg.hour,
        'H21': 34 * _ureg.watt,
        'H22': 10 * _ureg.watt * _ureg.hour,
        'H23': 4 * _ureg.watt,
        'HSDS': 7 * _ureg.day,
    }
    got = next(parser)
    assert got == want
