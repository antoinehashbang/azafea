.. _events page:

Events
======

This page is a list of events that Endless OS currently records for users that
have not opted out of metrics recording, as well as events recorded by previous
versions of Endless OS which are not recorded by current versions.


Stored Events
-------------

.. automodule:: azafea.event_processors.endless.metrics.events
   :members:


Unknown Events
--------------

Desktop Searches
~~~~~~~~~~~~~~~~

We record searches made from the desktop search bar.

- Since: 2.1.2
- UUID: ``b02266bc-b010-44b2-ae0f-8f116ffa50eb``
- UUID name: ``EVENT_DESKTOP_SEARCH`` in gnome-shell
- Payload: type ``(us)``

  - search provider

    - local: 0
    - Google: 1

  - query string (what the user searched for)

.. note::

   Since the 2.1.6. release, Google searches have no longer been recorded.

Knowledge App Search
~~~~~~~~~~~~~~~~~~~~

We record the search terms used for searching within the knowledge apps along
with the app ID of the knowledge app. (We also record the search term used when
a user performed a desktop search and clicked through to a knowledge app.)

- Since: 2.3.0
- UUID: ``a628c936-5d87-434a-a57a-015a0f223838``
- UUID name: ``SEARCH_METRIC_EVENT_ID`` in eos-knowledge-lib
- Payload: type ``(ss)``

  - search terms
  - application ID

Link Shared from Knowledge App
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reported when a user shares a link from one of our content apps on a social network.

- Since: SDK 2
- UUID: ``6775771a-afe7-4158-b7bb-6296fcc7b70d``
- UUID name: ``SHARE_METRIC_EVENT_ID`` in eos-knowledge-lib
- Payload: type ``(sayssu)``

  - Application ID (e.g. ``com.endlessm.animals.en``)
  - ID of content record as a byte array of length 20
    (``ekn://043fd69fe153ac69a05000b60bfea9cff110f14c`` becomes ``[0x04, 0x3f,
    0xd6, 0x9f, 0xe1, 0x53, 0xac, 0x69, 0xa0, 0x50, 0x00, 0xb6, 0x0b, 0xfe,
    0xa9, 0xcf, 0xf1, 0x10, 0xf1, 0x4c]``)
  - Content title
  - The exact URL of the content online, as it was shared to the social network
  - A numerical code indicating which social network the content was shared to

    - Facebook: 0
    - Twitter: 1
    - Whatsapp: 2

See `T18524 <https://phabricator.endlessm.com/T18524>`_.

Knowledge App – Article Open/Close
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We record when an article is opened or closed in a knowledge app. We record the
ID of the content, the entry point (whether the article was accessed via
article link, desktop search, app link click, or a nav button), the app ID, the
article title, and the content type.

- Since: SDK 2
- UUID: ``fae00ef3-aad7-44ca-aff2-16555e45f0d9``
- UUID name: ``CONTENT_ACCESS_METRIC_EVENT_ID`` in eos-knowledge-lib
- Payload of start event: type ``(ssss)``

  - Entry point
  - Application ID
  - Title
  - Content type

- Payload of stop event: ``NULL``

See `T18516 <https://phabricator.endlessm.com/T18516>`_.

Hack Toolbox - Code View Error - Hack Episode 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Since: 3.5.3
- UUID: ``e98aa2b8-3f11-4a25-b8e9-b10a635df121``
- UUID name: ``CODEVIEW_ERROR_EVENT``
- Payload of start event: type ``sssa(suquq)``

  - Application ID that this toolbox belongs to (string)
  - ID of function that was being edited in the toolbox (string) (currently always blank)
  - Contents of code view (string)
  - List of the error messages that are displayed, each containing:
  - Text of error message (string)
  - Start line number where error is shown, 1-based (32-bit unsigned)
  - Start column number where error is shown, 0-based (16-bit unsigned)
  - End line number where error is shown, 1-based (32-bit unsigned)
  - End column number where error is shown, 0-based (16-bit unsigned)

- Payload of progress and stop events: type ``s``

  - Diff of the contents of the code view to the state from the previous event,
    in the form of an `ed script
    <https://www.gnu.org/software/diffutils/manual/html_node/ed-Scripts.html>`_,
    chosen because it's the shortest form that the ``diff`` utility can output

See `T24429 <https://phabricator.endlessm.com/T24429>`_.

Hack Clubhouse - Quest
~~~~~~~~~~~~~~~~~~~~~~

