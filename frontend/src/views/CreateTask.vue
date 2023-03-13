<template>
  <div class="container">
    <h1 align="center">Create Your Image Task</h1>
    <div class="row">
      <div class="col-md-4">
        <form @submit.prevent="onSubmit">
          <br>
          <div class="form-group">
                <label for="location">Task Name</label>
                <input type="text" v-model="taskForm.title" class="form-control" id="title" placeholder="" required>
          </div>
          <br>
          <div class="form-group">
            <label for="about_me">Discription</label>
            <textarea v-model="taskForm.discription" class="form-control" id="discription" rows="5" placeholder="" required></textarea>
          </div>
          <br>
          <!-- <form name="imgForm" id="imgForm" enctype="multipart/form-data" action="图片上传接口" method='post'>
            <input class="input-loc-img"  name="imgLocal" id="imgLocal" type='file' accept="image/*" @change="selectImg" />
          </form>  -->
          <div class="upload">           
           <input type="file" id="file" multiple @change="upload">
         </div>
         <div v-show="taskForm.ImgError">{{ taskForm.ImgError }}</div>
          <br>
          <div style="text-align:center">
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>
          <!-- <el-upload
        class="avatar-uploader"
        action="/peng/addFile"
        :on-success="handleAvatarFileSuccess"
        :on-error="handleAvatarFileError"
        :before-upload="beforeAvatarFileUpload"
        limit="1">
        <el-button size="small" type="primary">点击上传</el-button>
        </el-upload> -->
        </form>
      </div>
      <div class="col-md-8">
          <h3 style="text-align:center">Only Image Files Allowed!</h3>
          <ul class="view">
            <!-- <li>
                <img src="../assets/logo.png">
                <div class="delect" title="删不了我" @click="noDelect">×</div>
            </li> -->
            <li v-for="(item,index) in list" :key="index" >
                <img :src="item">
                <div class="delect" @click="delect(index)">×</div>
            </li>     
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import store from '../store/index.js'
export default {
  name: 'CreateTask',  //this is the name of the component
  data () {
    return {
      sharedState: store.state,
      taskForm: {
        title: '',
        discription: '',
        submitted: false,  // 是否点击了 submit 按钮
        ImgError: null
      },
      list:[],
      file:[]
    }
  },
  methods: {
    onSubmit () {
      this.taskForm.submitted = true  // 先更新状态
      if (!this.list) {
        this.taskForm.ImgError = 'Please add at least one image.'
        return false
        // alert('Task name required.')
      } else {
        this.taskForm.ImgError = null
      }
      
      const user_id = this.sharedState.user_id
      const path = `/newtask/${user_id}`
      const payload = {
        title: this.taskForm.title,
        discription: this.taskForm.discription,
        file: this.list,
      }
      this.$axios.post(path, payload)
        .then(() => {
          // handle success
          this.$toasted.success('Successed create your task.')
          this.$router.push({
            name: 'Profile',
            params: { id: user_id }
          })
        })
        .catch((error) => {
          // handle error
          alert('请上传至少一张图片')
          console.log(error.response.data)
        })
    },
    delect(index){
        console.log(index);
        this.list.splice(index,1);                    
    },
    // 这是默认图片的方法，弹出默认图片无法删除
    noDelect(){
        alert('默认图片无法删除。')
    },
    upload(e){
        //e.target指向事件执行时鼠标所点击区域的那个元素，那么为input的标签，
        // 可以输出 e.target.files 看看，这个files对象保存着选中的所有的图片的信息。
        console.log(e.target.files)
        //------------------------------------------------------     
        // 既然如此，循环这个files对象，用for of 循环，     
        for(let item of e.target.files){
            //正则表达式，判断每个元素的type属性是否为图片形式
            if (!/image\/\w+/.test(item.type)){
                // 提示只能是图片，return
                alert("只能选择图片");
                return;
            }
            // 保存下当前 this ，就是vue实例
            var _this = this;
            //  创建一个FileReader()对象，它里面有个readAsDataURL方法
            let reader = new FileReader();
            // readAsDataURL方法可以将上传的图片格式转为base64,然后在存入到图片路径, 
            //这样就可以上传电脑任意位置的图片                            
            reader.readAsDataURL(item);
            //文件读取成功完成时触发
            reader.addEventListener('load',function(){
                //reader.result返回文件的内容。
                //只有在读取操作完成后，此属性才有效，返回的数据的格式取决于是使用哪种读取方法来执行读取操作的。
                //给数组添加这个文件也就是图片的内容
                _this.list.push(this.result)
            })
            // let reader2 = new FileReader();
            // reader2.readAsBinaryString(item); 
            // reader2.onload = function() { 
            //     _this.file.push(this.result)
            // }; 
        }
    },
    created (){
        console.log("created")
  },
    // handleAvatarFileError: function () {
    //     alert("文件上传走丢了。。");
    // },
    // handleAvatarFileSuccess: function () {
    //     this.$message.success("上传文件成功！");
    // },
    // beforeAvatarFileUpload: function (file) {
    //     //限制的上限为10M
    //     const isLt10M = file.size / 1024 / 1024 < 10;
    //     if (!isLt10M) {
    //     this.$message.error('上传文件大小不能超过 10MB!');
    //     }
    //     return isLt10M;
    // }
  },
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