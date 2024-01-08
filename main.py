from pprint import pprint
# 커스텀
from src.utils import check_ip
from src.model import get_pred

if __name__ == '__main__':
    check_ip()
    for t in ('BTC', 'ETH'):
        get_pred(t)