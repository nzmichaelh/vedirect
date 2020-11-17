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

import click
import prometheus_client
import serial

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
def app(port: str, prometheus_port: int, mqtt_host: str, echo: bool):
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
