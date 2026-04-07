# research/backtest.jl
# Install: ]add DataFrames Statistics HTTP JSON3 Plots
using DataFrames, Statistics

struct Backtester
    capital::Float64
    commission::Float64
end

function run_backtest(data::DataFrame, strategy::Function, bt::Backtester)
    equity = Float64[]
    cash = bt.capital
    pos = 0.0
    
    for row in eachrow(data)
        signal = strategy(row)
        if signal > 0 && pos == 0.0
            pos = cash / row.close * (1 - bt.commission)
            cash = 0.0
        elseif signal < 0 && pos > 0.0
            cash = pos * row.close * (1 - bt.commission)
            pos = 0.0
        end
        push!(equity, cash + pos * row.close)
    end
    
    rets = diff(equity) ./ equity[1:end-1]
    sharpe = mean(rets) / (std(rets) + 1e-9) * sqrt(252)
    return (equity=equity, sharpe=sharpe)
end