- Since: 3.7.4
- UUID: ``50aebb1b-7a93-4caf-8698-3a601a0fc0f6``
- UUID name: ``QUEST_EVENT``
- Key: The quest name
- Payload of start event: type ``(bsas)``

  - ``True`` if the quest is completed
  - The quest ID
  - The list of pathway names of this quest

- Payload of stop event: type ``(bsas)``

  - ``True`` if the quest is completed
  - The quest ID
  - The list of pathway names of this quest

See `T28004 <https://phabricator.endlessm.com/T28004>`_.


Deprecated Events
-----------------

System Shutdown
~~~~~~~~~~~~~~~

.. note::

   This event has been deprecated in 3.7.0 and is not sent any more. See the
   uptime event which replaced it. See `T27963
   <https://phabricator.endlessm.com/T27963>`_.

We records shutdowns as well as the total length of time the computer has been
powered on across all boots. Since 2.5.0, we also include the total number of
boots the computer has been through.

- UUID from 2.2.0: ``SHUTDOWN`` − ``ae391c82-1937-4ae5-8539-8d1aceed037d`` − eos-metrics-instrumentation
- UUID from 2.5.0: ``SHUTDOWN_EVENT`` − ``91de63ea-c7b7-412c-93f3-6f3d9b2f864c`` − eos-metrics-instrumentation
- UUID from 2.5.2: ``SHUTDOWN_EVENT`` − ``8f70276e-3f78-45b2-99f8-94db231d42dd`` − eos-metrics-instrumentation

- Payload: type ``(xx)``

  - total uptime across all boots
  - number of boots the computer has been through

.. note::

   A serious bug that often prevented this event from being recorded was fixed
   in the 2.3.0 release. Another serious bug that often prevented this event
   from being recorded was introduced in 2.4.0 and fixed in 2.5.1. A serious
   bug that often prevented the boot count from being incremented was fixed in
   the 2.5.2 release.

Companion App - Device Authenticate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note:

   The companion app is no more.

Reported when a user authenticates a device with the Companion App Service

- UUID from 3.4: ``6dad6c44-f52f-4bca-8b4c-dc203f175b97`` − eos-companion-app-integration

- Payload: type ``a{ss}``

  - A dictionary of string keys to string values:

    - ``deviceUUID``: hash of unique device identifier

See `T21316 <https://phabricator.endlessm.com/T21316>`_.

Companion App - List Applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   The companion app is no more.

Reported when a user gets an application listing from the Companion App Service

- UUID from 3.4: ``337fa66d-5163-46ae-ab20-dc605b5d7307`` − eos-companion-app-integration

- Payload: type ``a{ss}``

  - a dictionary of string keys to string values:

    - ``deviceUUID``: hash of unique device identifier
    - ``referrer``: optional, name of view that the user came from, one of:

      - ``feed``: the content feed
      - ``search_content``: search
      - ``list_content_for_tags``: listing of content for a category
      - ``list_applications``: listing of available applications
      - ``list_application_sets``: listing of categories for an application
      - ``device_authenticate``: when a user first associates a device with a computer
      - ``refresh``: when a user pulls down to refresh
      - ``retry``: when the user manually retries after a timeout
      - ``back``: when the user goes back
      - ``content``: following a link from within content

See `T21316 <https://phabricator.endlessm.com/T21316>`_.

Companion App - List Sets for Applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   The companion app is no more.

Reported when a user gets a listing of application sets from the Companion App
Service.

- UUID from 3.4: ``c02a5764-7f81-48c7-aea4-1413fd4e829c``

- Payload: type ``a{ss}``

  - A dictionary of string keys to string values:

    - ``deviceUUID``: hash of unique device identifier
    - ``applicationId``: application ID
    - ``referrer``: see "Companion App - List applications"

See `T21316 <https://phabricator.endlessm.com/T21316>`_.

Companion App - List Content for Tags of Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   The companion app is no more.

Reported when a user gets a listing of application content for a set of tags
from the Companion App Service.

- UUID from 3.4: ``bef3d12c-df9b-43cd-a67c-31abc5361f03``

- Payload: type ``a{ss}``

  - A dictionary of string keys to string values:

    - ``deviceUUID``: hash of unique device identifier
    - ``applicationId``: application ID
    - ``tags``: semicolon delimited list of tags
    - ``referrer``: see "Companion App - List applications"

See `T21316 <https://phabricator.endlessm.com/T21316>`_.

Companion App - View Content
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   The companion app is no more.

Reported when a user views some requested content EKN-ID on the Companion App.

