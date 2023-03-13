<template>
  <div class="container">
      <el-form :model="formInline" style="text-align: right">
          <el-form-item  label="WELCOME TO LULU‘S WEBSITE">
            <el-radio-group v-model="formInline.radio" @change="handleChange" size="small">
              <el-radio-button label="全部"></el-radio-button>
              <el-radio-button label="未标注"></el-radio-button>
              <el-radio-button label="已标注"></el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>
    <div class="card border-0 g-mb-15">
      <!-- Panel Header -->
      <div class="card-header d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 g-mb-15">
        <h3 class="h6 mb-0">
          <i class="icon-bubbles g-pos-rel g-top-1 g-mr-5"></i> All Tasks <small v-if="posts">(共 {{ posts._meta.total_items }} 篇, {{ posts._meta.total_pages }} 页)</small>
        </h3>
        <div class="dropdown g-mb-10 g-mb-0--md">
          <span class="d-block g-color-primary--hover g-cursor-pointer g-mr-minus-5 g-pa-5" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <i class="icon-options-vertical g-pos-rel g-top-1"></i>
            </span>
          <div class="dropdown-menu dropdown-menu-right rounded-0 g-mt-10">
            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 5 }}" class="dropdown-item g-px-10">
              <i class="icon-layers g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 5 篇
            </router-link>
            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 10 }}" class="dropdown-item g-px-10">
              <i class="icon-wallet g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 10 篇
            </router-link>
            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 20 }}" class="dropdown-item g-px-10">
              <i class="icon-fire g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 20 篇
            </router-link>

            <div class="dropdown-divider"></div>

            <router-link v-bind:to="{ name: 'Home', query: { page: 1, per_page: 1 }}" class="dropdown-item g-px-10">
              <i class="icon-plus g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 1 篇
            </router-link>            
          </div>
        </div>
      </div>
      <!-- End Panel Header -->

      <!-- Panel Body -->
      <div v-if="posts" class="card-block g-pa-0" >
        <div v-for="(post, index) in posts.items" v-bind:key="index" class="media g-brd-around g-brd-gray-light-v4 g-pa-20 g-mb-20">
          <!-- <router-link v-bind:to="{ name: 'Profile', params: { id: post.creator_id }}" v-bind:title="post.creator_id || post.id">
            <img class="d-flex g-width-50 g-height-50 g-mt-3 g-mr-20" v-bind:src="post.creator_id._links.avatar" v-bind:alt="post.creator_id.name || post.creator_id.name">
          </router-link> -->
          
          <div class="media-body">
            <div class="d-sm-flex justify-content-sm-between align-items-sm-center g-mb-15 g-mb-10--sm">
              <h5 class="h4 g-font-weight-300 g-mr-10 g-mb-5 g-mb-0--sm">
                <router-link v-bind:to="{ name: 'ShowTask', params: { id: post.id }}" class="g-text-underline--none--hover">{{ post.title }}</router-link>
              </h5>
              <div class="text-nowrap g-font-size-12">
                <span>{{ $moment(post.create_time).fromNow() }}</span> / <router-link v-bind:to="{ name: 'Profile', params: { id: post.creator_id}}"><span v-if="post.creator_id">{{ post.creator_id }}</span><span v-else>{{ post.title }}</span></router-link>
              </div>
            </div>

            <div class="d-flex justify-content-start">
              <ul class="list-inline mb-0">
                <li class="list-inline-item g-mr-20">
                  <a class="g-color-gray-dark-v5 g-text-underline--none--hover">
                    {{ post.discription }}
                  </a>
                </li>
              </ul>

              <ul class="mb-0 ml-auto">
                <li v-if="post.creator_id == sharedState.user_id" class="list-inline-item g-mr-5">
                  <router-link v-if="post.IsFinished" v-bind:to="{ name: 'ShowMarker', params: { id: post.id }}" class="btn btn-xs u-btn-outline-purple g-mr-5">我发布的任务(已完成)</router-link>
                  <router-link v-else v-bind:to="{ name: 'ShowTask', params: { id: post.id }}" class="btn btn-xs u-btn-outline-red">我发布的任务(待领取)</router-link>
                </li>
                <li v-else class="list-inline-item g-mr-5">
                  <div v-if="post.IsFinished">
                    <button class="btn btn-xs u-btn-outline-purple g-mr-5" data-toggle="modal" data-target="#updatePostModal">任务已完成</button>
                    <router-link v-bind:to="{ name: 'ShowMarker', params: { id: post.id }}" class="btn btn-xs u-btn-outline-primary g-mr-5">查看任务</router-link>
                  </div>
                  <div v-else>
                    <router-link  v-bind:to="{ name: 'Marker', params: { id: post.id }}" class="btn btn-xs u-btn-outline-primary g-mr-5">领取任务</router-link>
                    <router-link v-bind:to="{ name: 'ShowTask', params: { id: post.id }}" class="btn btn-xs u-btn-outline-primary g-mr-5">查看任务</router-link>
                  </div>
                </li>
                <!-- <li v-if="post.creator_id == sharedState.user_id" class="list-inline-item g-mr-5">
                  <button v-on:click="onEditPost(post)" class="btn btn-xs u-btn-outline-purple" data-toggle="modal" data-target="#updatePostModal">编辑</button>
                </li>
                <li v-if="post.creator_id == sharedState.user_id" class="list-inline-item">
                  <button v-on:click="onDeletePost(post)" class="btn btn-xs u-btn-outline-red">删除</button>
                </li> -->
              </ul>
            </div>
          </div>
        </div>
      </div>
      <!-- End Panel Body -->
    </div>

    <!-- Pagination #04 -->
    <nav v-if="posts" aria-label="Page Navigation" class="g-mb-50" style="text-align:center">
      <ul class="list-inline">
        <li class="list-inline-item">
          <router-link v-bind:to="{ name: 'Home', query: { page: posts._meta.page - 1, per_page: posts._meta.per_page }}" v-bind:class="{'u-pagination-v1__item--disabled': posts._meta.page == 1}" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-21" aria-label="Previous">
            <span aria-hidden="true">
              <i class="fa fa-angle-left"></i>
            </span>
            <span class="sr-only">Previous</span>
          </router-link>
        </li>
        <span v-if="page != 'NaN'">
        <li  v-for="(page, index) in iter_pages" v-bind:key="index" class="list-inline-item g-hidden-sm-down">
          <router-link v-bind:to="{ name: 'Home', query: { page: page, per_page: posts._meta.per_page }}" v-bind:class="{'u-pagination-v1-1--active': $route.query.page == page || (!$route.query.page && page == 1)}" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-19">{{ page }}</router-link>
        </li>
        </span>
        <span v-else>
          <li class="list-inline-item g-hidden-sm-down">
            <span class="g-pa-12-19">...</span>
          </li>
        </span>
        <li class="list-inline-item">
          <router-link v-bind:to="{ name: 'Home', query: { page: posts._meta.page + 1, per_page: posts._meta.per_page }}" v-bind:class="{'u-pagination-v1__item--disabled': posts._meta.page == posts._meta.total_pages }" class="u-pagination-v1__item u-pagination-v1-1 g-rounded-50 g-pa-12-21" aria-label="Next">
            <span aria-hidden="true">
              <i class="fa fa-angle-right"></i>
            </span>
            <span class="sr-only">Next</span>
          </router-link>
        </li>
        <li class="list-inline-item float-right">
          <span class="u-pagination-v1__item-info g-pa-12-19">Page {{ posts._meta.page }} of {{ posts._meta.total_pages }}</span>
        </li>
      </ul>
    </nav>
    <!-- End Pagination #04 -->
  </div>
