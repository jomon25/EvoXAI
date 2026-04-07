import streamlit as st, pandas as pd, numpy as np
from datetime import datetime

st.set_page_config(page_title='EvoXAI Dashboard', layout='wide', page_icon='🧬')
st.title('🧬 EvoXAI - Evolutionary + Explainable Trading System')

# -- KPI row --
c1, c2, c3, c4 = st.columns(4)
c1.metric('Active Strategies', '247', '+12')
c2.metric('Sharpe Ratio (30d)', '1.82', '+0.15')
c3.metric('Max Drawdown', '6.2%', '-1.1%')
c4.metric('Drift Alerts Today', '2', '')

# -- Equity curve --
st.subheader('🧬 Portfolio Equity Curve')
eq = pd.DataFrame(np.random.randn(200).cumsum() + 10000, columns=['Equity ($)'])
st.line_chart(eq)

# -- Explanation --
st.subheader('🧬 Last Trade Explanation')
st.info('BUY signal: primary driver is RSI elevated (weight 0.45); '
        'supported by Volume elevated (0.30) and ATR suppressed (0.15). '
        'Model confidence: 82%.')

# -- Top strategies --
st.subheader('🧬 Top Performing Strategies')
df = pd.DataFrame({
    'ID': ['SMC-001', 'ICT-047', 'SNR-012', 'SW-089'],
    'Style': ['SMC', 'ICT', 'SnR', 'Swing'],
    'Sharpe': [2.14, 1.93, 1.78, 1.65],
    'Win%': ['59%', '55%', '53%', '51%'],
    'Generation': [14, 11, 8, 6]
})
st.dataframe(df, use_container_width=True)

# -- Evolution --
st.subheader('🧬 Evolution Progress')
gen_df = pd.DataFrame({'Best Sharpe': np.random.uniform(0.8, 2.2, 20).cummax()},
                      index=range(1, 21))
gen_df.index.name = 'Generation'
st.line_chart(gen_df)

# -- Regime --
st.subheader('🧬 Current Market Regime')
st.success('Bull Trend - probability 72%. Strategy pool biased towards Swing style.')
st.caption(f'Last updated: {datetime.now():%Y-%m-%d %H:%M:%S}')
