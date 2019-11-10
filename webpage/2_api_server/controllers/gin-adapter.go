package controllers

import (
	"context"
	"net/http"

	"github.com/gin-gonic/gin"
)

// New returns a handler to be passed to middleware which will ensure
// the next handler in the chain is called correctly, along with
// a function that wraps the middleware's handler into a gin.HandlerFunc
// to be passed to Engine.Use.
//
// If the middleware does not call the handler it's wrapping, Abort is
// called on the Gin context.
func New() (http.Handler, func(h http.Handler) gin.HandlerFunc) {
	nextHandler := new(connectHandler)
	makeGinHandler := func(h http.Handler) gin.HandlerFunc {
		return func(c *gin.Context) {
			state := &middlewareCtx{ctx: c}
			ctx := context.WithValue(c.Request.Context(), nextHandler, state)
			h.ServeHTTP(c.Writer, c.Request.WithContext(ctx))
			if !state.childCalled {
				c.Abort()
			}
		}
	}
	return nextHandler, makeGinHandler
}

// Wrap takes the common HTTP middleware function signature, calls it to generate
// a handler, and wraps it into a Gin middleware handler.
//
// This is just a convenience wrapper around New.
func Wrap(f func(h http.Handler) http.Handler) gin.HandlerFunc {
	next, adapter := New()
	return adapter(f(next))
}

type connectHandler struct{}

// pull Gin's context from the request context and call the next item
// in the chain.
func (h *connectHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	state := r.Context().Value(h).(*middlewareCtx)
	defer func(r *http.Request) { state.ctx.Request = r }(state.ctx.Request)
	state.ctx.Request = r
	state.childCalled = true
	state.ctx.Next()
}

type middlewareCtx struct {
	ctx         *gin.Context
	childCalled bool
}