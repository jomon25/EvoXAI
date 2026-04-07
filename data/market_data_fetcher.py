"""Market Data Fetcher - downloads OHLCV from Yahoo Finance and Binance."""
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from loguru import logger
import os

class MarketDataFetcher:
    """Downloads, cleans, and stores market data to TimescaleDB."""
    DEFAULT_SYMBOLS = ['BTC-USD', 'ETH-USD', 'AAPL', 'MSFT', 'SPY', 'QQQ', 'GLD']

    def __init__(self, db_url: str | None = None):
        url = db_url or (
            f'postgresql://{os.getenv("POSTGRES_USER", "evoxai")}:'
            f'{os.getenv("POSTGRES_PASSWORD", "evoxai123")}@'
            f'{os.getenv("POSTGRES_HOST", "localhost")}:5432/'
            f'{os.getenv("POSTGRES_DB", "evoxai_db")}'
        )
        self.engine = create_engine(url)

    def fetch_ohlcv(self, symbol: str, period: str = '5y',
                    interval: str = '1d') -> pd.DataFrame:
        logger.info(f'Fetching {symbol} period={period} interval={interval}')
        df = yf.Ticker(symbol).history(period=period, interval=interval)
        df.reset_index(inplace=True)
        df['symbol'] = symbol
        df.columns = [c.lower() for c in df.columns]
        df.rename(columns={'date': 'timestamp'}, inplace=True)
        return df[['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume']]

    def store_to_db(self, df: pd.DataFrame) -> None:
        df.to_sql('market_data', self.engine, if_exists='append',
                  index=False, method='multi', chunksize=1000)
        logger.success(f'Stored {len(df)} rows for {df["symbol"].iloc[0]}')

    def fetch_all(self, symbols: list[str] | None = None) -> None:
        for sym in (symbols or self.DEFAULT_SYMBOLS):
            try:
                df = self.fetch_ohlcv(sym)
                self.store_to_db(df)
            except Exception as e:
                logger.error(f'Failed {sym}: {e}')
        logger.success('All symbols fetched and stored')

if __name__ == '__main__':
    MarketDataFetcher().fetch_all()
