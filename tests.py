import datetime
import time
import unittest

from rateestimate import rate_estimate


class SimpleRateEstimateTests(unittest.TestCase):

    def test_5_exact(self):
        time_value_pairs_sequence = [
            (0, 12),
            (5, 37),
            (23, 127),
            (37, 197),
        ]
        self.assertAlmostEqual(rate_estimate(time_value_pairs_sequence), 5)

    def test_uneven(self):
        time_value_pairs_sequence = [
            (0, 12),
            (5, 27),
            (23, 127),
            (37, 197),
        ]
        self.assertAlmostEqual(rate_estimate(time_value_pairs_sequence), 4.5185185)

    def test_0_exact(self):
        time_value_pairs_sequence = [
            (0, 0),
            (5, 0),
            (23, 0),
            (37, 0),
        ]
        self.assertAlmostEqual(rate_estimate(time_value_pairs_sequence), 0)

    def test_negative(self):
        time_value_pairs_sequence = [
            (0, 100),
            (5, 90),
            (10, 80),
            (15, 70),
        ]
        self.assertAlmostEqual(rate_estimate(time_value_pairs_sequence), -2)


class DateTimeParseRateEstimateTests(unittest.TestCase):

    def test_5_per_second(self):
        time_value_pairs_sequence = [
            ('2012-08-29 11:59:58', 20),
            ('2012-08-29 11:59:59', 25),
            ('2012-08-29 12:00:00', 30),
            ('2012-08-29 12:00:01', 35),
            ('2012-08-29 12:00:02', 40),
            ('2012-08-29 12:00:03', 45),
        ]
        self.assertAlmostEqual(rate_estimate(time_value_pairs_sequence), 5.0)

    def test_120_per_minute_span_midnight_yesterday_and_today(self):
        time_value_pairs_sequence = [
            ('yesterday 23:58', 20),
            ('yesterday 23:59', 140),
            ('today 00:00', 260),
            ('today 00:01', 380),
            ('today 00:02', 500),
            ('today 00:03', 620),
        ]
        self.assertAlmostEqual(rate_estimate(time_value_pairs_sequence), 2.0)

    def test_120_per_minute_span_midnight_with_dates(self):
        time_value_pairs_sequence = [
            ('2012-08-28 23:58', 20),
            ('2012-08-28 23:59', 140),
            ('2012-08-29 00:00', 260),
            ('2012-08-29 00:01', 380),
            ('2012-08-29 00:02', 500),
            ('2012-08-29 00:03', 620),
        ]
        self.assertAlmostEqual(rate_estimate(time_value_pairs_sequence), 2.0)

    def test_5_per_second_from_12_to_1(self):
        time_value_pairs_sequence = [
            ('2012-08-29 12:59:58 PM', 20),
            ('2012-08-29 12:59:59 PM', 25),
            ('2012-08-29 1:00:00 PM', 30),
            ('2012-08-29 1:00:01 PM', 35),
            ('2012-08-29 1:00:02 PM', 40),
            ('2012-08-29 1:00:03 PM', 45),
        ]
        self.assertAlmostEqual(rate_estimate(time_value_pairs_sequence), 5.0)

    def test_5_per_second_span_midnight_struct_times(self):
        def parse_datetime(s):
            # Returns a time.struct_time
            return time.strptime(s, '%Y-%m-%d %I:%M:%S %p')

        time_value_pairs_sequence = [
            (parse_datetime('2012-08-28 11:59:58 PM'), 20),
            (parse_datetime('2012-08-28 11:59:59 PM'), 25),
            (parse_datetime('2012-08-29 12:00:00 AM'), 30),
            (parse_datetime('2012-08-29 12:00:01 AM'), 35),
            (parse_datetime('2012-08-29 12:00:02 AM'), 40),
            (parse_datetime('2012-08-29 12:00:03 AM'), 45),
        ]
        self.assertAlmostEqual(rate_estimate(time_value_pairs_sequence), 5.0)

    def test_5_per_second_span_midnight_datetime_time(self):
        time_value_pairs_sequence = [
            (datetime.time(hour=4, minute=59, second=58), 20),
            (datetime.time(hour=4, minute=59, second=59), 25),
            (datetime.time(hour=5, minute=0, second=0), 30),
            (datetime.time(hour=5, minute=0, second=1), 35),
            (datetime.time(hour=5, minute=0, second=2), 40),
            (datetime.time(hour=5, minute=0, second=3), 45),
        ]
        self.assertAlmostEqual(rate_estimate(time_value_pairs_sequence), 5.0)

    def test_5_per_second_datetime_datetime(self):
        time_value_pairs_sequence = [
            (datetime.datetime(year=2012, month=8, day=28, hour=23, minute=59, second=58), 20),
            (datetime.datetime(year=2012, month=8, day=28, hour=23, minute=59, second=59), 25),
            (datetime.datetime(year=2012, month=8, day=29, hour=0, minute=0, second=0), 30),
            (datetime.datetime(year=2012, month=8, day=29, hour=0, minute=0, second=1), 35),
            (datetime.datetime(year=2012, month=8, day=29, hour=0, minute=0, second=2), 40),
            (datetime.datetime(year=2012, month=8, day=29, hour=0, minute=0, second=3), 45),
        ]
        self.assertAlmostEqual(rate_estimate(time_value_pairs_sequence), 5.0)

    def test_5_per_minute(self):
        time_value_pairs_sequence = [
            ('2012-08-29 11:57', 20),
            ('2012-08-29 11:58', 25),
            ('2012-08-29 11:59', 30),
            ('2012-08-29 12:00', 35),
            ('2012-08-29 12:01', 40),
            ('2012-08-29 12:02', 45),
        ]
        self.assertAlmostEqual(rate_estimate(time_value_pairs_sequence), 0.08333333333333333)

    def test_real_data(self):
        time_value_pairs_sequence = [
            ('2012-08-29 11:23', 137),
            ('2012-08-29 12:42', 212),
            ('2012-08-29 12:57', 223),
            ('2012-08-29 13:40', 248),
            ('2012-08-29 15:46', 321),
            ('2012-08-29 16:21', 338),
        ]
        self.assertAlmostEqual(rate_estimate(time_value_pairs_sequence), 0.01109725045285834)


if __name__ == '__main__':
    unittest.main()
