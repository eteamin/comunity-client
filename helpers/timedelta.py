from datetime import datetime


def tell_time_ago(basetime):
    date, time = basetime.split(' ')
    y, mth, d = date.split('-')
    h, m, mss = time.split(':')
    # mss == Second and millisecond
    s, ms = mss.split('.')
    given_time = datetime(int(y), int(mth), int(d), int(h), int(m), int(s), int(ms))
    difference = datetime.now() - given_time

    days = difference.days
    seconds = difference.seconds
    hours = seconds / 3600
    minutes = seconds / 60

    if days and days == 1:
        return 'yesterday'
    elif days and days != 1 and days < 7:
        return '%s days ago' % days
    elif days and days != 1 and 7 < days < 31:
        return 'within this month'
    elif days and days != 1 and 30 < days < 365:
        return '%s months ago' % (days / 30)
    elif days and days != 1 and 365 <= days < 730:
        return 'a year ago'
    elif days and days != 1 and days >= 730:
        return '%s years ago' % (days / 365)

    elif hours and hours == 1:
        return 'an hour ago'
    elif hours and hours != 1:
        return '%s hours ago' % hours

    elif minutes and minutes == 1:
        return 'a minute ago'
    elif minutes and minutes != 1:
        return '%s minutes ago' % minutes

    elif seconds and seconds == 1:
        return 'a second ago'
    elif seconds and seconds != 1:
        return '%s seconds ago' % seconds

    else:
        return '0 second ago'


if __name__ == '__main__':
    a = datetime(2016, 9, 19, 16, 56, 57, 530000)
    print(tell_time_ago(a))
