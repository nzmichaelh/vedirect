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
"""Protocol definitions including fields, enums, and types."""

import collections
import enum

import pint

_ureg = pint.UnitRegistry()


class State(enum.IntEnum):
    """State is the state of operation. Sent in the `CS` field."""
    # Off
    OFF = 0
    # Low power
    LOW_POWER = 1
    # Fault
    FAULT = 2
    # Bulk
    BULK = 3
    # Absorption
    ABSORPTION = 4
    # Float
    FLOAT = 5
    # Storage
    STORAGE = 6
    # Equalize (manual)
    EQUALIZE_MANUAL = 7
    # Inverting
    INVERTING = 9
    # Power supply
    POWER_SUPPLY = 11
    # Starting-up
    STARTING_UP = 245
    # Repeated absorption
    REPEATED_ABSORPTION = 246
    # Auto equalize / Recondition
    AUTO_EQUALIZE_RECONDITION = 247
    # BatterySafe
    BATTERYSAFE = 248
    # External Control
    EXTERNAL_CONTROL = 252


class MPPTMode(enum.IntEnum):
    """MPPTMode is the state of the tracker. Sent in the `MPPT` field."""
    # Off
    OFF = 0
    # Voltage or current limited
    LIMITED = 1
    # MPPT Tracker active
    ACTIVE = 2


class Err(enum.IntEnum):
    """Err is the error code of the device. Sent in the `ERR` field."""
    # No error
    NO_ERROR = 0
    # Battery voltage too high
    BATTERY_VOLTAGE_TOO_HIGH = 2
    # Charger temperature too high
    CHARGER_TEMPERATURE_TOO_HIGH = 17
    # Charger over current
    CHARGER_OVER_CURRENT = 18
    # Charger current reversed
    CHARGER_CURRENT_REVERSED = 19
    # Bulk time limit exceeded
    BULK_TIME_LIMIT_EXCEEDED = 20
    # Current sensor issue (sensor bias/sensor broken)
    CURRENT_SENSOR_ISSUE = 21
    # Terminals overheated
    TERMINALS_OVERHEATED = 26
    # Input voltage too high (solar panel)
    INPUT_VOLTAGE_TOO_HIGH_SOLAR_PANEL = 33
    # Input current too high (solar panel)
    INPUT_CURRENT_TOO_HIGH_SOLAR_PANEL = 34
    # Input shutdown (due to excessive battery voltage)
    INPUT_SHUTDOWN = 38
    # Factory calibration data lost
    FACTORY_CALIBRATION_DATA_LOST = 116
    # Invalid/incompatible firmware
    INVALID_OR_INCOMPATIBLE_FIRMWARE = 117
    # User settings invalid
    USER_SETTINGS_INVALID = 119


class Load(enum.IntEnum):
    """Load is the state of the output to the load.

    Sent in the `LOAD` field."""
    # Off
    OFF = 0
    # On
    ON = 1


# Kinds maps the common units to the appropriate scale and unit.
_KINDS = {
    'mV': 1e-3 * _ureg.volt,
    'mA': 1e-3 * _ureg.amp,
    'W': 1 * _ureg.watt,
    '0.01 kWh': 1e-2 * 1000 * _ureg.watt * _ureg.hour,
    '0.01 V': 1e-2 * _ureg.volt,
    '0.1 A': 1e-1 * _ureg.amp,
    'Seconds': _ureg.second,
    'HSDS': 1 * _ureg.day,
    'ERR': Err,
    'CS': State,
    'MPPT': MPPTMode,
    'LOAD': Load,
    'SER#': str,
    'PID': str,
    'FW': str,
}


class Field(collections.namedtuple('Field', 'label unit description')):
    """Field describes a single field."""
    def kind(self):
        return _KINDS.get(self.unit, _KINDS.get(self.label, None))


