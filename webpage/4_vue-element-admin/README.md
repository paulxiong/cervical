## 序
项目基于vue-element-admin，实现全组件化、模块化，对所有公用的JS方法/插件进行封装并模块化，组件部分采用全局引用+就近依赖原则，页面相关性强的组件放在局部components，公用组件则放在全局components，代码分层清晰，每个目录/功能块实现高内聚、解耦合，静态资源分类存储，为样式避免重复代码应用了全局样式，并做了主题配色，方便后期更换。前后端数据部分做浏览器缓存，在vuex基础上加入动态绑定，保证页面中的重要数据展示有兜底数据，提升用户使用体验，路由上采用哈希路由（ps:可替换history路由），配置了全局权限配置文件permission.js，可根据后端分配的用户权限配置相应的路由/功能模块。

## 项目入手
```bash
$ npm install
$ npm run dev
```

## 打包部署
```bash
$ npm install
$ npm run build:prod #正式包
$ npm run build:alpha #测试包
```

## 集成单元测试
```bash
$ npm run test
```

## git管理
- 提交
```bash
$ git pull
$ git status
$ git add 文件目录/文件名
$ git commit -m '本次修改说明'
$ git push
```

- 撤销
```bash
$ git reset --hard
```

- 回退
```bash
$ git log
$ git reset 版本
```

## 补充
项目中还有一些多余的文件/目录，可根据实际业务需求进行修改/删除，对于未用到的全局组件可酌情处理。保证代码规范，维护好每一次git提交。