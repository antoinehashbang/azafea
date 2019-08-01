# Copyright (c) 2019 - Endless
#
# This file is part of Azafea
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from threading import RLock
from typing import Generator

from gi.repository import GLib


# This was copy-pasted from the cpython master source code, and can thus be used under the same
# license as Python itself.
#
# We copy the code here because it was only introduced in Python 3.8 which isn't released yet.
#
# All of it can be removed if we move to Python 3.8 as the minimum required version.
_NOT_FOUND = object()


class cached_property:  # pragma: no cover
    def __init__(self, func):  # type: ignore
        self.func = func
        self.attrname = None
        self.__doc__ = func.__doc__
        self.lock = RLock()

    def __set_name__(self, owner, name):  # type: ignore
        if self.attrname is None:
            self.attrname = name
        elif name != self.attrname:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                f"({self.attrname!r} and {name!r})."
            )

    def __get__(self, instance, owner):  # type: ignore
        if instance is None:
            return self
        if self.attrname is None:
            raise TypeError(
                "Cannot use cached_property instance without calling __set_name__ on it.")
        try:
            cache = instance.__dict__
        except AttributeError:  # not all objects have __dict__ (e.g. class defines slots)
            msg = (
                f"No '__dict__' attribute on {type(instance).__name__!r} "
                f"instance to cache {self.attrname!r} property."
            )
            raise TypeError(msg) from None
        val = cache.get(self.attrname, _NOT_FOUND)
        if val is _NOT_FOUND:
            with self.lock:
                # check if another thread filled cache while we awaited lock
                val = cache.get(self.attrname, _NOT_FOUND)
                if val is _NOT_FOUND:
                    val = self.func(instance)
                    try:
                        cache[self.attrname] = val
                    except TypeError:
                        msg = (
                            f"The '__dict__' attribute on {type(instance).__name__!r} instance "
                            f"does not support item assignment for caching {self.attrname!r} "
                            "property."
                        )
                        raise TypeError(msg) from None
        return val
# End of the copy-pasted code


# This assumes value is a `ay` variant, verify before calling this
def get_bytes(value: GLib.Variant) -> bytes:
    return bytes(v.get_byte() for v in get_child_values(value))


# This assumes value is an array/tuple variant, verify before calling this
def get_child_values(value: GLib.Variant) -> Generator[GLib.Variant, None, None]:
    return (value.get_child_value(i) for i in range(value.n_children()))