V = Field('V', 'mV', 'Main or channel 1 (battery) voltage')
V2 = Field('V2', 'mV', 'Channel 2 (battery) voltage')
V3 = Field('V3', 'mV', 'Channel 3 (battery) voltage')
VS = Field('VS', 'mV', 'Auxiliary (starter) voltage')
VM = Field('VM', 'mV', 'Mid-point voltage of the battery bank')
DM = Field('DM', '%', 'Mid-point deviation of the battery bank')
VPV = Field('VPV', 'mV', 'Panel voltage')
PPV = Field('PPV', 'W', 'Panel power')
I = Field('I', 'mA', 'Main or channel 1 battery current')  # noqa: E741
I2 = Field('I2', 'mA', 'Channel 2 battery current')
I3 = Field('I3', 'mA', 'Channel 3 battery current')
IL = Field('IL', 'mA', 'Load current')
LOAD = Field('LOAD', '', 'Load output state (ON/OFF)')
T = Field('T', '°C', 'Battery temperature')
P = Field('P', 'W', 'Instantaneous power')
CE = Field('CE', 'mAh', 'Consumed Amp Hours')
SOC = Field('SOC', '%', 'State-of-charge')
TTG = Field('TTG', 'Minutes', 'Time-to-go')
Alarm = Field('Alarm', '', 'Alarm condition active')
Relay = Field('Relay', '', 'Relay state')
AR = Field('AR', '', 'Alarm reason')
OR = Field('OR', '', 'Off reason')
H1 = Field('H1', 'mAh', 'Depth of the deepest discharge')
H2 = Field('H2', 'mAh', 'Depth of the last discharge')
H3 = Field('H3', 'mAh', 'Depth of the average discharge')
H4 = Field('H4', '', 'Number of charge cycles')
H5 = Field('H5', '', 'Number of full discharges')
H6 = Field('H6', 'mAh', 'Cumulative Amp Hours drawn')
H7 = Field('H7', 'mV', 'Minimum main (battery) voltage')
H8 = Field('H8', 'mV', 'Maximum main (battery) voltage')
H9 = Field('H9', 'Seconds', 'Number of seconds since last full charge')
H10 = Field('H10', '', 'Number of automatic synchronizations')
H11 = Field('H11', '', 'Number of low main voltage alarms')
H12 = Field('H12', '', 'Number of high main voltage alarms')
H13 = Field('H13', '', 'Number of low auxiliary voltage alarms')
H14 = Field('H14', '', 'Number of high auxiliary voltage alarms')
H15 = Field('H15', 'mV', 'Minimum auxiliary (battery) voltage')
H16 = Field('H16', 'mV', 'Maximum auxiliary (battery) voltage')
H17 = Field('H17', '0.01 kWh', 'Amount of discharged energy')
H18 = Field('H18', '0.01 kWh', 'Amount of charged energy')
H19 = Field('H19', '0.01 kWh', 'Yield total (user resettable counter)')
H20 = Field('H20', '0.01 kWh', 'Yield today')
H21 = Field('H21', 'W', 'Maximum power today')
H22 = Field('H22', '0.01 kWh', 'Yield yesterday')
H23 = Field('H23', 'W', 'Maximum power yesterday')
ERR = Field('ERR', '', 'Error code')
CS = Field('CS', '', 'State of operation')
BMV = Field('BMV', '', 'Model description (deprecated)')
FW = Field('FW', '', 'Firmware version (16 bit)')
FWE = Field('FWE', '', 'Firmware version (24 bit)')
PID = Field('PID', '', 'Product ID')
SER = Field('SER#', '', 'Serial number')
HSDS = Field('HSDS', '', 'Day sequence number (0..364)')
MODE = Field('MODE', '', 'Device mode')
AC_OUT_V = Field('AC_OUT_V', '0.01 V', 'AC output voltage')
AC_OUT_I = Field('AC_OUT_I', '0.1 A', 'AC output current')
AC_OUT_S = Field('AC_OUT_S', 'VA', 'AC output apparent power')
WARN = Field('WARN', '', 'Warning reason')
MPPT = Field('MPPT', '', 'Tracker operation mode')

FIELDS = (
    # These fields have been tested.
    PID,
    FW,
    SER,
    V,
    I,
    VPV,
    PPV,
    CS,
    MPPT,
    ERR,
    LOAD,
    IL,
    H19,
    H20,
    H21,
    H22,
    H23,
    HSDS,
)

FIELD_MAP = {x.label: x for x in FIELDS}

