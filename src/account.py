# 표준
import os
# 서드파티
import pandas as pd
from pyupbit import Upbit, get_current_price
# 커스텀
from src.utils import get_logger
from src.data import get_price_info
from src.model import get_pred
from src.telegram import send_message

client = Upbit(
    os.getenv('UPBIT_AK'),
    os.getenv('UPBIT_SK'),
)

logger = get_logger('account')
# tickers = ('KRW', 'BTC', 'ETH', 'SOL', 'XRP', 'ADA', 'AVAX')
tickers = ('KRW', 'BTC', 'ETH')

def get_account_balance(total=False) -> pd.DataFrame:
    '''계정 자산 목록 및 합계'''
    df = pd.DataFrame([dict(
            symbol=t,
            price=get_current_price(f'KRW-{t}') if t != 'KRW' else 1,
            volume=client.get_balance(t))
        for t in tickers])
    if total:
        s = (df['price'] * df['volume']).sum()
        send_message(f'보유총액 : ₩{s:,.3f}')
        logger.info(s)
        return s 
    logger.info('\n' + df.to_string())
    send_message(df)
    return df.set_index('symbol')

def trade():
    '''거래 로직'''
    send_message('🔮')
    balance = get_account_balance()
    total = get_account_balance(total=True)
    for t in tickers[1:]:
        msg = f'{t} 모니터링'
        logger.info(msg); send_message(f'👀 {msg}')
        pred = get_pred(t)
        info = get_price_info(t, target_risk=0.02)
        logger.debug(pred)
        logger.debug(info)
        prev = info.get('prev')
        curr = info.get('curr')
        risk = info.get('risk')
        send_message(f'☔️ 리스크 : {risk*100:.3f}%')
        vol = balance.loc[t]['volume']
        ticker = f'KRW-{t}'
        if  vol > 0:
            logger.info(f'{t} 잔고 있음')
            exit1 = pred.get('exit1')
            if ((exit1 < prev) and (exit1 > curr)):
                msg = f'{t} 추세추종 청산 (저점돌파)'
                logger.info(msg); send_message(f'🐻 {msg}')
                client.sell_market_order(ticker, vol)
                continue
            exit2 = pred.get('exit2')
            if ((exit2 > prev) and (exit2 < curr)):
                msg = f'{t} 평균회귀 청산 (고평가)'
                logger.info(msg); send_message(f'🐻 {msg}')
                client.sell_market_order(ticker, vol)
                continue
        else:
            logger.info(f'{t} 잔고 없음')
            enter1 = pred.get('enter1')
            if ((enter1 > prev) and (enter1 < curr)):
                msg = f'{t} 추세추종 진입 (고점돌파)'
                logger.info(msg); send_message(f'🐮 {msg}')
                client.buy_market_order(ticker, risk * total)
                continue
            enter2 = pred.get('enter2')
            if ((enter2 < prev) and (enter2 > curr)):
                msg = f'{t} 평균회귀 진입 (저평가)'
                logger.info(msg); send_message(f'🐮 {msg}')
                client.buy_market_order(ticker, risk * total)
                continue
        msg = f'{t} 포지션 유지'
        logger.info(msg); send_message(f'📌 {msg}')