</template>

<script>
import store from '../store/index.js'
import Alert from '../components/Alert'
export default {
  name: 'Home',  //this is the name of the component
  alert: Alert,
  data () {
    return {
      formInline: {
        region: '',
        radio: '全部'
      },
      sharedState: store.state,
      posts: '',
      iter_pages: [],  // 分页导航栏
    }
  },
  methods: {
    handleChange(label){
      if(label == '全部'){
        this.getPosts ()
      }
      else if(label == '未标注'){
        this.getUnfinishedPosts()
      }
      else{
        this.getFinishedPosts()
      }
    },
    getUnfinishedPosts(){
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }
      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }
      const path = `/unfinishedtasks?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.posts = response.data
          console.log(this.posts)
          // 构建分页导航，当前页左、右两边各显示2页，比如  1, 2, ... 7, 8, 9, 10, 11 ... 30, 31
          let arr = [1, 2, this.posts._meta.page-2, this.posts._meta.page-1, this.posts._meta.page, this.posts._meta.page+1, this.posts._meta.page+2, this.posts._meta.total_pages-1, this.posts._meta.total_pages]
          // 小于1，或大于最大页数的都是非法的，要去除
          arr = arr.filter(item => item > 0 && item <= this.posts._meta.total_pages)
          // 去除重复项
          this.iter_pages = [...new Set(arr)]
          // 假设当前页为1，总页数为6或6以上时，在倒数第2个位置插入特殊标记  1, 2, 3 ... 5, 6
          if (this.posts._meta.page + 2 < this.posts._meta.total_pages - 2) {
            this.iter_pages.splice(-2, 0, 'NaN')
          }
          // 当前页为6或6以上时，在第3个位置插入特殊标记  1, 2 ... 4, 5, 6
          if (this.posts._meta.page - 3 > 2) {
            this.iter_pages.splice(2, 0, 'NaN')
          }
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
        })
    },
    getFinishedPosts(){
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }
      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }
      const path = `/finishedtasks?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.posts = response.data
          console.log(this.posts)
          // 构建分页导航，当前页左、右两边各显示2页，比如  1, 2, ... 7, 8, 9, 10, 11 ... 30, 31
          let arr = [1, 2, this.posts._meta.page-2, this.posts._meta.page-1, this.posts._meta.page, this.posts._meta.page+1, this.posts._meta.page+2, this.posts._meta.total_pages-1, this.posts._meta.total_pages]
          // 小于1，或大于最大页数的都是非法的，要去除
          arr = arr.filter(item => item > 0 && item <= this.posts._meta.total_pages)
          // 去除重复项
          this.iter_pages = [...new Set(arr)]
          // 假设当前页为1，总页数为6或6以上时，在倒数第2个位置插入特殊标记  1, 2, 3 ... 5, 6
          if (this.posts._meta.page + 2 < this.posts._meta.total_pages - 2) {
            this.iter_pages.splice(-2, 0, 'NaN')
          }
          // 当前页为6或6以上时，在第3个位置插入特殊标记  1, 2 ... 4, 5, 6
          if (this.posts._meta.page - 3 > 2) {
            this.iter_pages.splice(2, 0, 'NaN')
          }
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
        })
    },
    getPosts () {
      let page = 1
      let per_page = 5
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }
      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }
      
      const path = `/tasks?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.posts = response.data
          console.log(this.posts)
          // 构建分页导航，当前页左、右两边各显示2页，比如  1, 2, ... 7, 8, 9, 10, 11 ... 30, 31
          let arr = [1, 2, this.posts._meta.page-2, this.posts._meta.page-1, this.posts._meta.page, this.posts._meta.page+1, this.posts._meta.page+2, this.posts._meta.total_pages-1, this.posts._meta.total_pages]
          // 小于1，或大于最大页数的都是非法的，要去除
          arr = arr.filter(item => item > 0 && item <= this.posts._meta.total_pages)
          // 去除重复项
          this.iter_pages = [...new Set(arr)]
          // 假设当前页为1，总页数为6或6以上时，在倒数第2个位置插入特殊标记  1, 2, 3 ... 5, 6
          if (this.posts._meta.page + 2 < this.posts._meta.total_pages - 2) {
            this.iter_pages.splice(-2, 0, 'NaN')
          }
          // 当前页为6或6以上时，在第3个位置插入特殊标记  1, 2 ... 4, 5, 6
          if (this.posts._meta.page - 3 > 2) {
            this.iter_pages.splice(2, 0, 'NaN')
          }
        })
        .catch((error) => {
          // handle error
          console.log(error.response.data)
        })
    },
},
  created (){
        console.log("created")
        this.getPosts()
  },
  // 当查询参数 page 或 per_page 变化后重新加载数据
  beforeRouteUpdate (to, from, next) {
    // 注意：要先执行 next() 不然 this.$route.query 还是之前的
    next()
    this.getPosts()
  }
}
</script>