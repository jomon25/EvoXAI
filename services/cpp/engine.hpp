#pragma once
#include <vector>
#include <chrono>
#include <numeric>
#include <spdlog/spdlog.h>

struct Tick { double open, high, low, close, volume; long long ts_ns; };
struct TradeResult { double pnl, max_dd, sharpe; int n_trades; };

class CPPBacktester {
    double capital_;
    std::vector<double> equity_;

public:
    explicit CPPBacktester(double cap = 10000.0) : capital_(cap) {}

    TradeResult run(const std::vector<Tick>& ticks, auto strategy_fn) {
        equity_.clear();
        double pos = 0.0, cash = capital_;

        for (const auto& t : ticks) {
            double signal = strategy_fn(t);
            if (signal > 0 && pos == 0.0) {
                pos = cash / t.close;
                cash = 0.0;
            } else if (signal < 0 && pos > 0.0) {
                cash = pos * t.close;
                pos = 0.0;
            }
            equity_.push_back(cash + pos * t.close);
        }

        return compute_metrics();
    }

private:
    TradeResult compute_metrics() { /* Sharpe, drawdown calc */ return {}; }
};
