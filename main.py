# import datetime
# from babel.dates import format_date, format_datetime, format_time
#
# a = datetime.datetime.now()
#
# formatted_date = format_date(a, locale='ru')
# formatted_datetime = format_datetime(a, locale='ru')
#
# print(formatted_date)
# print(formatted_datetime)

import datetime
from babel.dates import format_datetime


a = datetime.datetime.now()


formatted_datetime = format_datetime(a, format='EEEE, d MMMM ', locale='ru')

print(formatted_datetime)