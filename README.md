# vedirect - export Victron metrics

This tool parses the Victron [VE.Direct][ved] TEXT protocol and
exports the metrics over [Prometheus][prom] and [MQTT][mqtt]. This can
be used to monitor your solar installation and view statistics in
tools like [Grafana](https://grafana.com/) or [Home Assistant][hass].

## Usage

```
python3 setup.py install

vedirect --port=/dev/ttyAMA4 \
	--prometheus_port=7099 \
	--mqtt_host=localhost
```

This will connect to the Victron module on ttyAMA4, export the metrics
at http://localhost:7099/metrics, and push the metrics to the MQTT
server at `localhost:1889`.

## Compatibility

This tool has been tested with a Victron BlueSolar 75/15 running
firmware 1.56 with protocol v3.29. See `vedirect/defs.py` to
enable new types.

## Prometheus

Each field appears as a separate Prometheus metric. For example:

```
wget -nv -O - http://localhost:7099/metrics
```

gives

```
victron_fw_info{fw="1.53",product_id="0xA042",serial_number="HQ1123I8XGA"} 1.0
victron_v_volt{product_id="0xA042",serial_number="HQ1123I8XGA"} 12.235
victron_i_ampere{product_id="0xA042",serial_number="HQ1123I8XGA"} -0.401
victron_cs{product_id="0xA042",serial_number="HQ1123I8XGA",victron_cs="off"} 1.0
victron_cs{product_id="0xA042",serial_number="HQ1123I8XGA",victron_cs="low_power"} 0.0
```

Gauges are put through a first order filter before exporting. This increases the apparent resolution of low resolution signals like the load current.

## MQTT

Each field appears as a separate, single valued MQTT topic. For example:

```
tele/victron_HQ1123I8XGA/pid 0xA042
tele/victron_HQ1123I8XGA/fw 1.53
tele/victron_HQ1123I8XGA/v 12.24
tele/victron_HQ1123I8XGA/i -0.4
```

This tool exports MQTT discovery records and should be automatically
detected by Home Assistant.

## Note

This is not an official Google product.

\-- Michael Hope <michaelh@juju.nz> <mlhx@google.com>

[hass]: https://www.home-assistant.io/
[mqtt]: https://mqtt.org/
[prom]: https://prometheus.io/
[ved]: https://www.victronenergy.com/live/vedirect_protocol:faq
