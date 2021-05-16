"""
Nose tests for acp_times.py

We cannot test for randomness here (no effective oracle),
but we can test that the elements in the returned arrow
are correct.
"""

from acp_times import open_time, close_time

import nose    # Testing framework
import arrow
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def test_neg():
    # Test when the control distance is within the first 60km
    nose.tools.assert_raises(AssertionError, open_time, -10, 200, arrow.get("2021-01-01T00:00"))
    nose.tools.assert_raises(AssertionError, open_time, -1, 300, arrow.get("2021-01-01T00:00"))
    nose.tools.assert_raises(AssertionError, open_time, -12, 400, arrow.get("2021-01-01T00:00"))
    nose.tools.assert_raises(AssertionError, open_time, -200, 600, arrow.get("2021-01-01T00:00"))
    nose.tools.assert_raises(AssertionError, open_time, -20, 1000, arrow.get("2021-01-01T00:00"))


def test_long():
    # Test when the control distance is over 20% longer than the brevet distance
    nose.tools.assert_raises(AssertionError, open_time, 250, 200, arrow.get("2021-01-01T00:00"))
    nose.tools.assert_raises(AssertionError, open_time, 366, 300, arrow.get("2021-01-01T00:00"))
    nose.tools.assert_raises(AssertionError, open_time, 481, 400, arrow.get("2021-01-01T00:00"))
    nose.tools.assert_raises(AssertionError, open_time, 731, 600, arrow.get("2021-01-01T00:00"))
    nose.tools.assert_raises(AssertionError, open_time, 1220, 1000, arrow.get("2021-01-01T00:00"))


def test_200km():
    # Test when the control distance is within the first 60km
    assert open_time(0, 200, arrow.get("2021-01-01T00:00")) == arrow.get("2021-01-01T00:00")
    assert close_time(0, 200, arrow.get("2021-01-01T00:00")) == arrow.get("2021-01-01T01:00")

    # Test when the date change (end of year & end of month & end of day)
    assert open_time(100, 200, arrow.get("2021-12-31T21:00")) == arrow.get("2021-12-31T23:56")
    assert close_time(100, 200, arrow.get("2021-12-31T21:00")) == arrow.get("2022-01-01T03:40")

    # Test general case (0 <= control location <= 200)
    assert open_time(124, 200, arrow.get("2021-12-21T05:40")) == arrow.get("2021-12-21T09:19")
    assert close_time(124, 200, arrow.get("2021-12-21T05:40")) == arrow.get("2021-12-21T13:56")

    # Test when the control distance equals to the brevet distance
    assert open_time(200, 200, arrow.get("2001-03-21T10:15")) == arrow.get("2001-03-21T16:08")
    assert close_time(200, 200, arrow.get("2001-03-21T10:15")) == arrow.get("2001-03-21T23:45")

    # Test when the control distance is longer than the brevet distance but not than 20% of the brevet distance
    assert open_time(205, 200, arrow.get("2011-02-21T12:30")) == arrow.get("2011-02-21T18:23")
    assert close_time(205, 200, arrow.get("2011-02-21T12:30")) == arrow.get("2011-02-22T02:00")


def test_300km():
    # Test when the control distance is within the first 60km
    assert open_time(10, 300, arrow.get("2021-01-01T06:20")) == arrow.get("2021-01-01T06:38")
    assert close_time(10, 300, arrow.get("2021-01-01T06:20")) == arrow.get("2021-01-01T07:50")

    # Test when the date change (end of year & end of month & end of day)
    assert open_time(100, 300, arrow.get("1990-12-31T20:40")) == arrow.get("1990-12-31T23:36")
    assert close_time(100, 300, arrow.get("1990-12-31T20:40")) == arrow.get("1991-01-01T03:20")

    # Test general case (0 <= control location <= 200)
    assert open_time(137, 300, arrow.get("2019-11-30T12:00")) == arrow.get("2019-11-30T16:02")
    assert close_time(137, 300, arrow.get("2019-11-30T12:00")) == arrow.get("2019-11-30T21:08")

    # Test general case (200 < control location <= 400)
    assert open_time(250, 300, arrow.get("2019-12-30T07:00")) == arrow.get("2019-12-30T14:27")
    assert close_time(250, 300, arrow.get("2019-12-30T07:00")) == arrow.get("2019-12-30T23:40")

    # Test when the control distance equals to the brevet distance
    assert open_time(300, 300, arrow.get("2001-03-21T05:22")) == arrow.get("2001-03-21T14:22")
    assert close_time(300, 300, arrow.get("2001-03-21T05:22")) == arrow.get("2001-03-22T01:22")

    # Test when the control distance is longer than the brevet distance but not than 20% of the brevet distance
    assert open_time(320, 300, arrow.get("2001-03-21T05:22")) == arrow.get("2001-03-21T14:22")
    assert close_time(320, 300, arrow.get("2001-03-21T05:22")) == arrow.get("2001-03-22T01:22")


