CREATE EXTENSION IF NOT EXISTS timescaledb;

-- OHLCV hypertable partitioned by time
CREATE TABLE market_data (
    symbol TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    open DECIMAL(16,8),
    high DECIMAL(16,8),
    low DECIMAL(16,8),
    close DECIMAL(16,8),
    volume DECIMAL(24,4),
    PRIMARY KEY (symbol, timestamp)
);

SELECT create_hypertable('market_data', 'timestamp');

-- Computed features
CREATE TABLE features (
    symbol TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    feature_name TEXT NOT NULL,
    value DECIMAL(16,8),
    PRIMARY KEY (symbol, timestamp, feature_name)
);

-- Detected market regimes
CREATE TABLE regimes (
    symbol TEXT NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ,
    regime_id INTEGER,
    regime_name TEXT,
    probability DECIMAL(6,5),
    PRIMARY KEY (symbol, start_time)
);

-- Strategy DNA store
CREATE TABLE strategies (
    id UUID PRIMARY KEY,
    style TEXT NOT NULL,
    timeframe TEXT,
    dna_json JSONB NOT NULL,
    sharpe DECIMAL(8,4),
    max_drawdown DECIMAL(6,4),
    win_rate DECIMAL(6,4),
    generation INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Causal explanations per trade
CREATE TABLE trade_explanations (
    trade_id UUID PRIMARY KEY,
    strategy_id UUID REFERENCES strategies(id),
    symbol TEXT,
    decision TEXT,
    shap_json JSONB,
    causal_json JSONB,
    explanation TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX ON market_data (symbol, timestamp DESC);
CREATE INDEX ON strategies (style, sharpe DESC);
CREATE INDEX ON strategies (generation);
