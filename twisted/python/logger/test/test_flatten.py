# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Test cases for L{twisted.python.logger._format}.
"""

import sys
from itertools import count
import json

try:
    from time import tzset
    # We should upgrade to a version of pyflakes that does not require this.
    tzset
except ImportError:
    tzset = None

from twisted.trial import unittest

from .._format import formatEvent
from .._flatten import (
    flattenEvent, extractField, KeyFlattener, aFormatter
)



class FlatFormattingTests(unittest.TestCase):
    """
    Tests for flattened event formatting functions.
    """

    def test_formatFlatEvent(self):
        """
        L{flattenEvent} will "flatten" an event so that, if scrubbed of all but
        serializable objects, it will preserve all necessary data to be
        formatted once serialized.  When presented with an event thusly
        flattened, L{formatEvent} will produce the same output.
        """
        counter = count()

        class Ephemeral(object):
            attribute = "value"

        event1 = dict(
            log_format="callable: {callme()} attribute: {object.attribute} "
                       "numrepr: {number!r} strrepr: {string!r}",
            callme=lambda: next(counter), object=Ephemeral(),
            number=7, string="hello",
        )

        flattenEvent(event1)

        event2 = dict(event1)
        del event2["callme"]
        del event2["object"]
        event3 = json.loads(json.dumps(event2))
        self.assertEquals(formatEvent(event3),
                          u"callable: 0 attribute: value numrepr: 7 "
                          "strrepr: 'hello'")


    def test_formatFlatEventWithMutatedFields(self):
        """
        L{formatEvent} will prefer the stored C{str()} or C{repr()} value for
        an object, in case the other version.
        """
        class Unpersistable(object):
            destructed = False

            def selfDestruct(self):
                """Self destruct"""
                self.destructed = True

            def __repr__(self):
                if self.destructed:
                    return "post-serialization garbage"
                else:
                    return "un-persistable"

        up = Unpersistable()
        event1 = dict(
            log_format="unpersistable: {unpersistable}", unpersistable=up
        )

        flattenEvent(event1)
        up.selfDestruct()

        self.assertEquals(formatEvent(event1), "unpersistable: un-persistable")


    def test_keyFlattening(self):
        """
        Test that L{KeyFlattener.flatKey} returns the expected keys for format
        fields.
        """

        def keyFromFormat(format):
            for (
                literalText,
                fieldName,
                formatSpec,
                conversion,
            ) in aFormatter.parse(format):
                return KeyFlattener().flatKey(fieldName, formatSpec,
                                              conversion)

        # No name
        try:
            self.assertEquals(keyFromFormat("{}"), "!:")
        except ValueError:
            if sys.version_info[:2] == (2, 6):
                # In python 2.6, an empty field name causes Formatter.parse to
                # raise ValueError.
                pass
            else:
                # In Python 2.7, it's allowed, so this exception is unexpected.
                raise

        # Just a name
        self.assertEquals(keyFromFormat("{foo}"), "foo!:")

        # Add conversion
        self.assertEquals(keyFromFormat("{foo!s}"), "foo!s:")
        self.assertEquals(keyFromFormat("{foo!r}"), "foo!r:")

        # Add format spec
        self.assertEquals(keyFromFormat("{foo:%s}"), "foo!:%s")
        self.assertEquals(keyFromFormat("{foo:!}"), "foo!:!")
        self.assertEquals(keyFromFormat("{foo::}"), "foo!::")

        # Both
        self.assertEquals(keyFromFormat("{foo!s:%s}"), "foo!s:%s")
        self.assertEquals(keyFromFormat("{foo!s:!}"), "foo!s:!")
        self.assertEquals(keyFromFormat("{foo!s::}"), "foo!s::")
        [keyPlusLiteral] = aFormatter.parse("{x}")
        key = keyPlusLiteral[1:]
        sameFlattener = KeyFlattener()
        self.assertEquals(sameFlattener.flatKey(*key), "x!:")
        self.assertEquals(sameFlattener.flatKey(*key), "x!:/2")


    def test_formatFlatEvent_fieldNamesSame(self):
        """
        The same format field used twice is rendered twice.
        """
        counter = count()

        class CountStr(object):
            def __str__(self):
                return str(next(counter))

        event = dict(
            log_format="{x} {x}",
            x=CountStr(),
        )
        flattenEvent(event)
        self.assertEquals(formatEvent(event), u"0 1")


    def test_extractField(self, flattenFirst=lambda x: x):
        """
        L{extractField} will extract a field used in the format string.

        @param flattenFirst: callable to flatten an event
        """
        class ObjectWithRepr(object):
            def __repr__(self):
                return "repr"

        class Something(object):
            def __init__(self):
                self.number = 7
                self.object = ObjectWithRepr()

            def __getstate__(self):
                raise NotImplementedError("Just in case.")

        event = dict(
            log_format="{something.number} {something.object}",
            something=Something(),
        )

        flattened = flattenFirst(event)

        def extract(field):
            return extractField(field, flattened)

        self.assertEquals(extract("something.number"), 7)
        self.assertEquals(extract("something.number!s"), "7")
        self.assertEquals(extract("something.object!s"), "repr")


    def test_extractFieldFlattenFirst(self):
        """
        L{extractField} behaves identically if the event is explicitly
        flattened first.
        """
        def flattened(evt):
            flattenEvent(evt)
            return evt
        self.test_extractField(flattened)


    def test_flattenEventWithoutFormat(self):
        """
        L{flattenEvent} will do nothing to an event with no format string.
        """
        inputEvent = {'a': 'b', 'c': 1}
        flattenEvent(inputEvent)
        self.assertEquals(inputEvent, {'a': 'b', 'c': 1})


    def test_flattenEventWithInertFormat(self):
        """
        L{flattenEvent} will do nothing to an event with a format string that
        contains no format fields.
        """
        inputEvent = {'a': 'b', 'c': 1, 'log_format': 'simple message'}
        flattenEvent(inputEvent)
        self.assertEquals(
            inputEvent,
            {
                'a': 'b',
                'c': 1,
                'log_format': 'simple message',
            }
        )