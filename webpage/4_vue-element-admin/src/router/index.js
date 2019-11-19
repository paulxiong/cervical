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
    path: '/',
    component: Layout,
    redirect: '/home',
    children: [
      {
        path: 'home',
        component: () => import('@/views/home/index'),
        name: '首页',
        meta: { title: '首页', icon: 'dashboard', affix: true }
      }
    ]
  },
  {
    path: '/workSpace',
    component: Layout,
    redirect: '/workSpace/list',
    name: '概览',
    meta: { title: '概览', icon: 'component' },
    children: [
      {
        path: 'list',
        component: () => import('@/views/workSpace/index'),
        name: '工作台',
        meta: { title: '工作台', icon: 'component', affix: true }
      },
      {
        path: 'details',
        component: () => import('@/views/workSpace/details'),
        hidden: true,
        name: '详情',
        meta: { title: '详情', affix: true }
      }
    ]
  },
  {
    path: '/report',
    component: Layout,
    redirect: '/report/list',
    name: '概览',
    meta: { title: '概览', icon: 'nested' },
    children: [
      {
        path: 'list',
        component: () => import('@/views/report/report'),
        name: '医疗报告',
        meta: { title: '医疗报告', icon: 'documentation', affix: true }
      },
      {
        path: 'details',
        component: () => import('@/views/workSpace/details'),
        hidden: true,
        name: '详情',
        meta: { title: '详情', affix: true }
      }
    ]
  },
  {
    path: '/label',
    component: Layout,
    redirect: '/label',
    children: [
      {
        path: '/label',
        component: () => import('@/views/label/index'),
        name: '标注',
        meta: { title: '标注', icon: 'edit', affix: true }
      }
    ]
  },
  {
    path: '/authManage',
    component: Layout,
    redirect: '/authManage/userManage',
    name: '权限管理',
    meta: {
      title: '权限管理',
      icon: 'peoples'
    },
    children: [
      {
        path: 'userManage',
        component: () => import('@/views/user/userMannage'),
        name: '用户管理',
        meta: { title: '用户管理', icon: 'peoples', affix: true }
      },
      {
        path: 'userLog',
        component: () => import('@/views/user/userLog'),
        name: '用户日志',
        meta: { title: '用户日志', icon: 'nested', affix: true }
      },
      {
        path: 'userInfo',
        component: () => import('@/views/user/userInfo'),
        name: '用户信息',
        meta: { title: '用户信息', icon: 'nested', affix: true }
      }
    ]
  },
  {
    path: '/system',
    component: Layout,
    redirect: '/system',
    name: '系统设置',
    meta: {
      title: '系统设置',
      icon: 'table'
    },
    children: [
      {
        path: 'email',
        component: () => import('@/views/system/email'),
        name: '邮件设置',
        meta: { title: '邮件设置', icon: 'email', affix: true }
      },
      {
        path: 'resourece',
        component: () => import('@/views/system/resource'),
        name: '资源管理',
        meta: { title: '资源管理', icon: 'tree-table', affix: true }
      },
      {
        path: 'errLog',
        component: () => import('@/views/system/errLog'),
        name: '错误日志',
        meta: { title: '错误日志', icon: 'bug', affix: true }
      }
    ]
  }
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
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
