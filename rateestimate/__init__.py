import datetime
import logging
import time

logger = logging.getLogger()


def get_epoch_time_from_string(s):
    try:
        import dateutil.parser  # http://pypi.python.org/pypi/python-dateutil/
        return dateutil.parser.parse(s)
    except (ImportError, ValueError):
        # parsedatetime can parse stuff like "yesterday" and "today" but it doesn't work with Python 3
        try:
            from parsedatetime import parsedatetime  # http://pypi.python.org/pypi/parsedatetime/
        except ImportError:
            raise ValueError("Couldn't parse datetime string: %r" % s)
        else:
            calendar = parsedatetime.Calendar()
            logger.debug("dateutil.parser.parse failed to parse: %r; trying parsedatetime.Calendar..." % s)
            return time.mktime(calendar.parse(s)[0])


def rate_estimate(time_value_pairs_sequence):
    times = []
    values = []
    rates = []

    for a_time, value in time_value_pairs_sequence:
        if hasattr(a_time, 'startswith'):
            a_time = get_epoch_time_from_string(a_time)

        if isinstance(a_time, time.struct_time):
            a_time = time.mktime(a_time)

        if isinstance(a_time, datetime.time):
            a_time = datetime.datetime(year=2012, month=8, day=27, hour=a_time.hour, minute=a_time.minute, second=a_time.second)

        if isinstance(a_time, datetime.datetime):
            a_time = time.mktime(a_time.timetuple())

        times.append(a_time)
        values.append(value)
        logger.debug("# time: %r; value: %r" % (a_time, value))

        try:
            time_delta = times[-1] - times[-2]
            value_delta = values[-1] - values[-2]
        except IndexError:
            pass
        else:
            rate = float(value_delta) / float(time_delta)
            logger.info("# time: %r; value: %r; time_delta: %r; value_delta: %r; rate: %r" % (a_time, value, time_delta, value_delta, rate))
            rates.append(rate)

    logger.info("# Rates: %r" % rates)

    return mean(rates)


def mean(seq):
    return sum(seq) / len(seq)
