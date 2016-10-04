

def normalize_tags(tags):
    """
    :param tags:
     expected tags in string format separated by comma

    :return:
    return a list containing tags
    """
    return [unicode.strip(t) for t in tags.split(',')]
