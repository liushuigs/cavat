import datetime


# convert local datetime str to utc str
# example given local timezone is -7000, 2016-04-26 02:00:00 will be converted to 2016-04-26 09:00:00
def datetime_str_to_utc(date_str):
        timedelta = datetime.datetime.utcnow() - datetime.datetime.now()
        local_datetime = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        result_utc_datetime = local_datetime - timedelta
        return result_utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

__all__ = ['datetime_str_to_utc']
