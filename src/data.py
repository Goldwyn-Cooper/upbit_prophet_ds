# 서드파티
import pandas as pd
from pyupbit import get_ohlcv_from, get_ohlcv
# 커스텀
from src.utils import get_logger, get_from_dt

logger = get_logger('data')

def get_price_info(ticker, target_risk=0.01) -> dict:
    logger.info(f'{ticker}')
    hours : pd.DataFrame = get_ohlcv(f'KRW-{ticker}', 'minute60', 24)\
        .loc[:, ['high', 'low']]
    logger.debug('\n' + hours.tail().to_string())
    min10 : pd.DataFrame = get_ohlcv(f'KRW-{ticker}', 'minute10', 2)\
        .loc[:, 'close']
    logger.debug('\n' + min10.to_string())
    prev = min10.iloc[-2]
    curr = min10.iloc[-1]
    aatr = (hours['high'] - hours['low']).ewm(24).mean().iloc[-1] / curr
    risk = target_risk*2/24/aatr
    info = dict(prev=prev, curr=curr, risk=risk)
    logger.debug(info)
    return info

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