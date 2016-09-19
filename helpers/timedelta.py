from datetime import datetime


def tell_time_ago(basetime):
    difference = datetime.now() - basetime

    days = difference.days
    seconds = difference.seconds
    hours = seconds / 3600
    minutes = seconds / 60

    if days and days == 1:
        return 'Yesterday'
    elif days and days != 1 and days < 7:
        return '%s days ago' % days
    elif days and days != 1 and 7 < days < 31:
        return 'Within this month'
    elif days and days != 1 and 30 < days < 365:
        return '%s months ago' % (days / 30)
    elif days and days != 1 and 365 <= days < 730:
        return 'A year ago'
    elif days and days != 1 and days >= 730:
        return '%s years ago' % (days / 365)

    elif hours and hours == 1:
        return 'An hour ago'
    elif hours and hours != 1:
        return '%s hours ago' % hours

    elif minutes and minutes == 1:
        return 'A minute ago'
    elif minutes and minutes != 1:
        return '%s minutes ago' % minutes

    elif seconds and seconds == 1:
        return 'A second ago'
    elif seconds and seconds != 1:
        return '%s seconds ago' % seconds

    else:
        return '0 second ago'


if __name__ == '__main__':
    a = datetime(2016, 9, 19, 16, 56, 57, 530000)
    print(tell_time_ago(a))