PIDS = {
    0x203: 'BMV-700',
    0x204: 'BMV-702',
    0x205: 'BMV-700H',
    0x0300: 'BlueSolar MPPT 70|15',
    0xA040: 'BlueSolar MPPT 75|50',
    0xA041: 'BlueSolar MPPT 150|35',
    0xA042: 'BlueSolar MPPT 75|15',
    0xA043: 'BlueSolar MPPT 100|15',
    0xA044: 'BlueSolar MPPT 100|30',
    0xA045: 'BlueSolar MPPT 100|50',
    0xA046: 'BlueSolar MPPT 150|70',
    0xA047: 'BlueSolar MPPT 150|100',
    0xA049: 'BlueSolar MPPT 100|50 rev2',
    0xA04A: 'BlueSolar MPPT 100|30 rev2',
    0xA04B: 'BlueSolar MPPT 150|35 rev2',
    0xA04C: 'BlueSolar MPPT 75|10',
    0xA04D: 'BlueSolar MPPT 150|45',
    0xA04E: 'BlueSolar MPPT 150|60',
    0xA04F: 'BlueSolar MPPT 150|85',
    0xA050: 'SmartSolar MPPT 250|100',
    0xA051: 'SmartSolar MPPT 150|100',
    0xA052: 'SmartSolar MPPT 150|85',
    0xA053: 'SmartSolar MPPT 75|15',
    0xA054: 'SmartSolar MPPT 75|10',
    0xA055: 'SmartSolar MPPT 100|15',
    0xA056: 'SmartSolar MPPT 100|30',
    0xA057: 'SmartSolar MPPT 100|50',
    0xA058: 'SmartSolar MPPT 150|35',
    0xA059: 'SmartSolar MPPT 150|100 rev2',
    0xA05A: 'SmartSolar MPPT 150|85 rev2',
    0xA05B: 'SmartSolar MPPT 250|70',
    0xA05C: 'SmartSolar MPPT 250|85',
    0xA05D: 'SmartSolar MPPT 250|60',
    0xA05E: 'SmartSolar MPPT 250|45',
    0xA05F: 'SmartSolar MPPT 100|20',
    0xA060: 'SmartSolar MPPT 100|20 48V',
    0xA061: 'SmartSolar MPPT 150|45',
    0xA062: 'SmartSolar MPPT 150|60',
    0xA063: 'SmartSolar MPPT 150|70',
    0xA064: 'SmartSolar MPPT 250|85 rev2',
    0xA065: 'SmartSolar MPPT 250|100 rev2',
    0xA066: 'BlueSolar MPPT 100|20',
    0xA067: 'BlueSolar MPPT 100|20 48V',
    0xA068: 'SmartSolar MPPT 250|60 rev2',
    0xA069: 'SmartSolar MPPT 250|70 rev2',
    0xA06A: 'SmartSolar MPPT 150|45 rev2',
    0xA06B: 'SmartSolar MPPT 150|60 rev2',
    0xA06C: 'SmartSolar MPPT 150|70 rev2',
    0xA06D: 'SmartSolar MPPT 150|85 rev3',
    0xA06E: 'SmartSolar MPPT 150|100 rev3',
    0xA06F: 'BlueSolar MPPT 150|45 rev2',
    0xA070: 'BlueSolar MPPT 150|60 rev2',
    0xA071: 'BlueSolar MPPT 150|70 rev2',
    0xA102: 'SmartSolar MPPT VE.Can 150/70',
    0xA103: 'SmartSolar MPPT VE.Can 150/45',
    0xA104: 'SmartSolar MPPT VE.Can 150/60',
    0xA105: 'SmartSolar MPPT VE.Can 150/85',
    0xA106: 'SmartSolar MPPT VE.Can 150/100',
    0xA107: 'SmartSolar MPPT VE.Can 250/45',
    0xA108: 'SmartSolar MPPT VE.Can 250/60',
    0xA109: 'SmartSolar MPPT VE.Can 250/70',
    0xA10A: 'SmartSolar MPPT VE.Can 250/85',
    0xA10B: 'SmartSolar MPPT VE.Can 250/100',
    0xA10C: 'SmartSolar MPPT VE.Can 150/70 rev2',
    0xA10D: 'SmartSolar MPPT VE.Can 150/85 rev2',
    0xA10E: 'SmartSolar MPPT VE.Can 150/100 rev2',
    0xA10F: 'BlueSolar MPPT VE.Can 150/100',
    0xA112: 'BlueSolar MPPT VE.Can 250/70',
    0xA113: 'BlueSolar MPPT VE.Can 250/100',
    0xA114: 'SmartSolar MPPT VE.Can 250/70 rev2',
    0xA115: 'SmartSolar MPPT VE.Can 250/100 rev2',
    0xA116: 'SmartSolar MPPT VE.Can 250/85 rev2',
    0xA201: 'Phoenix Inverter 12V 250VA 230V',
    0xA202: 'Phoenix Inverter 24V 250VA 230V',
    0xA204: 'Phoenix Inverter 48V 250VA 230V',
    0xA211: 'Phoenix Inverter 12V 375VA 230V',
    0xA212: 'Phoenix Inverter 24V 375VA 230V',
    0xA214: 'Phoenix Inverter 48V 375VA 230V',
    0xA221: 'Phoenix Inverter 12V 500VA 230V',
    0xA222: 'Phoenix Inverter 24V 500VA 230V',
    0xA224: 'Phoenix Inverter 48V 500VA 230V',
    0xA231: 'Phoenix Inverter 12V 250VA 230V',
    0xA232: 'Phoenix Inverter 24V 250VA 230V',
    0xA234: 'Phoenix Inverter 48V 250VA 230V',
    0xA239: 'Phoenix Inverter 12V 250VA 120V',
    0xA23A: 'Phoenix Inverter 24V 250VA 120V',
    0xA23C: 'Phoenix Inverter 48V 250VA 120V',
    0xA241: 'Phoenix Inverter 12V 375VA 230V',
    0xA242: 'Phoenix Inverter 24V 375VA 230V',
    0xA244: 'Phoenix Inverter 48V 375VA 230V',
    0xA249: 'Phoenix Inverter 12V 375VA 120V',
    0xA24A: 'Phoenix Inverter 24V 375VA 120V',
    0xA24C: 'Phoenix Inverter 48V 375VA 120V',
    0xA251: 'Phoenix Inverter 12V 500VA 230V',
    0xA252: 'Phoenix Inverter 24V 500VA 230V',
    0xA254: 'Phoenix Inverter 48V 500VA 230V',
    0xA259: 'Phoenix Inverter 12V 500VA 120V',
    0xA25A: 'Phoenix Inverter 24V 500VA 120V',
    0xA25C: 'Phoenix Inverter 48V 500VA 120V',
    0xA261: 'Phoenix Inverter 12V 800VA 230V',
    0xA262: 'Phoenix Inverter 24V 800VA 230V',
    0xA264: 'Phoenix Inverter 48V 800VA 230V',
    0xA269: 'Phoenix Inverter 12V 800VA 120V',
    0xA26A: 'Phoenix Inverter 24V 800VA 120V',
    0xA26C: 'Phoenix Inverter 48V 800VA 120V',
    0xA271: 'Phoenix Inverter 12V 1200VA 230V',
    0xA272: 'Phoenix Inverter 24V 1200VA 230V',
    0xA274: 'Phoenix Inverter 48V 1200VA 230V',
    0xA279: 'Phoenix Inverter 12V 1200VA 120V',
    0xA27A: 'Phoenix Inverter 24V 1200VA 120V',
    0xA27C: 'Phoenix Inverter 48V 1200VA 120V',
    0xA281: 'Phoenix Inverter 12V 1600VA 230V',
    0xA282: 'Phoenix Inverter 24V 1600VA 230V',
    0xA284: 'Phoenix Inverter 48V 1600VA 230V',
    0xA291: 'Phoenix Inverter 12V 2000VA 230V',
    0xA292: 'Phoenix Inverter 24V 2000VA 230V',
    0xA294: 'Phoenix Inverter 48V 2000VA 230V',
    0xA2A1: 'Phoenix Inverter 12V 3000VA 230V',
    0xA2A2: 'Phoenix Inverter 24V 3000VA 230V',
    0xA2A4: 'Phoenix Inverter 48V 3000VA 230V',
    0xA340: 'Phoenix Smart IP43 Charger 12|50 (1+1)',
    0xA341: 'Phoenix Smart IP43 Charger 12|50 (3)',
    0xA342: 'Phoenix Smart IP43 Charger 24|25 (1+1)',
    0xA343: 'Phoenix Smart IP43 Charger 24|25 (3)',
    0xA344: 'Phoenix Smart IP43 Charger 12|30 (1+1)',
    0xA345: 'Phoenix Smart IP43 Charger 12|30 (3)',
    0xA346: 'Phoenix Smart IP43 Charger 24|16 (1+1)',
    0xA347: 'Phoenix Smart IP43 Charger 24|16 (3)',
}
