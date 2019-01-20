import datetime


def date_from_str(date_str):
    format_str = '%m/%d/%Y'
    datetime_obj = datetime.datetime.strptime(date_str, format_str)
    return datetime_obj.date()