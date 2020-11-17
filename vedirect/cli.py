import prometheus_client
import serial
import click

from . import mqtt
from . import prometheus
from . import text


class Echo:
    def export(self, fields):
        print(fields)


@click.command()
@click.option('--port',
              type=click.Path(exists=True),
              required=True,
              help='Serial port connected to the controller')
@click.option('--prometheus_port',
              type=int,
              help='If supplied, export metrics on this port')
@click.option('--mqtt_host',
              help='If supplied, export metrics to this MQTT host')
@click.option('--echo',
              is_flag=True,
              help='If supplied, echo metrics to stdout')
def app(port, prometheus_port, mqtt_host, echo):
    s = serial.Serial(port, 19200, timeout=0.7)
    exporters = []

    if prometheus_port:
        prometheus_client.start_http_server(prometheus_port)
        exporters.append(prometheus.Exporter())

    if mqtt_host:
        exporters.append(mqtt.Exporter(mqtt_host))

    if echo:
        exporters.append(Echo())

    for fields in text.parse(s):
        for e in exporters:
            e.export(fields)
