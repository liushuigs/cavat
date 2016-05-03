import datetime
import numbers
from datetime import timedelta


def datetime_str_to_utc(date_str, timezone=None):
    """
    convert local datetime str to utc str

    timezone should be a number
    example given local timezone is -7, 2016-04-26 02:00:00 will be converted to 2016-04-26 09:00:00
    """
    if isinstance(timezone, numbers.Number):
        time_delta = timedelta(seconds=timezone * 3600)
    else:
        time_delta = datetime.datetime.utcnow() - datetime.datetime.now()
    local_datetime = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    result_utc_datetime = local_datetime - time_delta
    return result_utc_datetime.strftime("%Y-%m-%d %H:%M:%S")


__all__ = ['datetime_str_to_utc']
