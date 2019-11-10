package controllers

import (
	"crypto/sha256"
	"image"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
	"runtime"
	"time"

	"github.com/disintegration/gift"
	"github.com/pierrre/imageserver"

	imageserver_cache "github.com/pierrre/imageserver/cache"
	imageserver_cache_file "github.com/pierrre/imageserver/cache/file"
	imageserver_cache_memory "github.com/pierrre/imageserver/cache/memory"
	imageserver_http "github.com/pierrre/imageserver/http"
	imageserver_http_crop "github.com/pierrre/imageserver/http/crop"
	imageserver_http_gamma "github.com/pierrre/imageserver/http/gamma"
	imageserver_http_gift "github.com/pierrre/imageserver/http/gift"
	imageserver_http_image "github.com/pierrre/imageserver/http/image"
	imageserver_image "github.com/pierrre/imageserver/image"
	imageserver_image_crop "github.com/pierrre/imageserver/image/crop"
	imageserver_image_gamma "github.com/pierrre/imageserver/image/gamma"
	imageserver_image_gif "github.com/pierrre/imageserver/image/gif"
	imageserver_image_gift "github.com/pierrre/imageserver/image/gift"

	// 支持的图片格式
	_ "github.com/pierrre/imageserver/image/bmp"
	_ "github.com/pierrre/imageserver/image/jpeg"
	_ "github.com/pierrre/imageserver/image/png"
	_ "github.com/pierrre/imageserver/image/tiff"
)

const (
	maxWidth     = 4096
	maxHeight    = 4096
	dirName      = "upload"
	cachedir     = "cache"
	memCacheSize = int64(128 * (1 << 20))
)

func newServer() imageserver.Server {
	srv := getImgServer()
	srv = newServerImage(srv)
	srv = newServerFile(srv)
	srv = newServerLimit(srv)
	srv = newServerCacheMemory(srv)
	return srv
}

func newServerImage(srv imageserver.Server) imageserver.Server {
	basicHdr := &imageserver_image.Handler{
		Processor: imageserver_image_gamma.NewCorrectionProcessor(
			imageserver_image.ListProcessor([]imageserver_image.Processor{
				&imageserver_image_crop.Processor{},
				&imageserver_image_gift.RotateProcessor{
					DefaultInterpolation: gift.CubicInterpolation,
				},
				&imageserver_image_gift.ResizeProcessor{
					DefaultResampling: gift.LanczosResampling,
					MaxWidth:          maxWidth,
					MaxHeight:         maxHeight,
				},
			}),
			true,
		),
	}
	gifHdr := &imageserver_image_gif.FallbackHandler{
		Handler: &imageserver_image_gif.Handler{
			Processor: &imageserver_image_gif.SimpleProcessor{
				Processor: imageserver_image.ListProcessor([]imageserver_image.Processor{
					&imageserver_image_crop.Processor{},
					&imageserver_image_gift.RotateProcessor{
						DefaultInterpolation: gift.NearestNeighborInterpolation,
					},
					&imageserver_image_gift.ResizeProcessor{
						DefaultResampling: gift.NearestNeighborResampling,
						MaxWidth:          maxWidth,
						MaxHeight:         maxHeight,
					},
				}),
			},
		},
		Fallback: basicHdr,
	}
	return &imageserver.HandlerServer{
		Server:  srv,
		Handler: gifHdr,
	}
}

//根据请求返回本地图片
func getImgServer() imageserver.Server {
	return imageserver.Server(imageserver.ServerFunc(func(params imageserver.Params) (*imageserver.Image, error) {
		source, err := params.GetString("source")
		if err != nil {
			return nil, err
		}
		filePath := filepath.Join(dirName, source)
		data, err := os.Open(filePath)
		if err != nil {
			if os.IsNotExist(err) {
				return nil, &imageserver.ImageError{
					Message: "404",
				}
			}
			panic(err)
		}
		_, format, err := image.DecodeConfig(data)
		if err != nil {
			panic(err)
		}
		b, err := ioutil.ReadFile(filePath)
		if err != nil {
			panic(err)
		}

		im := &imageserver.Image{
			Format: format,
			Data:   b,
		}
		return im, nil
	}))
}

func newServerFile(srv imageserver.Server) imageserver.Server {
	cch := imageserver_cache_file.Cache{Path: cachedir}
	kg := imageserver_cache.NewParamsHashKeyGenerator(sha256.New)
	return &imageserver_cache.Server{
		Server:       srv,
		Cache:        &cch,
		KeyGenerator: kg,
	}
}

func newServerLimit(srv imageserver.Server) imageserver.Server {
	return imageserver.NewLimitServer(srv, runtime.GOMAXPROCS(0)*2)
}

func newServerCacheMemory(srv imageserver.Server) imageserver.Server {
	if len(cachedir) <= 0 {
		return srv
	}
	return &imageserver_cache.Server{
		Server:       srv,
		Cache:        imageserver_cache_memory.New(memCacheSize),
		KeyGenerator: imageserver_cache.NewParamsHashKeyGenerator(sha256.New),
	}
}

// ImageAPI 图片URL
// @Summary 图片URL
// @Description 图片URL
// @tags API1 文件（需要认证）
// @Accept  json
// @Produce json
// @Security ApiKeyAuth
// @Param id query string false "id, default 0, 数据集的ID"
// @Success 200 {string} json "{"ping": "pong",	"status": 200}"
// @Failure 401 {string} json "{"data": "cookie token is empty", "status": 错误码}"
// @Router /api1/imgs [get]
func ImageAPI() http.Handler {
	var _handler http.Handler = &imageserver_http.Handler{
		Parser: imageserver_http.ListParser([]imageserver_http.Parser{
			&imageserver_http.SourcePathParser{},
			&imageserver_http_crop.Parser{},
			&imageserver_http_gift.RotateParser{},
			&imageserver_http_gift.ResizeParser{},
			&imageserver_http_image.FormatParser{},
			&imageserver_http_image.QualityParser{},
			&imageserver_http_gamma.CorrectionParser{},
		}),
		Server:   newServer(),
		ETagFunc: imageserver_http.NewParamsHashETagFunc(sha256.New),
	}
	_handler = &imageserver_http.ExpiresHandler{
		Handler: _handler,
		Expires: 7 * 24 * time.Hour,
	}
	_handler = &imageserver_http.CacheControlPublicHandler{
		Handler: _handler,
	}

	return _handler
}
