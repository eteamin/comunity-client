import re

from normalize import normalize_tags
from timedelta import tell_time_ago
from alert import Alert


def find_step(size):
    return [i for i in range(20, 30) if size % i == 0][0]


def valid_email(email):
    pattern = '[^@]+@[^@]+\.[^@]+'
    return re.match(pattern, email)


def valid_username(u):
    return len(u) > 3 and not u.startswith('_') and not u.startswith('.') and not u.endswith('_') and not u.endswith('.')


def valid_password(p, rp):
    return len(p) >= 8 and p == rp
