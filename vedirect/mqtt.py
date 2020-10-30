import enum
import time
import json

import serial
import paho.mqtt.client as mqtt
import pint

from . import defs
from . import text

_UNITS = {
    'volt': ('V', 'voltage'),
    'ampere': ('A', 'current'),
    'watt': ('W', 'power'),
    'hour * watt': ('Wh', 'energy'),
}


def _config(client, ser, fields):
    for label, value in fields.items():
        f = defs.FIELD_MAP[label]
        labelc = f.label.replace('#', '').lower()
        device = {
            'ids': [ser],
        }
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

        client.publish(f'homeassistant/sensor/victron_{ser}_{labelc}/config',
                       json.dumps(config))


def main():
    s = serial.Serial('/dev/ttyAMA4', 19200, timeout=0.7)
    client = mqtt.Client()
    client.connect_async('localhost', 1883, 60)
    client.loop_start()

    last = None
    for fields in text.parse(s):
        ser = fields[defs.SER.label]
        if last is None:
            _config(client, ser, fields)
        elif (time.time() - last) < 60:
            continue

        last = time.time()

        for label, value in fields.items():
            name = label.replace('#', '').lower()
            topic = f'tele/victron_{ser}/{name}'

            if isinstance(value, pint.Quantity):
                payload = value.m
            elif isinstance(value, enum.IntEnum):
                payload = int(value)
            else:
                payload = str(value)

            client.publish(topic, payload)


if __name__ == '__main__':
    main()
