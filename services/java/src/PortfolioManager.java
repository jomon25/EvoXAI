import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicReference;

public class PortfolioManager {
    private final double maxDailyLoss;
    private final double maxPositionSize;
    private final AtomicReference<Double> dailyPnL = new AtomicReference<>(0.0);
    private final ConcurrentHashMap<String, Double> positions = new ConcurrentHashMap<>();

    public PortfolioManager(double maxDailyLoss, double maxPositionSize) {
        this.maxDailyLoss = maxDailyLoss;
        this.maxPositionSize = maxPositionSize;
    }

    public synchronized boolean canTrade(String symbol, double size, double price) {
        double exposure = positions.getOrDefault(symbol, 0.0);
        if (exposure + size * price > maxPositionSize) return false;
        
        if (dailyPnL.get() < -maxDailyLoss) {
            System.err.println("Circuit breaker: daily loss limit reached");
            return false;
        }
        return true;
    }

    public void updatePosition(String symbol, double qty, double pnl) {
        positions.merge(symbol, qty, Double::sum);
        dailyPnL.updateAndGet(v -> v + pnl);
    }
}
