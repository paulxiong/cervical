// Package rectangle provides a imageserver/image.Processor implementation that allows to draw rectangle on Image.
package rectangle

import (
	"image"
	"image/color"
	"image/draw"

	"github.com/pierrre/imageserver"
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
	return bds, nil
}

// NewDrawable returns a new draw.Image with the same type and size as p.
//
// If p has no size, 1x1 is used.
//
// See NewDrawableSize.
func NewDrawable(p image.Image) draw.Image {
	r := p.Bounds()
	if _, ok := p.(*image.Uniform); ok {
		r = image.Rect(0, 0, 1, 1)
	}
	return NewDrawableSize(p, r)
}

// NewDrawableSize returns a new draw.Image with the same type as p and the given bounds.
//
// If p is not a draw.Image, another type is used.
//
// nolint: gocyclo
func NewDrawableSize(p image.Image, r image.Rectangle) draw.Image {
	switch p := p.(type) {
	case *image.RGBA:
		return image.NewRGBA(r)
	case *image.RGBA64:
		return image.NewRGBA64(r)
	case *image.NRGBA:
		return image.NewNRGBA(r)
	case *image.NRGBA64:
		return image.NewNRGBA64(r)
	case *image.Alpha:
		return image.NewAlpha(r)
	case *image.Alpha16:
		return image.NewAlpha16(r)
	case *image.Gray:
		return image.NewGray(r)
	case *image.Gray16:
		return image.NewGray16(r)
	case *image.Paletted:
		pl := make(color.Palette, len(p.Palette))
		copy(pl, p.Palette)
		return image.NewPaletted(r, pl)
	case *image.CMYK:
		return image.NewCMYK(r)
	default:
		return image.NewRGBA(r)
	}
}

// Copy copies src to dst.
func Copy(dst draw.Image, src image.Image) {
	bd := src.Bounds().Intersect(dst.Bounds())
	at := imageutil.NewAtFunc(src)
	set := imageutil.NewSetFunc(dst)
	imageutil.Parallel1D(bd, func(bd image.Rectangle) {
		for y := bd.Min.Y; y < bd.Max.Y; y++ {
			for x := bd.Min.X; x < bd.Max.X; x++ {
				r, g, b, a := at(x, y)
				set(x, y, r, g, b, a)
			}
		}
	})
}

func drawrect(bds image.Rectangle, img image.Image, thickness int) (newimg image.Image) {
	out := NewDrawable(img)
	bdout := img.Bounds().Intersect(out.Bounds())
	at := imageutil.NewAtFunc(img)
	set := imageutil.NewSetFunc(out)

	if bds.Max.Y > bdout.Max.Y || bds.Max.X > bdout.Max.X {
		return img
	}

	imageutil.Parallel1D(bdout, func(bd image.Rectangle) {
		for y := bd.Min.Y; y < bd.Max.Y; y++ {
			for x := bd.Min.X; x < bd.Max.X; x++ {
				r, g, b, a := at(x, y)
				set(x, y, r, g, b, a)
			}
		}
	})

	imageutil.Parallel1D(bds, func(bd image.Rectangle) {
		for y := bd.Min.Y; y < bd.Max.Y; y++ {
			for x := bd.Min.X; x < bd.Max.X; x++ {
				if x >= bds.Min.X+thickness && x < bds.Max.X-thickness && y >= bds.Min.Y+thickness && y < bds.Max.Y-thickness {
					continue
				}
				r, g, b, a := uint32(64971), uint32(299), uint32(549), uint32(65535)
				set(x, y, r, g, b, a)
			}
		}
	})
	return out
}

func (prc *Processor) rectangle(im image.Image, bds image.Rectangle) (image.Image, error) {
	type SubImage interface {
		image.Image
		SubImage(image.Rectangle) image.Image
	}
	newimg := drawrect(bds, im, 2)
	return newimg, nil
}

// Change implements imageserver/image.Processor.
func (prc *Processor) Change(params imageserver.Params) bool {
	return params.Has(param)
}