def test_400km():
    # Test when the control distance is within the first 60km
    assert open_time(20, 400, arrow.get("2021-05-01T00:00")) == arrow.get("2021-05-01T00:35")
    assert close_time(20, 400, arrow.get("2021-05-01T00:00")) == arrow.get("2021-05-01T02:00")

    # Test when the date change (end of year & end of month & end of day)
    assert open_time(100, 400, arrow.get("1990-12-31T21:22")) == arrow.get("1991-01-01T00:18")
    assert close_time(100, 400, arrow.get("1990-12-31T21:22")) == arrow.get("1991-01-01T04:02")

    # Test general case (0 <= control location <= 200)
    assert open_time(99, 400, arrow.get("2010-04-17T13:20")) == arrow.get("2010-04-17T16:15")
    assert close_time(99, 400, arrow.get("2010-04-17T13:20")) == arrow.get("2010-04-17T19:56")

    # Test general case (200 < control location <= 400)
    assert open_time(220, 400, arrow.get("2018-11-17T06:00")) == arrow.get("2018-11-17T12:30")
    assert close_time(220, 400, arrow.get("2018-11-17T06:00")) == arrow.get("2018-11-17T20:40")

    # Test when the control distance equals to the brevet distance
    assert open_time(400, 400, arrow.get("2001-08-14T06:35")) == arrow.get("2001-08-14T18:43")
    assert close_time(400, 400, arrow.get("2001-08-14T06:35")) == arrow.get("2001-08-15T09:35")

    # Test when the control distance is longer than the brevet distance but not than 20% of the brevet distance
    assert open_time(470, 400, arrow.get("2001-10-21T05:40")) == arrow.get("2001-10-21T17:48")
    assert close_time(470, 400, arrow.get("2001-10-21T05:40")) == arrow.get("2001-10-22T08:40")


def test_600km():
    # Test when the control distance is within the first 60km
    assert open_time(35, 600, arrow.get("2021-06-01T01:00")) == arrow.get("2021-06-01T02:02")
    assert close_time(35, 600, arrow.get("2021-06-01T01:00")) == arrow.get("2021-06-01T03:45")

    # Test when the date change (end of year & end of month & end of day)
    assert open_time(100, 600, arrow.get("1880-12-31T21:20")) == arrow.get("1881-01-01T00:16")
    assert close_time(100, 600, arrow.get("1880-12-31T21:20")) == arrow.get("1881-01-01T04:00")

    # Test general case (0 <= control location <= 200)
    assert open_time(156, 600, arrow.get("2010-04-17T11:11")) == arrow.get("2010-04-17T15:46")
    assert close_time(156, 600, arrow.get("2010-04-17T11:11")) == arrow.get("2010-04-17T21:35")

    # Test general case (200 < control location <= 400)
    assert open_time(350, 600, arrow.get("2018-02-17T05:15")) == arrow.get("2018-02-17T15:49")
    assert close_time(350, 600, arrow.get("2018-02-17T05:15")) == arrow.get("2018-02-18T04:35")

    # Test general case (400 < control location <= 600)
    assert open_time(570, 600, arrow.get("2018-11-17T06:00")) == arrow.get("2018-11-17T23:48")
    assert close_time(570, 600, arrow.get("2018-11-17T06:00")) == arrow.get("2018-11-18T20:00")

    # Test when the control distance equals to the brevet distance
    assert open_time(600, 600, arrow.get("2001-08-14T15:27")) == arrow.get("2001-08-15T10:15")
    assert close_time(600, 600, arrow.get("2001-08-14T15:27")) == arrow.get("2001-08-16T07:27")

    # Test when the control distance is longer than the brevet distance but not than 20% of the brevet distance
    assert open_time(700, 600, arrow.get("2001-10-21T14:00")) == arrow.get("2001-10-22T08:48")
    assert close_time(700, 600, arrow.get("2001-10-21T14:00")) == arrow.get("2001-10-23T06:00")


def test_1000km():
    # Test when the control distance is within the first 60km
    assert open_time(44, 1000, arrow.get("2021-06-01T15:20")) == arrow.get("2021-06-01T16:38")
    assert close_time(44, 1000, arrow.get("2021-06-01T15:20")) == arrow.get("2021-06-01T18:32")

    # Test when the date change (end of year & end of month & end of day)
    assert open_time(80, 1000, arrow.get("1880-12-31T19:45")) == arrow.get("1880-12-31T22:06")
    assert close_time(80, 1000, arrow.get("1880-12-31T19:45")) == arrow.get("1881-01-01T01:05")

    # Test general case (0 <= control location <= 200)
    assert open_time(122, 1000, arrow.get("2000-02-17T11:37")) == arrow.get("2000-02-17T15:12")
    assert close_time(122, 1000, arrow.get("2000-02-17T11:37")) == arrow.get("2000-02-17T19:45")

    # Test general case (200 < control location <= 400)
    assert open_time(256, 1000, arrow.get("2018-02-17T05:55")) == arrow.get("2018-02-17T13:33")
    assert close_time(256, 1000, arrow.get("2018-02-17T05:55")) == arrow.get("2018-02-17T22:59")

    # Test general case (400 < control location <= 600)
    assert open_time(555, 1000, arrow.get("2018-11-17T16:24")) == arrow.get("2018-11-18T09:42")
    assert close_time(555, 1000, arrow.get("2018-11-17T16:24")) == arrow.get("2018-11-19T05:24")

    # Test general case (600 < control location <= 1000)
    assert open_time(890, 1000, arrow.get("1999-02-26T06:00")) == arrow.get("1999-02-27T11:09")
    assert close_time(890, 1000, arrow.get("1999-02-26T06:00")) == arrow.get("1999-02-28T23:23")

    # Test when the control distance equals to the brevet distance
    assert open_time(1000, 1000, arrow.get("2020-05-19T18:13")) == arrow.get("2020-05-21T03:18")
    assert close_time(1000, 1000, arrow.get("2020-05-19T18:13")) == arrow.get("2020-05-22T21:13")

    # Test when the control distance is longer than the brevet distance but not than 20% of the brevet distance
    assert open_time(1140, 1000, arrow.get("2011-10-21T11:00")) == arrow.get("2011-10-22T20:05")
    assert close_time(1140, 1000, arrow.get("2011-10-21T11:00")) == arrow.get("2011-10-24T14:00")

