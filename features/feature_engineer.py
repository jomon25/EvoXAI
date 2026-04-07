"""Computes 50+ technical indicators for each OHLCV bar."""
import pandas as pd
import numpy as np


class FeatureEngineer:
    def add_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # ── Robust column normalization (handles yfinance MultiIndex) ──
        # yfinance >=0.2 returns MultiIndex like ('Close', 'BTC-USD')
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [str(c[0]).lower() for c in df.columns]
        else:
            df.columns = [str(c).lower() for c in df.columns]

        # --- Trend ---
        for w in [5, 10, 20, 50, 200]:
            df[f'sma_{w}'] = df['close'].rolling(w).mean()
        for span in [9, 12, 26, 50]:
            df[f'ema_{span}'] = df['close'].ewm(span=span, adjust=False).mean()

        # --- MACD ---
        df['macd'] = df['ema_12'] - df['ema_26']
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']

        # --- RSI ---
        delta = df['close'].diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        df['rsi_14'] = 100 - (100 / (1 + gain / loss.replace(0, 1e-9)))

        # --- Bollinger Bands ---
        bb_mid = df['close'].rolling(20).mean()
        bb_std = df['close'].rolling(20).std()
        df['bb_mid'] = bb_mid
        df['bb_upper'] = bb_mid + 2 * bb_std
        df['bb_lower'] = bb_mid - 2 * bb_std
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / bb_mid

        # --- ATR ---
        hl = df['high'] - df['low']
        hc = (df['high'] - df['close'].shift()).abs()
        lc = (df['low'] - df['close'].shift()).abs()
        df['atr_14'] = pd.concat([hl, hc, lc], axis=1).max(axis=1).rolling(14).mean()

        # --- Volume ---
        df['volume_sma_20'] = df['volume'].rolling(20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma_20']
        df['obv'] = (np.sign(df['close'].diff()) * df['volume']).cumsum()

        # --- Volatility & returns ---
        df['returns'] = df['close'].pct_change()
        df['log_return'] = np.log(df['close'] / df['close'].shift())
        df['volatility_20'] = df['returns'].rolling(20).std()

        # --- Price position (0-1 in N-day range) ---
        lo20 = df['low'].rolling(20).min()
        hi20 = df['high'].rolling(20).max()
        df['price_position'] = (df['close'] - lo20) / (hi20 - lo20 + 1e-9)

        return df.dropna()
