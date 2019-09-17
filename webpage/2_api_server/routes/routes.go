package routes

import (
	"net/http"
	"time"

	ctr "github.com/paulxiong/cervical/webpage/2_api_server/controllers"

	"github.com/gin-contrib/cors"
	"github.com/gin-contrib/gzip"
	"github.com/gin-gonic/gin"

	ginSwagger "github.com/swaggo/gin-swagger"
	"github.com/swaggo/gin-swagger/swaggerFiles"
)

// Router 注册路由
func Router() *gin.Engine {
	r := gin.New()
	r.Use(gin.Logger())
	r.Use(gin.Recovery())
	r.Use(gzip.Gzip(gzip.DefaultCompression))

	r.StaticFile("/favicon.png", "./web/dist/favicon.ico")
	r.StaticFile("/", "./web/dist/")
	r.StaticFS("/static", http.Dir("./web/dist/static"))
	r.NoRoute(func(c *gin.Context) { c.JSON(404, gin.H{"text": "Not Found."}) })

	corsObject := cors.New(cors.Config{
		AllowAllOrigins: true,
		AllowMethods:    []string{"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"},
		AllowHeaders:    []string{"Accept", "Authorization", "Content-Type", "X-CSRF-Token", "X-Requested-With", "testHeader"},
		MaxAge:          12 * time.Hour,
	})
	r.Use(corsObject)

	r.GET("/swagger/*any", ginSwagger.DisablingWrapHandler(swaggerFiles.Handler, "RELEASE"))

	/* 用户相关的API */
	user := r.Group("/user")
	user.POST("/register", ctr.RegisterUser)
	user.POST("/login", ctr.LoginUser)
	user.Use(ctr.CheckAuth)
	{
		user.GET("/info", ctr.GetUser)
		user.GET("/logout", ctr.LogoutUser)
	}

	api1 := r.Group("/api1")
	api1.GET("/ping", ctr.Pong) //不需要登录就能ping的API

	api1.Use(ctr.CheckAuth)
	{
		api1.GET("/refresh_token", ctr.AuthMiddleware.RefreshHandler) // Refresh time can be longer than token timeout
		api1.GET("/authping", ctr.AuthPong)
		//用户
		api1.GET("/userinfo", ctr.GetUser)
		// 数据
		api1.GET("/dtinfo", ctr.AllInfo)
		api1.GET("/batchinfo", ctr.GetBatchInfo)
		api1.GET("/medicalidinfo", ctr.GetMedicalIDInfo)
		api1.GET("/categoryinfo", ctr.GetCategoryInfo)
		api1.POST("/imglistsofwanted", ctr.GetImgListOfWanted)
		api1.GET("/imglistsonebyone", ctr.GetImgListOneByOne)
		api1.GET("/getLabelbyimageid", ctr.GetLabelByImageID)
		api1.POST("/createdataset", ctr.CreateDataset)
		api1.POST("/getimgnptypebymids", ctr.GetImagesNPTypeByMedicalID)
		api1.GET("/listdatasets", ctr.ListDatasets)
		// 任务
		api1.POST("/job", ctr.GetOneJob)
		api1.POST("/jobresult", ctr.SetJobResult)
		api1.GET("/jobresult", ctr.GetJobResult)
		api1.GET("/jobpercent", ctr.GetJobPercent)
		api1.GET("/joblog", ctr.GetJobLog)
		// 模型
		api1.GET("/jobmodel", ctr.GetModelInfo)
		api1.POST("/savemodel", ctr.SaveModelInfo)
	}
	return r
}
