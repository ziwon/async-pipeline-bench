## async-pipeline-bench
Simple pipeline bench related to `async` with some Python frameworks.

simple async code to test:
```python
async def somebody():
   return

async def hello():
   await somebody()
   # return response here in each framework
```

## wrk
Sending http pipeline with wrk:
```
wrk -t10 -c200 -d5s http://127.0.0.1:8080 --latency -s pipeline.lua -- 5
```

## Tl;dr
- As expected, **uvloop with httptools** shows the best performance in python frameworks.
- **aiohttp**, **tornado** successfully processed the http pipeline requests.
- **sanic** and **japronto** failed. (See `error.log` for details.)
- But, the winner is **go-fasthttp**.

### uvloop with httptools
```
Running 5s test @ http://127.0.0.1:8080
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    21.28ms   16.15ms 440.36ms   98.31%
    Req/Sec     2.65k   642.34     7.32k    78.29%
  Latency Distribution
     50%   20.12ms
     75%   26.83ms
     90%   30.30ms
     99%   41.07ms
  132595 requests in 5.08s, 9.74MB read
  Socket errors: connect 0, read 26461, write 0, timeout 0
Requests/sec:  26080.80
Transfer/sec:      1.89MB
```

### aiohttp
```
Running 5s test @ http://127.0.0.1:8080
  10 threads and 200 conneckjjtions
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   156.01ms   81.36ms 997.64ms   82.44%
    Req/Sec   463.88    186.65     1.01k    80.48%
  Latency Distribution
     50%  152.12ms
     75%  203.10ms
     90%  224.45ms
     99%  519.17ms
  21900 requests in 5.09s, 3.40MB read
Requests/sec:   4304.98
Transfer/sec:    685.27KB
```

### tornado
```
Running 5s test @ http://127.0.0.1:8080
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   122.01ms  170.33ms 616.60ms    0.00%
    Req/Sec   217.84     55.44   404.00     80.48%
  Latency Distribution
     50%    0.00us
     75%    0.00us
     90%    0.00us
     99%    0.00us
  10915 requests in 5.09s, 0.96MB read
Requests/sec:   2144.32
Transfer/sec:    192.65KB
```

### sanic
```
Running 5s test @ http://127.0.0.1:8080
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     0.00us    0.00us   0.00us    -nan%
    Req/Sec    51.92     54.90   202.00     91.67%
  Latency Distribution
     50%    0.00us
     75%    0.00us
     90%    0.00us
     99%    0.00us
  200 requests in 5.09s, 25.78KB read
Requests/sec:     39.28
Transfer/sec:      5.06KB
```

### japronto
```
Running 5s test @ http://127.0.0.1:8080
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     0.00us    0.00us   0.00us    -nan%
    Req/Sec     0.00      0.00     0.00      -nan%
  Latency Distribution
     50%    0.00us
     75%    0.00us
     90%    0.00us
     99%    0.00us
  0 requests in 5.10s, 0.00B read
  Socket errors: connect 0, read 123, write 499613, timeout 0
Requests/sec:      0.00
Transfer/sec:       0.00B
```

### go-fasthttp
```
Running 5s test @ http://127.0.0.1:8080
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     4.90ms    3.93ms 213.52ms   92.23%
    Req/Sec    15.64k     3.10k   45.50k    83.47%
  Latency Distribution
     50%    4.30ms
     75%    6.37ms
     90%    8.35ms
     99%   13.41ms
  781050 requests in 5.07s, 109.50MB read
Requests/sec: 154092.25
Transfer/sec:     21.60MB
```
