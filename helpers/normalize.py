

def normalize_tags(tags):
    """
    :param tags:
     expected tags in string format separated by comma

    :return:
    return string containing tags
    """
    return tags.replace('#', '').replace(' ', ',')


def normalize_number(n):
    if n < 1000:
        return str(n)
    elif 1000000 > n >= 1000:
        return '{}k'.format(str(n / float(1000))[:str(n / float(1000)).index('.') + 2])
    elif 1000000000 > n >= 1000000:
        return '{}m'.format(str(n / float(1000000))[:str(n / float(1000000)).index('.') + 2])
    else:
        return 'Unlimited!'
