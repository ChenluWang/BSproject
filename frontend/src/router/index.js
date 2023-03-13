// export default router

import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/views/Login'
import Register from '@/views/Register'
import Profile from '@/views/Profile'
import EditProfile from '@/views/EditProfile'
import Marker from '@/views/Marker'
import BaseNavBar from '@/components/BaseNavBar'
import Home from '@/views/Home'
import ShowTask from '@/views/ShowTask'
import ShowMarker from '@/views/ShowMarker'
import CreateVedioTask from '@/views/CreateVedioTask'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/test',
      name: 'Test',
      component: BaseNavBar,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/user/:id',
      name: 'Profile',
      component: Profile,
      meta: {
        requiresAuth: true
      }
    },
    {
      // 用户修改自己的个人信息
      path: '/edit-profile',
      name: 'EditProfile',
      component: EditProfile,
      meta: {
        requiresAuth: true
      }
    },
    // {
    //   path: '/createtask',
    //   name: 'CreateTask',
    //   component: CreateTask,
    //   meta: {
    //     requiresAuth: true
    //   }
    // },
    {
      path: '/createvediotask',
      name: 'CreateVedioTask',
      component: CreateVedioTask,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/marker/:id',
      name: 'Marker',
      component: Marker
    },
    {
      path: '/showmarker/:id',
      name: 'ShowMarker',
      component: ShowMarker
    },
    {
      path: '/showtask/:id',
      name: 'ShowTask',
      component: ShowTask
    },
  ]
})

router.beforeEach((to, from, next) => {
  const token = window.localStorage.getItem('madblog-token')
  if (to.matched.some(record => record.meta.requiresAuth) && (!token || token === null)) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else if (token && to.name == 'Login') {
    // 用户已登录，但又去访问登录页面时不让他过去
    next({
      path: from.fullPath
    })
  } else if (to.matched.length === 0) {  // 要前往的路由不存在时
    console.log('here')
    console.log(to.matched)
    Vue.toasted.error('404: NOT FOUND', { icon: 'fingerprint' })
    if (from.name) {
      next({
        name: from.name
      })
    } else {
      next({
        path: '/'
      })
    }
  } else {
    next()
  }
})

export default router