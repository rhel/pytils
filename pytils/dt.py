# -*- coding: utf-8 -*-
# -*- test-case-name: pytils.test.test_dt -*-
# License: GNU GPL2
# Author: Pythy <the.pythy@gmail.com>
"""
Russian dates without locales
"""

__id__ = __revision__ = "$Id$"
__url__ = "$URL$"

import time
import datetime

from pytils import numeral

DAY_ALTERNATIVES = {
    1: (u"вчера", u"завтра"),
    2: (u"позавчера", u"послезавтра")
    }

DAY_VARIANTS = (
    u"день",
    u"дня",
    u"дней",
    )
HOUR_VARIANTS = (
    u"час",
    u"часа",
    u"часов",
    )
MINUTE_VARIANTS = (
    u"минуту",
    u"минуты",
    u"минут",
    )
PREFIX_IN = u"через"
SUFFIX_AGO = u"назад"

MONTH_NAMES = (
    (u"янв", u"январь", u"января"),
    (u"фев", u"февраль", u"февраля"),
    (u"мар", u"март", u"марта"),
    (u"апр", u"апрель", u"апреля"),
    (u"май", u"май", u"мая"),
    (u"июн", u"июнь", u"июня"),
    (u"июл", u"июль", u"июля"),
    (u"авг", u"август", u"августа"),
    (u"сен", u"сентябрь", u"сентября"),
    (u"окт", u"октябрь", u"октября"),
    (u"ноя", u"ноябрь", u"ноября"),
    (u"дек", u"декабрь", u"декабря"),
    )

DAY_NAMES = (
    (u"пн", u"понедельник"),
    (u"вт", u"вторник"),
    (u"ср", u"среда"),
    (u"чт", u"четверг"),
    (u"пт", u"пятница"),
    (u"сб", u"суббота"),
    (u"вск", u"воскресенье"),
    )


def distance_of_time_in_words(from_time, accuracy=1, to_time=None):
    """
    Represents distance of time in words

    @param from_time: source time (in seconds from epoch)
    @type from_time: C{int} or C{float}

    @param accuracy: level of accuracy (1..3), default=1
    @type accuracy: C{int}

    @param to_time: target time (in seconds from epoch),
        default=None translates to current time
    @type to_time: C{int} or C{float}

    @return: distance of time in words
    @rtype: unicode

    @raise AssertionError: input parameters' check failed
    """
    current = False
    
    if to_time is None:
        current = True
        to_time = time.time()

    assert isinstance(from_time, (int, float))
    assert isinstance(to_time, (int, float))
    assert isinstance(accuracy, int) and accuracy > 0

    seconds_orig = int(abs(to_time - from_time))
    minutes_orig = int(abs(to_time - from_time)/60.0)
    hours_orig   = int(abs(to_time - from_time)/3600.0)
    days_orig =    int(abs(to_time - from_time)/86400.0)
    in_future = from_time > to_time

    words = []
    values = []
    alternatives = []

    days = days_orig
    hours = hours_orig - days_orig*24

    words.append(u"%d %s" % (days, numeral.choose_plural(days, DAY_VARIANTS)))
    values.append(days)
    
    words.append(u"%d %s" % \
                  (hours, numeral.choose_plural(hours, HOUR_VARIANTS)))
    values.append(hours)

    hours == 1 and current and alternatives.append(u"час")

    minutes = minutes_orig - hours_orig*60

    words.append(u"%d %s" % (minutes,
                              numeral.choose_plural(minutes, MINUTE_VARIANTS)))
    values.append(minutes)

    minutes == 1 and current and alternatives.append(u"минуту")

    real_words = words
    # убираем из values и words конечные нули
    while values and not values[-1]:
        values.pop()
        words.pop()
    # убираем из values и words начальные нули
    while values and not values[0]:
        values.pop(0)
        words.pop(0)
    limit = min(accuracy, len(words))
    real_words = words[:limit]
    real_values = values[:limit]
    # снова убираем конечные нули
    while real_values and not real_values[-1]:
        real_values.pop()
        real_words.pop()
        limit -= 1

    real_str = u" ".join(real_words)
    
    # альтернативные варианты нужны только если в real_words одно значение
    # и, вдобавок, если используется текущее время
    alter_str = limit == 1 and current and \
                alternatives and alternatives[0]
    _result_str = alter_str or real_str
    result_str = in_future and u"%s %s" % (PREFIX_IN, _result_str) \
                           or u"%s %s" % (_result_str, SUFFIX_AGO)

    # если же прошло менее минуты, то real_words -- пустой, и поэтому
    # нужно брать alternatives[0], а не result_str
    zero_str = minutes == 0 and not real_words and \
            (in_future and u"менее чем через минуту" \
                        or u"менее минуты назад")

    # нужно использовать вчера/позавчера/завтра/послезавтра
    # если days 1..2 и в real_words одно значение
    day_alternatives = DAY_ALTERNATIVES.get(days, False)
    alternate_day = day_alternatives and current and limit == 1 and \
                    ((in_future and day_alternatives[1]) \
                                 or day_alternatives[0])

    
    final_str = not real_words and zero_str or alternate_day or result_str

    return final_str


def ru_strftime(format=u"%d.%m.%Y", date=None, inflected=False):
    """
    Russian strftime without locale

    @param format: strftime format, default=u'%d.%m.%Y'
    @type format: C{unicode}

    @param date: date value, default=None translates to today
    @type date: C{datetime.date} or C{datetime.datetime}

    @return: strftime string
    @rtype: unicode

    @raise AssertionError: input parameters' check failed
    """
    if date is None:
        date = datetime.datetime.today()
    assert isinstance(date, (datetime.date, datetime.datetime))
    assert isinstance(format, unicode)
    
    if inflected:
        midx = 2
    else:
        midx = 1

    format = format.replace(u'%a', DAY_NAMES[date.weekday()][0])
    format = format.replace(u'%A', DAY_NAMES[date.weekday()][1])
    format = format.replace(u'%b', MONTH_NAMES[date.month-1][0])
    format = format.replace(u'%B', MONTH_NAMES[date.month-1][midx])

    # strftime must be str, so encode it to utf8:
    s_format = format.encode("utf-8")
    s_res = date.strftime(s_format)
    # and back to unicode
    u_res = s_res.decode("utf-8")

    return u_res
    
