import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)
/* Layout */
import Layout from '@/layout'

export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '图标数据分析', icon: 'dashboard' }
    }]
  },
  {
    path:'/settings',
    component:Layout,
    redirect:"/settings",
    meta:{title:"项目管理",icon:"el-icon-cpu"},
    children:[{
      path:'product',
      name:'Product',
      component:()=>import('@/views/product/product'),
      meta:{title:"项目管理",icon:'el-icon-menu'}
    },
    {
      path:'apps',
      name:'apps',
      component:()=>import('@/views/product/apps'),
      meta:{title:"配置项/系统测试",icon:'el-icon-s-unfold'}
    }]
  },
  {
    path: '/tmp',
    component: Layout,
    redirect: '/tmp',
    meta: { title: '测试项和用例', icon: 'el-icon-files' },
    children: [
      {
        path: 'testitem',
        name: 'testitem',
        component: () => import('@/views/testitem/index'),
        meta: { title: '测试项管理', icon: 'el-icon-bank-card' }
      },
    ]
  },
  {
    path: 'commit',
    name:'commit',
    hidden: true,
    component:()=>import('@/views/testitem/commit'),
    meta: { title: '测试项新增修改', icon: 'el-icon-postcard' },
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  mode: 'history', // require service support
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
