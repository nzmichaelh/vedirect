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
"""Implements a VE.Direct text protocol decoder."""

import enum
from typing import Iterator, Tuple

import pint

from . import defs

_LF = 0x0A
_CR = 0x0D
_TAB = 0x09
_CHECKSUM = 'Checksum'

# Parsers for certain unique field values.
_PARSERS = {
    defs.FW.label: lambda x: '%d.%d' % (int(x) // 100, int(x) % 100),
    defs.LOAD.label: lambda x: 1 if x == 'ON' else 0,
}


class ProtocolError(RuntimeError):
    pass


class _Source:
    """A simple buffered reader."""
    def __init__(self, f):
        self._f = f
        self._ready = b''

    def next(self) -> int:
        while self._ready is None or len(self._ready) == 0:
            self._ready = self._f.read(1000)

        ch, self._ready = self._ready[0], self._ready[1:]
        return ch


def _get_value(label: str, value: bytearray) -> object:
    """Parses the value in a label specific way."""
    if label == _CHECKSUM:
        return value[0]

    value = value.decode()
    try:
        if label not in defs.FIELD_MAP:
            return int(value)
        field = defs.FIELD_MAP[label]
        kind = field.kind()
        if field.label in _PARSERS:
            value = _PARSERS[field.label](value)
        if kind is not None:
            if isinstance(kind, pint.Quantity):
                return int(value) * kind
            elif issubclass(kind, enum.Enum):
                return kind(int(value))
            elif issubclass(kind, str):
                return value
            assert False, 'Unhandled kind %s' % kind
        return int(value)
    except ValueError:
        return value


def _get_line(src: _Source) -> Tuple[str, object]:
    label = bytearray()

    while True:
        ch = src.next()
        if ch == _TAB:
            break
        label.append(ch)

    value = bytearray((src.next(), ))

    while True:
        ch = src.next()
        if ch == _CR:
            break
        value += bytes([ch])

    ch = src.next()
    if ch != _LF:
        raise ProtocolError('got a 0x%x, want a LF' % ch)

    label = label.decode()
    return label, _get_value(label, value)


def parse(src) -> Iterator[dict]:
    src = _Source(src)

    while src.next() != _LF:
        pass

    while True:
        label, value = _get_line(src)
        if label == _CHECKSUM:
            break

    while True:
        fields = {}

        while True:
            label, value = _get_line(src)
            if label == _CHECKSUM:
                # End of a block
                break
            fields[label] = value

        yield fields
