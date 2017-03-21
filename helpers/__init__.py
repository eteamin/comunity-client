import re

from normalize import normalize_tags
from timedelta import tell_time_ago
from alert import Alert
from overscroll import OverScrollEffect
from variables import server_url


def find_step(size):
    try:
        return [i for i in range(15, 40) if size % i == 0][0]
    except IndexError:
        return 15


def valid_email(email):
    pattern = '[^@]+@[^@]+\.[^@]+'
    return re.match(pattern, email)


def valid_username(u):
    return len(u) > 3 and not u.startswith('_') and not u.startswith('.') and not u.endswith('_') and not u.endswith('.')


def valid_password(p, rp):
    return len(p) >= 8 and p == rp
