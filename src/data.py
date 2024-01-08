# 서드파티
import pandas as pd
from pyupbit import get_ohlcv_from
# 커스텀
from src.utils import get_logger, get_from_dt

logger = get_logger('data')

def get_price_hourly(ticker:str, count:int) -> pd.DataFrame:
    '''티커(`ticker`)로 `count`개의 데이터 가져오기'''
    logger.info(f'{ticker} {count}')
    from_dt = get_from_dt(hours=-count-24)
    ohlcv : pd.DataFrame = get_ohlcv_from(
        ticker=f'KRW-{ticker}',
        interval="minute60",
        fromDatetime=from_dt)
    ohlcv['tr'] = ohlcv['high'] - ohlcv['low']
    logger.debug(ohlcv.tail())
    logger.info(f'len(ohlcv) = {len(ohlcv)}')
    col = ('high', 'low', 'value', 'tr')
    return ohlcv.loc[:, col].tail(count+1)