import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/* Router Modules */

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    noCache: true                if set true, the page will no be cached(default is false)
    affix: true                  if set true, the tag will affix in the tags-view
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path*',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/auth-redirect',
    component: () => import('@/views/login/auth-redirect'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  },
  {
    path: '/test',
    component: () => import('@/views/testView/index'),
    hidden: true
  },
  {
    path: '/test2',
    component: () => import('@/views/testView/index2'),
    hidden: true
  },
  {
    path: '/doctorreport',
    component: () => import('@/views/review/components/doctorReportPage'),
    hidden: true
  },
  {
    path: '/report/details',
    component: () => import('@/views/workSpace/details2'),
    hidden: true
  },
  {
    path: '/label/page',
    component: () => import('@/views/label/labelpage'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/home',
    children: [
      {
        path: 'home',
        component: () => import('@/views/home/index'),
        name: 'route.homepage',
        meta: { title: 'route.homepage', icon: 'dashboard', affix: true, keepAlive: true }
      }
    ]
  },
  /*boostx: added step-by-step operation flow */
  {
    path: '/stepBystep',
    component: Layout,
    redirect: '/stepBystep/list',
    name: 'route.stepBystepOverview',
    meta: { title: 'route.stepBystepOverview', icon: 'component', keepAlive: true, roles: ['admin', 'editor'] },
    children: [
      {
        path: 'list',
        component: () => import('@/views/stepBystep/index'),
        name: 'route.stepBystepOverview',
        meta: { title: 'route.stepBystepOverview', icon: 'component', affix: true }
      },
      {
        path: 'details',
        component: () => import('@/views/stepBystep/details'),
        hidden: true,
        name: 'route.stepBystepDetails',
        meta: { title: 'route.stepBystepDetails', affix: true }
      }
    ]
  },

  {
    path: '/workSpace',
    component: Layout,
    redirect: '/workSpace/list',
    name: 'route.workSpace',
    meta: { title: 'route.workSpace', icon: 'component', keepAlive: true, roles: ['admin', 'editor'] },
    children: [
      {
        path: 'list',
        component: () => import('@/views/workSpace/index'),
        name: 'route.workSpaceOverview',
        meta: { title: 'route.workSpaceOverview', icon: 'component', affix: true }
      },
      {
        path: 'details',
        component: () => import('@/views/workSpace/details'),
        hidden: true,
        name: 'route.workSpaceDetails',
        meta: { title: 'route.workSpaceDetails', affix: true }
      }
    ]
  },
  {
    path: '/report',
    component: Layout,
    redirect: '/report/list',
    name: 'route.report',
    meta: { title: 'route.report', icon: 'nested', keepAlive: true, roles: ['admin', 'editor'] },
    children: [
      {
        path: 'list',
        component: () => import('@/views/report/report'),
        name: 'route.reportOverview',
        meta: { title: 'route.reportOverview', icon: 'documentation', affix: true }
      }
    ]
  },
  // {
  //   path: '/review',
  //   component: Layout,
  //   redirect: '/review/list',
  //   name: 'route.cell',
  //   meta: { title: 'route.cell', icon: 'nested', roles: ['admin', 'editor'] },
  //   children: [
  //     {
  //       path: 'list',
  //       component: () => import('@/views/review/index'),
  //       name: 'route.cellOverview',
  //       meta: { title: 'route.cellOverview', icon: 'cellspredict', affix: true, keepAlive: true }
  //     }
  //   ]
  // },
  {
    path: '/label',
    component: Layout,
    redirect: '/label',
    children: [
      {
        path: '/label',
        component: () => import('@/views/label/labelhome'),
        name: 'route.label',
        meta: { title: 'route.label', icon: 'edit', affix: true, roles: ['admin', 'editor'] }
      }
    ]
  }
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  {
    path: '/system',
    component: Layout,
    redirect: '/system',
    name: 'route.system',
    meta: { title: 'route.system', icon: 'table', keepAlive: true, roles: ['admin'] },
    children: [
      {
        path: 'imgserver',
        component: () => import('@/views/system/imgServer'),
        name: 'route.systemImg',
        meta: { title: 'route.systemImg', icon: 'photo', affix: true }
      },
      // {
      //   path: 'email',
      //   component: () => import('@/views/system/email'),
      //   name: 'route.systemMail',
      //   meta: { title: 'route.systemMail', icon: 'email', affix: true }
      // },
      {
        path: 'errLog',
        component: () => import('@/views/system/errLog'),
        name: 'route.systemErr',
        meta: { title: 'route.systemErr', icon: 'bug', affix: true }
      }
    ]
  },
  {
    path: '/authManage',
    component: Layout,
    redirect: '/authManage/userManage',
    name: 'route.permission',
    meta: { title: 'route.permission', icon: 'peoples', keepAlive: true, roles: ['admin'] },
    children: [
      {
        path: 'userManage',
        component: () => import('@/views/user/userMannage'),
        name: 'route.permissionUser',
        meta: { title: 'route.permissionUser', icon: 'peoples', affix: true }
      },
      {
        path: 'userLog',
        component: () => import('@/views/user/userLog'),
        name: 'route.permissionLog',
        meta: { title: 'route.permissionLog', icon: 'nested', affix: true }
      },
      {
        path: 'userInfo',
        component: () => import('@/views/user/userInfo'),
        name: 'route.permissionInfo',
        meta: { title: 'route.permissionInfo', icon: 'nested', affix: true },
        hidden: true
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
