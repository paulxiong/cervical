package logutils

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
	//Trace 调试
	Trace *log.Logger
	//Info 调试
	Info *log.Logger
	//Warning 警告
	Warning *log.Logger
	//Error 错误
	Error *log.Logger
)

func init() {
	traceWriter := io.Writer(os.Stdout)
	infoWriter := io.Writer(os.Stdout)
	warningWriter := io.Writer(os.Stdout)
	errorWriter := io.Writer(os.Stdout)

	if configs.Log.LogOut != "enable" {
		traceWriter = ioutil.Discard
		infoWriter = ioutil.Discard
		warningWriter = ioutil.Discard
		errorWriter = ioutil.Discard

		gin.SetMode(gin.ReleaseMode)
		gin.DefaultWriter = ioutil.Discard
	} else {
		if configs.Log.LogLevel == "Info" {
			traceWriter = ioutil.Discard
		} else if configs.Log.LogLevel == "Warning" {
			traceWriter = ioutil.Discard
			infoWriter = ioutil.Discard
		} else if configs.Log.LogLevel == "error_writer" {
			traceWriter = ioutil.Discard
			infoWriter = ioutil.Discard
			warningWriter = ioutil.Discard
		}

		if configs.Log.LogGin == "enable" {
			gin.SetMode(gin.DebugMode)
			gin.DisableConsoleColor()
			gin.DefaultWriter = os.Stdout
		} else {
			gin.SetMode(gin.ReleaseMode)
			gin.DefaultWriter = ioutil.Discard
		}
	}

	Trace = log.New(traceWriter, "TRACE:   ", log.Ltime|log.Lshortfile)
	Info = log.New(infoWriter, "INFO:    ", log.Ltime|log.Lshortfile)
	Warning = log.New(warningWriter, "WARNING: ", log.Ltime|log.Lshortfile)
	Error = log.New(errorWriter, "ERROR:   ", log.Ltime|log.Lshortfile)
}
