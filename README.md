# vedirect - export Victron metrics

This tool parses the [VE.Direct][ved] TEXT protocol and exports the metrics
over [Prometheus][prom] and [MQTT][mqtt]. This can be used to monitor
your solar installation and view them in tools like
[Grafana](https://grafana.com/) or [Home Assistant][hass].

## Usage

	python3 setup.py install

    vedirect --port=/dev/ttyAMA4 \
		--prometheus_port=7099 \
		--mqtt_host=localhost

This will connect to the Victron module on ttyAMA4, export the metrics
at http://localhost:7099/metrics, and push the metrics to the MQTT
server at `localhost:1889`.

## Compatability

This tool has been tested with a Victron BlueSolar 75/15 running
firmware 1.56 with protocol v3.29. See `vedirect/defs.py` to
enable new types.

## Home Assistant

Ths tool exports MQTT discovery records and should be automatically
detected by Home Assistant.

## Note

This is not an official Google product.

-- Michael Hope <michaelh@juju.nz> <mlhx@google.com>

[ved]: https://www.victronenergy.com/live/vedirect_protocol:faq
[prom]: https://prometheus.io/
[mqtt]: https://mqtt.org/
[hass]: https://www.home-assistant.io/
