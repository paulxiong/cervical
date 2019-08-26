package log_utils

import (
	configs "github.com/paulxiong/cervical/webpage/2_api_server/configs"

	"io"
	"io/ioutil"
	"log"
	"os"

	"github.com/gin-gonic/gin"
)

var errorfile string = "error.log"

var (
	Trace   *log.Logger
	Info    *log.Logger
	Warning *log.Logger
	Error   *log.Logger
)

func init() {
	trace_writer := io.Writer(os.Stdout)
	info_writer := io.Writer(os.Stdout)
	warning_writer := io.Writer(os.Stdout)
	error_writer := io.Writer(os.Stdout)

	if configs.Log.Log_out != "enable" {
		trace_writer = ioutil.Discard
		info_writer = ioutil.Discard
		warning_writer = ioutil.Discard
		error_writer = ioutil.Discard

		gin.SetMode(gin.ReleaseMode)
		gin.DefaultWriter = ioutil.Discard
	} else {
		if configs.Log.Log_level == "Info" {
			trace_writer = ioutil.Discard
		} else if configs.Log.Log_level == "Warning" {
			trace_writer = ioutil.Discard
			info_writer = ioutil.Discard
		} else if configs.Log.Log_level == "error_writer" {
			trace_writer = ioutil.Discard
			info_writer = ioutil.Discard
			warning_writer = ioutil.Discard
		}

		if configs.Log.Log_gin == "enable" {
			gin.SetMode(gin.DebugMode)
			gin.DisableConsoleColor()
			gin.DefaultWriter = os.Stdout
		} else {
			gin.SetMode(gin.ReleaseMode)
			gin.DefaultWriter = ioutil.Discard
		}
	}

	Trace = log.New(trace_writer, "TRACE:   ", log.Ltime|log.Lshortfile)
	Info = log.New(info_writer, "INFO:    ", log.Ltime|log.Lshortfile)
	Warning = log.New(warning_writer, "WARNING: ", log.Ltime|log.Lshortfile)
	Error = log.New(error_writer, "ERROR:   ", log.Ltime|log.Lshortfile)
}
