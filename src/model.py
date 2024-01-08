# 표준
import logging
# 서드파티
import pandas as pd
from prophet import Prophet
# 커스텀
from src.data import get_price_hourly
from src.utils import get_logger, get_yaml

logger = get_logger('model')

def get_pred(ticker) -> dict:
    '''가격 예측 결과 제공'''
    logger.info(f'{ticker} Enter & Exit Prediction START')
    pred = {}
    for y in ('high', 'low'):
        fcst = forecast_with_config(ticker, y)
        if y == 'high':
            pred['enter1'] = fcst['yhat'].iloc[-1] # 예상고점 돌파로 인한 진입
            pred['exit2'] = fcst['yhat_upper'].iloc[-1] # 고평가로 인한 청산
            continue
        if y == 'low':
            pred['exit1'] = fcst['yhat'].iloc[-1] # 예상저점 돌파로 인한 진입
            pred['enter2'] = fcst['yhat_lower'].iloc[-1] # 저평가로 인한 청산
            continue
    logger.info(f'{ticker} Enter & Exit Prediction DONE')
    logger.debug(pred)
    return pred

def forecast_with_config(
        ticker:str,
        y_col:str,
    ) -> pd.DataFrame:
    '''하이퍼패러미터을 적용한 prophet으로 예측 진행'''
    logging.getLogger('cmdstanpy').setLevel(logging.ERROR)
    logger.info(f'{ticker} {y_col}')
    yaml : dict = get_yaml('config.yml')
    # 데이터
    days = int(yaml.get('params').get('days'))
    logger.debug(days)
    price = get_price_hourly(ticker, days)
    regs = ['value', 'tr']
    df = price.loc[:, [y_col, *regs]]\
        .reset_index()\
        .rename(columns={'index': 'ds', y_col: 'y'})
    df['ds'] = pd.to_datetime(df['ds'])
    # 모델링
    config = yaml.get('params', {}).get(ticker, {})
    m = Prophet(**config, yearly_seasonality=False)
    for reg in regs:
        m.add_regressor(reg)
    m.fit(df.head(len(df) - 1))
    # 예측
    future = m.make_future_dataframe(periods=1, freq='H')
    for reg in regs:
        future[reg] = df[reg]
    fcst = m.predict(future)
    logger.debug(fcst.tail())
    return fcst