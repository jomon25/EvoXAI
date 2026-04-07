use tokio::time::{interval, Duration};
use std::time::Instant;

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct Tick {
    pub symbol: String,
    pub price: f64,
    pub volume: f64,
    pub ts_ns: u128, // nanosecond timestamp
}

pub struct MarketDataFeed {
    tx: crossbeam::channel::Sender<Tick>,
}

impl MarketDataFeed {
    #[inline(always)]
    pub fn process_tick(&self, tick: Tick) {
        let start = Instant::now();
        self.tx.send(tick).ok();
        // Target: < 500ns per tick
        debug_assert!(start.elapsed().as_nanos() < 1000);
    }
}

fn main() {
    println!("Rust market data feed service initialized.");
}
