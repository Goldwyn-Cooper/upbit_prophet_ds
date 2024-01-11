# 표준
import logging
import os
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as rd
# 서드파티
import requests
import yaml

def get_yaml(fname: str):
    '''YAML 파일 읽기'''
    with open(fname) as f:
        y = yaml.load(f, Loader=yaml.FullLoader)
    return y

def get_logger(name):
    '''LOGGER 가져오기'''
    logger = logging.getLogger(name)
    level = int(get_yaml('/home/ubuntu/upbit_prophet_ds/config.yml')
                .get('logger', {})
                .get(name, '20'))
    logger.setLevel(level)
    if not logger.handlers:
        hdlr = logging.StreamHandler()
        fmt = logging.Formatter(
            '%(asctime)s:%(module)s:[%(levelname)s]:%(message)s',
            '%y-%m-%d %H:%M:%S')
        hdlr.setFormatter(fmt)
        logger.addHandler(hdlr)
    return logger

logger = get_logger('utils')

def check_ip():
    '''UPBIT API 인증을 위한 IP 확인'''
    URL = 'https://ifconfig.me'
    ip = requests.get(URL).text
    logger.info(ip)
    return ip

def get_from_dt(**kwargs):
    '''현재 UTC 시간을 기반으로 이동한 dt 제공'''
    utcnow_dt = dt.utcnow()
    kstnow_dt = utcnow_dt + rd(**kwargs)
    kstnow_str = kstnow_dt.strftime('%Y-%m-%d %H:%M:00')
    logger.debug(kstnow_str)
    return dt.strptime(kstnow_str, '%Y-%m-%d %H:%M:00')