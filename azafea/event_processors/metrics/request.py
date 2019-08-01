# Copyright (c) 2019 - Endless
#
# This file is part of Azafea
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from datetime import datetime, timezone
from typing import Generator

from gi.repository import GLib

from .utils import cached_property, get_bytes, get_child_values


class RequestBuilder:
    __format_string__ = '(ixxaya(uayxmv)a(uayxxmv)a(uaya(xmv)))'
    __variant_type__ = GLib.VariantType(__format_string__)

    def __init__(self, serialized: bytes, variant: GLib.Variant, received_at: datetime):
        self._serialized = serialized
        self._variant = variant
        self._received_at = received_at

    @classmethod
    def parse_bytes(cls, data: bytes) -> 'RequestBuilder':
        # data is an array of bytes, the concatenation of:
        # - a datetime encoded on 8 bytes (a 64 bits integer timestamp in microseconds)
        # - the metrics request (a serialized GVariant)

        received_at_timestamp = int.from_bytes(data[:8], 'little')
        received_at = datetime.fromtimestamp(received_at_timestamp / 1000000, tz=timezone.utc)

        request_body = data[8:]
        variant = GLib.Variant.new_from_bytes(cls.__variant_type__, GLib.Bytes.new(request_body),
                                              False)

        if not variant.is_normal_form():
            raise ValueError('Metric request is not in the expected format:'
                             f'{cls.__format_string__}')

        return cls(request_body, variant, received_at)

    @cached_property
    def send_number(self) -> int:
        return self._variant.get_child_value(0).get_int32()

    @cached_property
    def relative_timestamp(self) -> int:
        return self._variant.get_child_value(1).get_int64()

    @cached_property
    def absolute_timestamp(self) -> int:
        return self._variant.get_child_value(2).get_int64()

    @cached_property
    def machine_id(self) -> str:
        return get_bytes(self._variant.get_child_value(3)).hex()

    @property
    def singulars(self) -> Generator[GLib.Variant, None, None]:
        return get_child_values(self._variant.get_child_value(4))

    @property
    def aggregates(self) -> Generator[GLib.Variant, None, None]:
        return get_child_values(self._variant.get_child_value(5))

    @property
    def sequences(self) -> Generator[GLib.Variant, None, None]:
        return get_child_values(self._variant.get_child_value(6))
