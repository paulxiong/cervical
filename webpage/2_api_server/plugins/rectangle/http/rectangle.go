// Package rectangle provides a imageserver/http.Parser implementation for imageserver/image/rect.Processor.
package rectangle

import (
	"fmt"
	"net/http"
	"strings"

	"github.com/pierrre/imageserver"
)

const param = "rect"

// Parser is a imageserver/http.Parser implementation for imageserver/image/rectangle.Processor.
//
// It uses the "rectangle" param in the query string, with the following format: min_x,min_y|max_x,max_y
type Parser struct{}

// Parse implements imageserver/http.Parser.
func (prs *Parser) Parse(req *http.Request, params imageserver.Params) error {
	rectangle := req.URL.Query().Get(param)
	if rectangle == "" {
		return nil
	}
	var minX, minY, maxX, maxY int
	_, err := fmt.Sscanf(rectangle, "%d,%d|%d,%d", &minX, &minY, &maxX, &maxY)
	if err != nil {
		return &imageserver.ParamError{
			Param:   param,
			Message: fmt.Sprintf("expected format '<int>,<int>|<int>,<int>': %s", err),
		}
	}
	params.Set(param, imageserver.Params{
		"min_x": minX,
		"min_y": minY,
		"max_x": maxX,
		"max_y": maxY,
	})
	return nil
}

// Resolve implements imageserver/http.Parser.
func (prs *Parser) Resolve(p string) (httpParam string) {
	if p == param || strings.HasPrefix(p, param+".") {
		return param
	}
	return ""
}
