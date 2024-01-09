# 표준
import os
# 서드파티
import pandas as pd
from pyupbit import Upbit, get_current_price
# 커스텀
from src.utils import get_logger
from src.data import get_price_info
from src.model import get_pred

client = Upbit(
    os.getenv('UPBIT_AK'),
    os.getenv('UPBIT_SK'),
)

logger = get_logger('account')
tickers = ('KRW', 'BTC', 'ETH', 'SOL', 'XRP', 'ADA', 'AVAX')

def get_account_balance(total=False) -> pd.DataFrame:
    '''계정 자산 목록 및 합계'''
    df = pd.DataFrame([dict(
            symbol=t,
            price=get_current_price(f'KRW-{t}') if t != 'KRW' else 1,
            volume=client.get_balance(t))
        for t in tickers])
    if total:
        s = (df['price'] * df['volume']).sum()
        logger.info(s)
        return s 
    logger.info('\n' + df.to_string())
    return df.set_index('symbol')

def trade():
    '''거래 로직'''
    balance = get_account_balance()
    total = get_account_balance(total=True)
    for t in tickers[1:]:
        logger.info(f'{t} 모니터링')
        pred = get_pred(t)
        info = get_price_info(t)
        logger.debug(pred)
        logger.debug(info)
        prev = info.get('prev')
        curr = info.get('curr')
        risk = info.get('risk')
        vol = balance.loc[t]['volume']
        ticker = f'KRW-{t}'
        if  vol > 0:
            logger.info(f'{t} 잔고 있음')
            exit1 = pred.get('exit1')
            if ((exit1 < prev) and (exit1 > curr)):
                logger.info(f'{t} 추세추종 청산 (저점돌파)')
                client.sell_market_order(ticker, vol)
                continue
            exit2 = pred.get('exit2')
            if ((exit2 > prev) and (exit2 < curr)):
                logger.info(f'{t} 평균회귀 청산 (고평가)')
                client.sell_market_order(ticker, vol)
                continue
        else:
            logger.info(f'{t} 잔고 없음')
            enter1 = pred.get('enter1')
            if ((enter1 > prev) and (enter1 < curr)):
                logger.info(f'{t} 추세추종 진입 (고점돌파)')
                client.buy_market_order(ticker, risk * total)
                continue
            enter2 = pred.get('enter2')
            if ((enter2 < prev) and (enter2 > curr)):
                logger.info(f'{t} 평균회귀 진입 (저평가)')
                client.buy_market_order(ticker, risk * total)
                continue
        logger.info(f'{t} 포지션 유지')