package function

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
	logger "github.com/paulxiong/cervical/webpage/2_api_server/log"
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

// ImageServerSettings 图片服务器的配置
type ImageServerSettings struct {
	MaxWidth     int           `json:"maxWidth"     example:"1024"`          // 图片缩放的最大宽度
	MaxHeight    int           `json:"maxHeight"    example:"768"`           // 图片缩放的最大高度
	ImgDir       string        `json:"imgDir"       example:"uoload"`        // 存放图片的目录
	Cachedir     string        `json:"cachedir"     example:"cache"`         // 图片文件的缓存目录
	MemCacheSize int64         `json:"memCacheSize" example:"134217728"`     // 内存缓存的大小
	HTTPExpires  time.Duration `json:"httpExpires"  example:"3600000000000"` // It only sets the header if the status code is StatusOK/204 or StatusNotModified/304.
}

func newServer(imgdir string, cachedir string, memCacheSize int64, maxWidth int, maxHeight int) imageserver.Server {
	srv := getImgServer(imgdir)
	srv = newServerImage(srv, maxWidth, maxHeight)
	srv = newServerFile(srv, cachedir)
	srv = newServerLimit(srv)
	srv = newServerCacheMemory(srv, cachedir, memCacheSize)
	return srv
}

func newServerImage(srv imageserver.Server, maxWidth int, maxHeight int) imageserver.Server {
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
func getImgServer(imgdir string) imageserver.Server {
	return imageserver.Server(imageserver.ServerFunc(func(params imageserver.Params) (*imageserver.Image, error) {
		source, err := params.GetString("source")
		if err != nil {
			return nil, err
		}
		filePath := filepath.Join(imgdir, source)
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

func newServerFile(srv imageserver.Server, cachedir string) imageserver.Server {
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

func newServerCacheMemory(srv imageserver.Server, cachedir string, memCacheSize int64) imageserver.Server {
	if len(cachedir) <= 0 {
		return srv
	}
	return &imageserver_cache.Server{
		Server:       srv,
		Cache:        imageserver_cache_memory.New(memCacheSize),
		KeyGenerator: imageserver_cache.NewParamsHashKeyGenerator(sha256.New),
	}
}

// ImageServer 返回图片服务器的http.Handler
func ImageServer(cfg *ImageServerSettings) http.Handler {
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
		ErrorFunc: func(err error, req *http.Request) {
			logger.Info.Println(err)
		},
		Server:   newServer(cfg.ImgDir, cfg.Cachedir, cfg.MemCacheSize, cfg.MaxWidth, cfg.MaxHeight),
		ETagFunc: imageserver_http.NewParamsHashETagFunc(sha256.New),
	}
	_handler = &imageserver_http.ExpiresHandler{
		Handler: _handler,
		Expires: cfg.HTTPExpires,
	}
	_handler = &imageserver_http.CacheControlPublicHandler{
		Handler: _handler,
	}
	return _handler
}
