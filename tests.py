# 표준
from unittest import TestCase, main, skip
# 커스텀
from src.utils import check_ip, get_yaml
from src.data import get_price_hourly, get_price_info
from src.model import forecast_with_config, get_pred
from src.account import get_account_balance, trade

class LogicTests(TestCase):
    @skip('하위 모듈 → trade')
    def test_basket(self):
        basket = get_yaml('config.yml').get('basket', [])
        print(basket)
        self.assertNotEqual(len(basket), 0)

    def test_check_ip(self):
        self.assertIsInstance(check_ip(), str)

    @skip('하위 모듈 → forecast_with_config')
    def test_price_hourly(self):
        cnt = 100
        for t in ('BTC', 'ETH'):
            l = len(get_price_hourly(t, cnt))
            self.assertEqual(l, cnt+1)
    
    @skip('하위 모듈 → get_pred')
    def test_forecast_with_config(self):
        for t in ('BTC', 'ETH'):
            for y in ('high', 'low'):
                fcst = forecast_with_config(t, y)
                self.assertGreater(len(fcst), 0)
    
    @skip('하위 모듈 → trade')
    def test_get_pred(self):
        for t in ('BTC', 'ETH'):
            pred = get_pred(t)
            self.assertIsInstance(pred, dict)

    @skip('하위 모듈 → trade')
    def test_get_account_balance(self):
        self.assertEqual(
            len(get_account_balance()), 3)

    @skip('하위 모듈 → trade')
    def test_get_account_balance_total(self):
        self.assertIsInstance(
            get_account_balance(total=True), float)
    
    @skip('하위 모듈 → trade')
    def test_get_price_info(self):
        for t in ('BTC', 'ETH'):
            self.assertIsInstance(get_price_info(t), dict)

    def test_trade(self):
        trade()

if __name__ == '__main__':
    main()