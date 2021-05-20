Network Protocol
================

The metrics system has a particular wire format that it must adhere to (that
is, a format for the network request containing a bundle of metrics.) It should
be kept up to date with `emer-daemon.c
<https://github.com/endlessm/eos-event-recorder-daemon/blob/master/daemon/emer-daemon.c>`_.
If this document is inconsistent with the code, please make sure the document
is updated accordingly.

.. note::

    Any changes that modify the network protocol must increment the network
    protocol version number in the same commit.


Wire Format
-----------

Global Structure
~~~~~~~~~~~~~~~~

The format is entirely little-endian. In order, its elements are:

Relative Timestamp
++++++++++++++++++

- 64 bit signed integer
- GVariant symbol: ``x``
- See: http://linux.die.net/man/3/clock_gettime

Absolute Timestamp
++++++++++++++++++

- 64 bit signed integer
- GVariant symbol: ``x``
- Nanoseconds since the Unix epoch
- See: http://linux.die.net/man/3/clock_gettime

Image
+++++

- String
- GVariant symbol: ``s``
- Saved in an attribute on the root filesystem by the image builder, and allows
  to tell the channel that the OS was installed by (e.g. download, OEM
  pre-install, Endless hardware, USB stick, etc), to tell which version was
  installed, and to group machines with deployment-specific images for metrics
  analysis purposes
- Format is ``{product}-{branch}-{arch}-{platform}.{date}-{time}.{personality}``
  (for example ``eos-3.7-amd64-amd64.190419-225606.base``)

Site
++++

- Dictionary from string to string
- GVariant symbol: ``a{ss}``
- Location label allowing an operator to provide an optional human-readable
  label for the location of the system, which can be used when preparing
  reports or visualisations of the metrics data

Dual Boot, Live
+++++++++++++++

- Byte
- GVariant symbol: ``y``
- Bits are set to 1 to set flags:

  - bit 0: dual boot
  - bit 1: live
  - bits 2 to 7 are curently unused and reserved for future use

Singular Metrics
++++++++++++++++

- Array of singular metrics
- See `Singular Metric`_
- GVariant symbol: ``a(aysxmv)``

Aggregate Metrics
+++++++++++++++++

- Array of aggregate metrics
- See `Aggregate Metric`_
- GVariant symbol: ``a(aysyxxmv)``

Total GVariant Format String
++++++++++++++++++++++++++++

All together it should look like: ``(xxsa{ss}ya(aysxmv)a(aysyxxmv))``.

Singular Metric
~~~~~~~~~~~~~~~

Singular metrics indicate simple events that occur and don't need to be
aggregated (like an aggregate metric) to make sense.

In order:

Event ID
++++++++

- Array of 16 unsigned bytes
- GVariant symbol: ``ay``
- Listed in :ref:`events page`
- See: http://linux.die.net/man/3/uuid

OS Version
++++++++++

- String
- GVariant symbol: ``s``
- This is ``VERSION_ID`` from `os-release
  <https://www.freedesktop.org/software/systemd/man/os-release.html>`_

Relative Timestamp
++++++++++++++++++

- 64 bit signed integer
- GVariant symbol: ``x``
- Nanoseconds since the last computer boot
- See: http://linux.die.net/man/3/clock_gettime

Auxiliary Payload
+++++++++++++++++

- Maybe Variant
- Allows for no contents ``(NULL)`` or content of any type
- Used to contain data associated with an event that is logged
- GVariant symbol: ``mv``
- See: https://developer.gnome.org/glib/stable/gvariant-format-strings.html#gvariant-format-strings-maybe-types
- Details for each event ID listed in :ref:`events page`

Aggregate Metric
~~~~~~~~~~~~~~~~

Aggregate metrics indicate counts that summarize a value of interest (e.g., a
very common event happening n times in a particular time interval or
fluctuations in heap size over time). Counts are always strictly positive. They
are identical to the singular metrics but have an added counter field in the
wire format.

Aggregates can be used to record noisy events such as cache hit ratios, heap
usage, or any number items that would be impractical to send a `singular
metric`_ for each instance.

