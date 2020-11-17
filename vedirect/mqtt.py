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
"""Exports fields over MQTT with discovery."""

import enum
import json
import time
from typing import Dict, Optional

import paho.mqtt.client as mqtt
import pint

from . import defs

_UNITS = {
    'volt': ('V', 'voltage'),
    'ampere': ('A', 'current'),
    'watt': ('W', 'power'),
    'hour * watt': ('Wh', 'energy'),
}


class Exporter:
    def __init__(self, host: str, port: int = 1883):
        self._last = None  # type: Optional[float]

        self._client = mqtt.Client()
        self._client.connect_async(host, port, 60)
        self._client.loop_start()

    def _config(self, ser: str, fields: dict) -> None:
        for label, value in fields.items():
            f = defs.FIELD_MAP[label]
            labelc = f.label.replace('#', '').lower()
            device = {
                'ids': [ser],
            }  # type: Dict[str, object]
            if f == defs.PID:
                device.update({
                    'manufacturer': 'Victron',
                    'model': defs.PIDS[int(value, 16)],
                    'name': f'Victron {ser}',
                    'sw_version': fields[defs.FW.label],
                })

            config = {
                'name': f'Victron {label}',
                'state_topic': f'tele/victron_{ser}/{labelc}',
                'unique_id': f'victron_{ser}_{labelc}',
                'expire_after': 600,
                'device': device,
            }
            if isinstance(value, pint.Quantity):
                unit = str(value.units)
                unit, klass = _UNITS.get(unit, (unit, None))
                config['unit_of_measurement'] = unit
                if klass:
                    config['device_class'] = klass

            self._client.publish(
                f'homeassistant/sensor/victron_{ser}_{labelc}/config',
                json.dumps(config),
                retain=True)

    def export(self, fields: dict) -> None:
        ser = fields[defs.SER.label]
        if self._last is None:
            self._config(ser, fields)
        elif (time.time() - self._last) < 60:
            return

        self._last = time.time()

        for label, value in fields.items():
            name = label.replace('#', '').lower()
            topic = f'tele/victron_{ser}/{name}'

            if isinstance(value, pint.Quantity):
                payload = round(value.m, 3)
            elif isinstance(value, enum.IntEnum):
                payload = int(value)
            else:
                payload = str(value)

            self._client.publish(topic, payload)