- UUID from 3.4: ``e6541049-9462-4db5-96df-1977f3051578``

- Payload: type ``a{ss}``

  - A dictionary of string keys to string values:

    - ``deviceUUID``: hash of unique device identifier
    - ``applicationId``: application ID
    - ``contentTitle``: content title
    - ``contentType``: content MIME type
    - ``referrer``: see "Companion App - List applications"

See `T21316 <https://phabricator.endlessm.com/T21316>`_.

Companion App - Get Content Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   The companion app is no more.

Reported when a user gets some metadata about some requested content EKN-ID on
the Companion App.

- UUID from 3.4: ``3a4eff55-5d01-48c8-a827-fca5732fd767``

- Payload: type ``a{ss}``

  - A dictionary of string keys to string values:

    - ``deviceUUID``: hash of unique device identifier
    - ``applicationId``: application ID
    - ``contentId``: EKN ID
    - ``referrer``: see "Companion App - List applications"

See `T21316 <https://phabricator.endlessm.com/T21316>`_.

Companion App - Search for Content or Applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   The companion app is no more.

Reported when a user uses the search functionality on the app to search for
things.

- UUID from 3.4: ``9f06d0f7-677e-43ca-b732-ccbb40847a31``

- Payload: type ``a{ss}``

  - A dictionary of string keys to string values:

    - ``deviceUUID``: hash of unique device identifier
    - ``applicationId``: application ID
    - ``tags``: semicolon delimited list of tags
    - ``searchTerm``: optional, search term
    - ``referrer``: see "Companion App - List applications"

See `T21316 <https://phabricator.endlessm.com/T21316>`_.

Companion App - Request Content Feed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   The companion app is no more.

Reported when the user opens the Companion App and requests the content feed.

- UUID from 3.4: ``af3e89b2-8293-4703-809c-8e0231c128cb``

- Payload: type ``a{ss}``

  - A dictionary of string keys to string values:
    - ``deviceUUID``: hash of unique device identifier
    - ``mode``: 'ascending' or 'descending'
    - ``referrer``: see "Companion App - List applications"

See `T22203 <https://phabricator.endlessm.com/T22203>`_.

Companion App - Download Bundled Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   The companion app is no more.

- UUID from TBC: ``7be595662b23-408a-acf6-91490fc1df1c``

- Payload: type ``a{ss}``

  - A dictionary of string keys to string values:

    - ``deviceUUID``: hash of unique device identifier
    - ``referrer``: see "Companion App - List applications"

See `T22053 <https://phabricator.endlessm.com/T22053>`_.

Network Status Changed
~~~~~~~~~~~~~~~~~~~~~~

Removed in 3.7.4. See `T28301 <https://phabricator.endlessm.com/T28301>`_.

We record when the network status changes from one state to another. A common
case of this is moving from an "unknown" state to a "connecting" to a "globally
connected" state on startup.

See `the comprehensive list of status codes
<https://developer.gnome.org/NetworkManager/stable/nm-dbus-types.html#NMState>`_.

- UUID from 2.10: ``EMTR_EVENT_NETWORK_STATUS_CHANGED`` − ``5fae6179-e108-4962-83be-c909259c0584`` − eos-metrics

- Payload: type ``(uu)``

  - Previous network state
  - New network state

.. note::

   Since https://github.com/endlessm/eos-shell/issues/2684 was fixed in 2.2.0,
   we no longer misrepresent local and site connectivity as global
   connectivity.

Social Bar Is Visible
~~~~~~~~~~~~~~~~~~~~~

We record when the social bar is made visible to the user and when it is no
longer visible. Basically, it corresponds to the user clicking on the social
bar icon.

- UUID from 2.10: ``EMTR_EVENT_SOCIAL_BAR_IS_VISIBLE`` − ``9c33a734-7ed8-4348-9e39-3c27f4dc2e62`` - eos-social
- Payload of start event: ``NULL``
- Payload of stop event: ``NULL``


Test Events
-----------

The following are only ever used in tests, and are thus discarded by the server
upon reception.

We document them here to make sure they don't get reused inadvertently by real
events.

- `Smoke tests <https://github.com/endlessm/eos-metrics/blob/ab66c7319c573999740f636555b14b6f658e82c0/tests/smoke-tests/smokeLibrary.js#L22-L27>`_

  - ``72fea371-15d1-401d-8a40-c47f379f64fd``
  - ``9a0cf836-12cd-4887-95d8-e48ccdf6e552``
  - ``b1f87a3f-a464-48d4-8e35-35dd45659010``
  - ``b2b17dfd-c30e-4789-abcc-4a38323127f6``
  - ``b89f9a4a-3035-4fc3-9bef-584367fe2c96``
  - ``fb59199e-5384-472e-af1e-00b7a419d5c2``