In order:

Event ID
++++++++

- Array of 16 unsigned bytes
- GVariant symbol: ``ay``
- Listed in :ref:`events page`
- See: http://linux.die.net/man/3/uuid

OS Version
++++++++++

- String
- GVariant symbol: ``s``

Period
++++++

- Unsigned byte
- GVariant symbol: ``y``
- Aggregation period (``h`` for hour, ``d`` for day, ``w`` for week, ``m`` for
  month)

Absolute Timestamp
++++++++++++++++++

- 64 bit signed integer
- GVariant symbol: ``x``
- Nanoseconds since the Unix epoch
- Beginning of the period, with aggregation done using user’s computer time

Count
+++++

- 64-bit signed integer
- GVariant symbol: ``x``

Auxiliary Payload
+++++++++++++++++

- Maybe Variant
- Allows for no contents ``(NULL)`` or content of any type
- Used to contain data associated with an event that is logged
- GVariant symbol: ``mv``
- See: https://developer.gnome.org/glib/stable/gvariant-format-strings.html#gvariant-format-strings-maybe-types
- Details for each event ID listed in :ref:`events page`

Version History
---------------

Version 0
~~~~~~~~~

- Initial Release
- URI Format: ``https://production.metrics.endlessm.com/0/<SHA-512-Hash>``
- No compression
- Little Endian
- GVariant Payload Format: ``(xxaya(uayxmv)a(uayxxmv)a(uaya(xmv)))``

Contents:

- Relative Timestamp
- Absolute Timestamp
- Machine ID (**unusable id**)
- Singular Events (User ID, Event ID, Relative Timestamp, Auxiliary Payload)
- Aggregate Events (User ID, Event ID, Count, Relative Timestamp, Auxiliary Payload)
- Sequence Events (User ID, Event ID, Array of (Relative Timestamp, Auxiliary Payload))

Version 1
~~~~~~~~~

- Endless 2.1.2
- URI Format: ``https://production.metrics.endlessm.com/1/<SHA-512-Hash>``
- No compression
- Little Endian
- GVariant Payload Format: ``(xxaya(uayxmv)a(uayxxmv)a(uaya(xmv)))``
- Now uses valid Machine ID

Contents:

- Relative Timestamp
- Absolute Timestamp
- Machine ID fixed
- Singular Events (User ID, Event ID, Relative Timestamp, Auxiliary Payload)
- Aggregate Events (User ID, Event ID, Count, Relative Timestamp, Auxiliary Payload)
- Sequence Events (User ID, Event ID, Array of (Relative Timestamp, Auxiliary Payload))

Version 2
~~~~~~~~~

- Endless 2.1.5
- URI Format: ``https://production.metrics.endlessm.com/2/<SHA-512-Hash>``
- No compression
- Little Endian
- GVariant Payload Format: ``(ixxaya(uayxmv)a(uayxxmv)a(uaya(xmv)))``
- Added "network send number" as a signed 32-bit integer to help glean information regarding the number of metric bundles that fail to make it to the databases.

Contents:

- Network Send Number
- Machine ID
- Singular Events (User ID, Event ID, Relative Timestamp, Auxiliary Payload)
- Aggregate Events (User ID, Event ID, Count, Relative Timestamp, Auxiliary Payload)
- Sequence Events (User ID, Event ID, Array of (Relative Timestamp, Auxiliary Payload))

Version 3
~~~~~~~~~

- Endless 4.0.0
- URI Format: ``https://production.metrics.endlessm.com/3/<SHA-512-Hash>``
- No compression
- Little Endian
- GVariant Payload Format: ``(xxsa{ss}ya(aysxmv)a(aysyxxmv))``
- Removed "network send number".

Contents:

- Network Send Number
- Channel (image, site, dualboot, live)
- Singular Events (Event ID, OS Version, Relative Timestamp, Absolute
  Timestamp, Auxiliary Payload)
- Aggregate Events (Event ID, OS Version, Period, Relative Timestamp, Count,
  Auxiliary Payload)
