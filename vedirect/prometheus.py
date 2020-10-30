import enum
import time

import serial
import prometheus_client
import pint

from . import defs
from . import text

_UNITS = {
    '%': 'percent',
    '°C': 'celcius',
    '0.01 kWh': 'DWh',
}


def _is_enum(v):
    try:
        return issubclass(v, enum.Enum)
    except TypeError:
        return False


def _metrics(fields):
    metrics = {}
    labels = ['serial_number', 'product_id']

    for f in defs.FIELDS:
        label = f.label.replace('#', '')
        name = 'victron_%s' % label.lower()
        kind = f.kind()
        if isinstance(kind, pint.Quantity):
            unit = str(kind.units)
        else:
            unit = _UNITS.get(f.unit, f.unit)

        if unit == 'hour * watt':
            unit = 'wh'

        if kind == str:
            metrics[f.label] = prometheus_client.Info(name,
                                                      f.description,
                                                      labelnames=labels)
        elif _is_enum(kind):
            states = [x.name.lower() for x in kind]
            metrics[f.label] = prometheus_client.Enum(
                name,
                f.description,
                labelnames=['serial_number', 'product_id'],
                states=states)
            metrics[f.label + '_value'] = prometheus_client.Gauge(
                name + '_value',
                f.description,
                labelnames=['serial_number', 'product_id'])
        else:
            metrics[f.label] = prometheus_client.Gauge(
                name,
                f.description,
                labelnames=['serial_number', 'product_id'],
                unit=unit)

    updated = prometheus_client.Gauge(
        'victron_updated',
        'Last time a block was received from the device',
        labelnames=labels)
    blocks = prometheus_client.Counter(
        'victron_blocks',
        'Number of blocks received from the device',
        labelnames=labels)

    return metrics, updated, blocks


def _update(fields, metrics, updated, blocks):
    ser = fields[defs.SER.label]
    pid = fields[defs.PID.label]
    updated.labels(ser, pid).set(time.time())
    blocks.labels(ser, pid).inc()

    for label, value in fields.items():
        gauge = metrics[label]
        if isinstance(value, pint.Quantity):
            gauge.labels(ser, pid).set(value.m)
        elif isinstance(gauge, prometheus_client.Info):
            gauge.labels(ser,
                         pid).info({label.lower().replace('#', ''): value})
        elif isinstance(gauge, prometheus_client.Enum):
            gauge.labels(ser, pid).state(value.name.lower())
            metrics[label + '_value'].labels(ser, pid).set(value.value)
        elif isinstance(value, int):
            gauge.labels(ser, pid).set(value)
        else:
            print(repr(value))


def main():
    s = serial.Serial('/dev/ttyAMA4', 19200, timeout=0.7)

    metrics, updated, blocks = _metrics(defs.FIELDS)
    prometheus_client.start_http_server(7099)

    for fields in text.parse(s):
        _update(fields, metrics, updated, blocks)


if __name__ == '__main__':
    main()
