// Package rectangle provides a imageserver/image.Processor implementation that allows to draw rectangle on Image.
package rectangle

import (
	"fmt"
	"image"

	"github.com/pierrre/imageserver"
	imageserver_image_internal "github.com/pierrre/imageserver/image/internal"
	"github.com/pierrre/imageutil"
)

const param = "rect"

// Processor is a imageserver/image.Processor implementation that allows to draw rectangle on Image
//
// All params are extracted from the "rect" node param and are mandatory:
//  - min_x: top-left X
//  - min_y: top-left Y
//  - max_x: bottom-right X
//  - max_y: bottom-right Y
type Processor struct{}

// Process implements imageserver/image.Processor.
func (prc *Processor) Process(im image.Image, params imageserver.Params) (image.Image, error) {
	if !params.Has(param) {
		return im, nil
	}
	params, err := params.GetParams(param)
	if err != nil {
		return nil, err
	}
	im, err = prc.process(im, params)
	if err != nil {
		if err, ok := err.(*imageserver.ParamError); ok {
			err.Param = param + "." + err.Param
		}
		return nil, err
	}
	return im, nil
}

func (prc *Processor) process(im image.Image, params imageserver.Params) (image.Image, error) {
	bds, err := prc.getBounds(params)
	if err != nil {
		return nil, err
	}
	return prc.rectangle(im, bds)
}

func (prc *Processor) getBounds(params imageserver.Params) (image.Rectangle, error) {
	var bds image.Rectangle
	var err error
	bds.Min.X, err = params.GetInt("min_x")
	if err != nil {
		return image.ZR, err
	}
	bds.Min.Y, err = params.GetInt("min_y")
	if err != nil {
		return image.ZR, err
	}
	bds.Max.X, err = params.GetInt("max_x")
	if err != nil {
		return image.ZR, err
	}
	bds.Max.Y, err = params.GetInt("max_y")
	if err != nil {
		return image.ZR, err
	}
	fmt.Printf("x1=%d x2=%d y1=%d y2=%d\n", bds.Min.X, bds.Max.X, bds.Min.Y, bds.Max.Y)
	return bds, nil
}

func drawrect(x1, y1, x2, y2, thickness int, img *image.Image) {
	// col := color.RGBA{255, 0, 0, 255}

	// for t := 0; t < thickness; t++ {
	// 	// draw horizontal lines
	// 	for x := x1; x <= x2; x++ {
	// 		img.Set(x, y1+t, col)
	// 		img.Set(x, y2-t, col)
	// 	}
	// 	// draw vertical lines
	// 	for y := y1; y <= y2; y++ {
	// 		img.Set(x1+t, y, col)
	// 		img.Set(x2-t, y, col)
	// 	}
	// }
}

func (prc *Processor) rectangle(im image.Image, bds image.Rectangle) (image.Image, error) {
	fmt.Println("rectangle")
	type SubImage interface {
		image.Image
		SubImage(image.Rectangle) image.Image
	}
	fmt.Println(bds)
	// im2, ok := im.(SubImage)
	// if !ok {
	// 	return nil, &imageserver.ImageError{
	// 		Message: fmt.Sprintf("rectangle: image type %T not supported: method SubImage not found", im),
	// 	}
	// }
	// drawrect(im.RGBA)

	out := imageserver_image_internal.NewDrawable(im)
	bd := nim.Bounds().Intersect(out.Bounds())
	at := imageutil.NewAtFunc(nim)
	set := imageutil.NewSetFunc(out)
	imageutil.Parallel1D(bd, func(bd image.Rectangle) {
		for y := bd.Min.Y; y < bd.Max.Y; y++ {
			for x := bd.Min.X; x < bd.Max.X; x++ {
				r, g, b, a := at(x, y)
				r, g, b, a = imageutil.RGBAToNRGBA(r, g, b, a)
				r = uint32(prc.vals[uint16(r)])
				g = uint32(prc.vals[uint16(g)])
				b = uint32(prc.vals[uint16(b)])
				r, g, b, a = imageutil.NRGBAToRGBA(r, g, b, a)
				set(x, y, r, g, b, a)
			}
		}
	})
	return im, nil
}

// Change implements imageserver/image.Processor.
func (prc *Processor) Change(params imageserver.Params) bool {
	return params.Has(param)
}
