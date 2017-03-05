package main

import "github.com/valyala/fasthttp"
import "github.com/magicdawn/go-co"

func somebody() *co.Task {
	return co.Async(func() interface{} {
		return nil
	})
}

func hello(ctx *fasthttp.RequestCtx) {
	co.Await(somebody())
	ctx.WriteString("Hello world!")
}

func main() {
	fasthttp.ListenAndServe("0.0.0.0:8080", hello)
}