- `Event recorder tests <https://github.com/endlessm/eos-metrics/blob/ab66c7319c573999740f636555b14b6f658e82c0/tests/test-event-recorder.c#L29-L30>`_

  - ``350ac4ff-3026-4c25-9e7e-e8103b4fd5d8``
  - ``d936cd5c-08de-4d4e-8a87-8df1f4a33cba``

- `Daemon tests <https://github.com/endlessm/eos-event-recorder-daemon/blob/efc6bb0e1283236ee4fe9c3d7fc992c4a53436d8/tests/daemon/test-daemon.c#L51>`_

  - ``350ac4ff-3026-4c25-9e7e-e8103b4fd5d8``


Timestamp Algorithm
-------------------

This chapter is not intended to be formal documentation but rather a primer to
understanding how the timestamp algorithm for the metrics system works. As
such, some simplifications are made at the expense of accuracy.

Analogies
~~~~~~~~~

Analogy to help understand the problem of determining correct event timestamps
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A tourist just arrived in San Francisco and wanted to visit the beautiful
sights and tourist spots in the city. Unfortunately, instead of bringing his
watch, he accidentally brought his stopwatch. Not to be deterred, right before
he started touring the city, he started his stopwatch.

Along the way, the man sees many beautiful sights, including a fireworks
display, an awesome office on the 3rd floor of 512 2nd Street, and sunset at
the Golden Gate Bridge. He records all of these events in his journal, writing
down the event and the time on his stopwatch.

Eventually, he gets tired and decides to catch a bus ride North all the way to
Seattle. He hops on the bus by the San Francisco Ferry Building, and right
before the bus leaves, he stops his stopwatch and checks the time on the clock
tower on the building. Right as he writes down the current date and time, and
the time on his stopwatch, the bus leaves.

Long after the bus has departed, he starts talking with the passenger sitting
next to him. The passenger informs the tourist that the clock tower is
sometimes inaccurate.

Not wishing to repeat his mistake of trusting a fallible clock tower, the
tourist consults an atomic clock upon arriving in Seattle. He then realizes
that he forgot to time the trip from San Francisco to Seattle, but he sighs in
relief when he remembers that his train ticket lists the estimated duration.

He checks into a hotel and starts going through his journal. He tries to
convert the stopwatch times of each San Francisco event to the time the event
happened. What can he do to make the times he calculates as accurate as
possible?

Analogy to help visualize the problem of calculating correct timestamps
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

All of the relative timestamps of events are correct relative to each other.
However, the problem is placing the groups of events on the right scale.

Imagine moving a sliding weight on a scale. The problem is finding the right
position of the weight on the scale where the scale is balanced. The weight is
analogous to a group of events with relative timestamps. The scale is analogous
to a timeline. The problem is finding the right position on the timeline where
the events occurred.

Client Side
~~~~~~~~~~~

Suppose we want to find out what time an event occurred.

Naive Attempt
+++++++++++++

- Definition: **Absolute Timestamp** - Time elapsed since the Unix Epoch in
  1970 -- at least according to the system clock.

Well, this should be simple, right? We will just use an **absolute timestamp**,
package it with the event, and pat ourselves on the back! Let's see what
happens in this case:

```
User boots up system at Noon (Day X).
User plays Akintu for 1 hour. It is now 1:00 PM (Day X).
User sets the system clock forward one day, tricking the metrics system. It is now 1:00 PM (Day X + 1).
Any events recorded now will appear to have occurred in the future.
(The previous Akintu event would still be correct as it was recorded before the clock change)
```

This problem also exists without setting the system clock to a bogus time. If
the user's computer is offline for a long time, his or her system clock will
slowly drift away from true time. This could end up being minutes off in
extreme cases of no connectivity. We cannot trust the **absolute timestamps**
alone.

- Definition: **Relative Timestamp** - Time elapsed since the OS booted up.

We cannot use purely **relative timestamps** either, as that wouldn't be able
to track the time while the computer is powered off. Rather we'll need a
combination of the two as well as something we call the **boot offset**.

- Definition: **Boot Offset** - The value to add to any relative timestamp
  within the current boot to correct (or "true up") to an accurate time.

