from normalize import normalize_tags
from timedelta import tell_time_ago


def find_step(size):
    return [i for i in range(20, 30) if size % i == 0][0]
