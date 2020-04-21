package function

import (
	"fmt"
	"time"
)

// Getbidmid 生成新的BID
func Getbidmid() (string, string) {
	ts := time.Now()
	year, mon, day := ts.Date()
	hour, min, sec := ts.Clock()
	ms := ts.Nanosecond() / 1000 / 1000
	bid := fmt.Sprintf("b%04d%02d%02d", year, mon, day)
	mid := fmt.Sprintf("m%02d%02d%02d%04d", hour, min, sec, ms)
	return bid, mid
}