Smart Algorithm
+++++++++++++++

(This algorithm is based on the `Kurt Truth Premise <https://www.youtube.com/watch?v=dQw4w9WgXcQ>`_.)

So we need some way to track the time that isn't vulnerable to user-changes to
the system clock or clock drift, but doesn't neglect to track time spent
offline. Turns out we need a **boot offset** to tell us how much to adjust our
events' timestamps by. This will make use of both a **relative time** and an
**absolute time** combined with some logging to persistent storage on shutdown
and computation on start up.

We will use the following quantities:

- Boot Offset (What we ultimately add to correct the events' relative timestamps.)
- Stored Boot Offset (The previously written boot offset.)
- Current Relative Time (How long the OS has been running for today. When computed at startup, will be about 0.)
- Stored Relative Time (How long the OS was running for the previous boot.)
- Current Absolute Time (What time the system clock says it is *right now*.)
- Stored Absolute Time (What time the system clock said it was during our last shutdown.)

In the following formula::

  Boot Offset = Stored Boot Offset + (Stored Relative Time - Current Relative Time) + (Current Absolute Time - Stored Absolute Time)

Let us give it a shot::

  User starts up at noon (Day X).
    -- Absolute Time = noon (Day X) Define this quantity as 0 for easier math!
    -- Relative Time = 0
    -- Boot Offset = 0 (When no boot offset exists, it is set to 0.)
  User learns about Racket until 1:00 PM (Day X).
  User powers off machine.
    -- Relative Time STORED --> 1
    -- Absolute Time STORED --> 1
  User powers on machine at 2:00 PM (Day X).
    -- Absolute Time = 2
    -- Stored Absolute Time = 1
    -- Relative Time = 0
    -- Stored Relative Time = 1
    -- Stored Boot Offset = 0
    -- New Boot Offset = 0 + (1 - 0) + (2 - 1) = 2
  User hooks up dance pads and plays Stepmania until 3:00 PM (Day X).
  User sets system clock back one day. It is now 3:00 PM (Day X - 1) according to the absolute clock.
  User reads up on the "Time Cube" until 4:00 PM (Day X in reality, Day X - 1 according to the absolute clock).
  User powers off machine.
    -- Relative Time STORED --> 2
    -- Absolute Time STORED --> -20
  User powers on machine at 5:00 PM (Day X, Day X - 1 according to the absolute clock).
    -- Absolute Time = -19
    -- Stored Absolute Time = -20
    -- Relative Time = 0
    -- Stored Relative Time = 2
    -- Stored Boot Offset = 2
    -- New Boot Offset = 2 + (2 - 0) + (-19 - -20) = 5

As you can see, the boot offsets are correctly determining the number of hours
since the true first boot. There are some subtleties that are being ignored
such as why we bother with the "current" relative time at all, but the intent
is to illustrate the motivation for and essentials of the algorithm.

Server Side
~~~~~~~~~~~

The metrics system packages bundles of events/metrics together into a **network
request** and sends it off to the server(s) when a connection is detected. This
network request has a couple of timestamps of its own.

- Definition: **Network Request Relative Timestamp** - Time elapsed between the
  "origin" boot and when the network request was created. Was also corrected
  via the client algorithm.
- Definition: **Network Request Absolute Timestamp** - The system clock's
  estimation of when the network request was created (in terms of the Unix
  Epoch, as before.)
- Definition: **Metric Corrected Relative Timestamp** - The result of our
  client-side algorithm to generate the time a metric occurred, relative to the
  "origin" boot.

When the server receives a network request, it will first examine the **network
request absolute time** to see if it varies significantly from its own
(trusted) clock. If it does, some special action will be taken with that
request, such as putting it in its own special table or attempting to correct
the timestamp in some fashion.

What we want is the **metric corrected absolute timestamp**.

- Definition: **Metric Corrected Absolute Timestamp** - The result of our
  server-side algorithm to generate the actual real-world time a metric
  occurred.
- Definition: **Origin Boot Absolute Time** - The time at which the "first"
  boot occurred on a system. In a perfect world, this is always the first boot
  of the system ever.

Assuming it passes this sanity check, the server then unpacks the network
request and examines each **metric corrected relative timestamp**. The server
does the following::

  … Assuming we've passed the sanity check …
  Origin Boot Absolute Time = Network Request Absolute Time - Network Request Relative Time
  For each metric in request:
      Metric Corrected Relative Timestamp = Origin Boot Absolute Time + Metric Corrected Relative Timestamp
