# 표준
from unittest import TestCase, main, skip
# 커스텀
from src.utils import check_ip
from src.data import get_price_hourly
from src.model import forecast_with_config, get_pred

class LogicTests(TestCase):
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
    
    def test_get_pred(self):
        for t in ('BTC', 'ETH'):
            pred = get_pred(t)
            self.assertIsInstance(pred, dict)

if __name__ == '__main__':
    main()