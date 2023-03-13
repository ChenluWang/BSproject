<template>
  <div class="container">
    <h1 align="center">Task-{{task.id}}</h1>
    <h2 class="h5 g-font-weight-300 g-mb-10">
        <i class="icon-badge g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i> Creator : <router-link v-bind:to="{name: 'Profile', params: { id: task.creator_id }}"><span>{{ task.creator_id }}</span></router-link>
    </h2> 
    <h2 class="h5 g-font-weight-300 g-mb-10">
        <i class="icon-badge g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i> Created Since : {{ $moment(task.create_time).format('LLL') }}
    </h2> 
    <h2 class="h5 g-font-weight-300 g-mb-10">
        <i class="icon-badge g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i> Title: {{task.title}}
    </h2>
    <h2 class="h5 g-font-weight-300 g-mb-10">
        <i class="icon-badge g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i> Discription: {{task.discription}}
    </h2>
    <div class="row">
          <ul class="view">
            <li v-for="(item,index) in task.Img" :key="index" >
                <img :src="item">
                <div class="delect" @click="delect(index)">×</div>
            </li>     
          </ul>
          <router-link v-bind:to="{ name: 'Home' }" class="btn btn-block u-btn-outline-primary g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-user-follow g-pos-rel g-top-1 g-mr-5"></i> Back to Home
          </router-link>
      </div>
    </div>
</template>

<script>
import store from '../store/index.js'
export default {
  name: 'ShowTask',  //this is the name of the component
  data () {
    return {
      sharedState: store.state,
      task: {
        id:'',  
        creator_id:'',
        title: '',
        discription: '',
        create_time:'',
        finish_time:'',
        IsFinished:'',
        Img:''
      },
    }
  },
  methods: {
    getTask(id) {
      const path = `/gettask/${id}`
      this.$axios.get(path)
        .then((response) => {
          this.task = response.data
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });
    },
  },
  created(){
    const task_id = this.$route.params.id
    this.getTask(task_id)
  },
  // 当 id 变化后重新加载数据
  beforeRouteUpdate (to, from, next) {
    this.getTask(to.params.id)
    next()
  }
}
</script>

<style>
    .view{
           display: flex;
           justify-content: space-around;
           flex-wrap: wrap;
           align-items: space-around;
        }
    .view > li{
            width: 200px;
            height: 120px;
            background-color: rgba(54, 194, 35,0.1);
            list-style: none;
            margin: 20px;
            position: relative;
        }
        .view > li > img{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
     .delect{
            position: absolute;
            right: 0;
            top: 0;
             width: 20px;
             height: 20px;
             text-align: center;
             line-height: 20px;
             font-size: 15px;
             background-color: rgba(255, 255, 255,0.5);
             user-select: none;
             cursor: pointer;
             opacity: 0;
        }
    .delect:hover{
            background-color: rgba(31, 31, 31, 0.5);
             color: white;
        }
        .view>li:hover .delect{
            opacity: 1;
        }
</style>