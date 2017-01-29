

def normalize_tags(tags):
    """
    :param tags:
     expected tags in string format separated by comma

    :return:
    return string containing tags
    """
    return tags.replace('#', '').replace(' ', ',')
