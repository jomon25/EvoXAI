package matching

import (
    "container/heap"
    "sync"
)

type Trade struct {} 

type Order struct {
    ID      string
    Price   float64
    Qty     float64
    Side    string // 'buy' | 'sell'
    StratID string
}

type PriorityQueue []*Order
func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].Price < pq[j].Price }
func (pq PriorityQueue) Swap(i, j int) { pq[i], pq[j] = pq[j], pq[i] }
func (pq *PriorityQueue) Push(x interface{}) { *pq = append(*pq, x.(*Order)) }
func (pq *PriorityQueue) Pop() interface{} {
    old := *pq
    n := len(old)
    item := old[n-1]
    *pq = old[0 : n-1]
    return item
}

type OrderBook struct {
    mu   sync.RWMutex
    bids PriorityQueue // max-heap
    asks PriorityQueue // min-heap
}

func (ob *OrderBook) AddOrder(o *Order) []*Trade {
    ob.mu.Lock()
    defer ob.mu.Unlock()

    if o.Side == "buy" {
        return ob.matchBuy(o)
    }
    return ob.matchSell(o)
}

func (ob *OrderBook) matchBuy(o *Order) []*Trade { return nil }
func (ob *OrderBook) matchSell(o *Order) []*Trade { return nil }
