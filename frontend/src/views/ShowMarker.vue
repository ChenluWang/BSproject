<template>
  <div>
    <!-- 图片导航 -->
    <div class="pics">
      <div class="arrow arrow-left" @click="showMore('down')"></div>
      <div class="pic-container">
        <div class="pic-box" ref="picContainer">
          <div class="pic" v-for="(v, i) in pics" :key="i">
            <div
              class="info"
              :style="{ 'background-image': 'url(' + v.cropImage + ')' }"
              @click="activePic(v.cropImage)"
            ></div>
          </div>
        </div>
      </div>
      <div class="arrow arrow-right" @click="showMore('up')"></div>
    </div>

    <el-row :gutter="10" class="tagList">
      <el-col :span="18">
        <ui-marker
          ref="aiPanel-editor"
          class="ai-observer"
          :uniqueKey="uuid"
          :ratio="16 / 9"
          :imgUrl="currentInfo.currentBaseImage"
          :readOnly="true"
          @vmarker:onImageLoad="onImageLoad"
        ></ui-marker>
      </el-col>
      <el-col :span="6">
        <div class="title">标签</div>
        <div class="tags" v-for="(v, i) in tags" :key="i">
          <el-tag size="small" @click="setTag(v)">
            {{ v.tagName }}
          </el-tag>
          <i class="el-icon-delete" @click="delTag(i)"></i>
        </div>
        <el-row>
          <el-button type="success" class="handleButton" @click="getResult">
            导出 Pascal VOC 格式的结果
          </el-button>
          </el-row>
          <el-button type="success" class="handleButton" @click="getResultofCOCO">
            导出 COCO 格式的结果
          </el-button>
      </el-col>
    </el-row>
  </div>
</template>
<script>
// import { AIMarker } from 'Vue-Picture-BD-Marker'
import { AIMarker } from 'vue-picture-bd-marker'
export default {
  name: 'ShowMarker',
  components: { 'ui-marker': AIMarker },
  data() {
    return {
      formInline: {
        region: '',
        radio: '全部'
      },
      uuid: '0da9130',
      // 当前图片的信息，包含图片原本的高矮胖瘦尺寸
      currentInfo: {
        currentBaseImage: 'http://m.imeitou.com/uploads/allimg/2019072516/3sw3nynp25y.jpg',
        rawW: 0,
        rawH: 0,
        currentW: 0,
        currentH: 0,
        checked: false, // false表示当前图片还没有标记过
        data: [] // 表示图片矩形标记信息
      },

      // *****************************
      pics: [],
      active: 0, // 当前图片序号
      picTotal: 10, // 照片总数
      active_id: 1, // 记录当前选中图片id
      // *********************************************
      tags: [
        {
          tagName: '小蜜蜂',
          tag: '0x0001'
        },
        {
          tagName: '汽车',
          tag: '0x0002'
        }
      ],
      allInfo: [], // 图片的矩形标记信息集合
      imageInfo: [], // 存储图片原始信息

      innerVisible: false,
      innerForm: {
        tagName: '',
        tag: ''
      },

      tep_rules: {
        tagName: [{ required: true, message: '请输入', trigger: 'blur' }],
        tag: [{ required: true, message: '请输入', trigger: 'blur' }]
      }
    }
  },
  mounted() {
    // this.onImageLoad()
  },
  methods: {
    /**记录图片当前的大小和原始大小 data={rawW,rawH,currentW,currentH} */
    onImageLoad(data) {
      console.log(data)
      this.imageInfo = data
    },

    setTag(v) {
      this.$refs['aiPanel-editor'].getMarker().setTag(v)
    },
    close() {
      this.innerVisible = false
      this.$refs['innerForm'].resetFields()
    },
    beforeClose(done) {
      this.$refs['innerForm'].resetFields()
      done()
    },
    // 点击左右按钮显示更多
    showMore(v) {
      let el = this.$refs.picContainer
      // let percent = (this.active / this.pics.length) * 100
      if (v == 'up') {
        this.active++
        if (this.active >= this.picTotal - 3) {
          // 最后4张图
          this.active = this.pics.length - 3
          return
        }
        if (
          this.pics.length - 3 == this.active &&
          this.pics.length < this.picTotal
        ) {
          this.photoPageIndex++
          this.getPhotos()
          return
        }
      } else {
        this.active--
        if (this.active < 0) this.active = 0
      }
      el.style.transform =
        'translateX(-' + (this.active / this.pics.length) * 100 + '%)'
    },

    getPhotos() {
      return this.$nextTick(() => {
        let el = this.$refs.picContainer
        if (el) {
          el.style.width = el.scrollWidth + 'px'

          el.style.transform =
            'translateX(-' + (this.active / this.pics.length) * 100 + '%)'
        }
      })
    },
    /**得到当前点击图片*/
    activePic(v) {
      this.currentInfo.currentBaseImage = v
      this.active_id = v.substring(v.lastIndexOf('/')+1,v.indexOf('.'))
      console.log(this.active_id)
      console.log(v)
      this.$refs['aiPanel-editor'].getMarker().clearData();
      const task_id = this.$route.params.id
      const path = `/getimgtag/${task_id}/${this.active_id}`
      this.$axios.get(path)
        .then((response) => {
          let mylist = response.data
          console.log("fanhui")
          console.log(mylist)
          this.$refs['aiPanel-editor'].getMarker().renderData(mylist);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });
    },
    getTaskImg(id) {
      const path = `/gettaskimg/${id}`
      this.$axios.get(path)
        .then((response) => {
          let mylist = response.data
          console.log(mylist)
          var list = []
          for (let i in mylist){
            let address = mylist[i]
            var dict = {}
            address = address.replace("/Users/wclulu/Project/BS/backend/app/api/images","")
            dict['cropImage'] = require(`../../../backend/app/api/images` + address)
            list.push(dict)
          }
          this.pics = list
          this.currentInfo.currentBaseImage=this.pics[0]['cropImage']
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });

       this.active_id = 1
       const path1 = `/getimgtag/${id}/${this.active_id}`
       this.$axios.get(path1)
        .then((response) => {
          let mylist = response.data
          console.log("fanhui")
          console.log(mylist)
          this.$refs['aiPanel-editor'].getMarker().renderData(mylist);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });
    },
    getTags(){
      const path = `/gettag`
      this.$axios.get(path)
        .then((response) => {
          let mylist = response.data
          console.log("haha")
          console.log(mylist)
          var list = []
          for (let i in mylist){
            let tag = mylist[i]
            var dict = {}
            dict['tagName'] = tag['tag_name']
            dict['tag'] = tag['id']
            list.push(dict)
          }
          this.tags = list
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });
    },
    getResult(){
        const task_id = this.$route.params.id
        const path = `/download_VOC/${task_id}`
        this.$axios({
        url: path,
        method: 'POST',
        responseType: 'blob'
        }).then((res) => {
            let data = res.data;
            const blob = new Blob([data], { type: 'application/zip' })
            let link = document.createElement('a')
            link.href = window.URL.createObjectURL(blob)
            link.download = 'task_PASCALVOC.zip'
            link.click()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });
    },
    getResultofCOCO(){
        const task_id = this.$route.params.id
        const path = `/download_COCO/${task_id}`
        this.$axios({
        url: path,
        method: 'POST',
        responseType: 'blob'
        }).then((res) => {
            let data = res.data;
            const blob = new Blob([data], { type: 'application/zip' })
            let link = document.createElement('a')
            link.href = window.URL.createObjectURL(blob)
            link.download = 'task_COCO.zip'
            link.click()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        });        
    }
  },
  created(){
    console.log('created')
    const task_id = this.$route.params.id
    this.getTaskImg(task_id)
    this.getTags()
  },
}
</script>

<style lang="scss" scoped>
.pics {
  width: 100%;
  overflow: hidden;
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  .arrow {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-image: url('http://m.imeitou.com/uploads/allimg/2019072516/3sw3nynp25y.jpg');
    background-repeat: no-repeat;
    background-size: contain;
    &.arrow-right {
      transform: rotate(180deg);
    }
  }
  .pic-container {
    // width: 1180px;
    width: calc(100% - 30px);
    height: 114px;
    margin: 0 auto;
    overflow: hidden;
    .pic-box {
      height: 100%;
      // min-width: 1180px;
      min-width: calc(100% - 30px);
      transition: all 0.5s linear;
      display: flex;
      flex-wrap: nowrap;
    }
    .pic {
      float: left;
      border: 1px solid #ccc;
      box-sizing: border-box;
      margin-right: 10px;
      width: 185px;
      height: 114px;
      .info {
        width: 183px;
        height: 100%;
        background-size: 100%;
        background-repeat: no-repeat;
        background-position: center;
        position: relative;
        &:hover {
          border: 1px solid skyblue;
        }
      }
    }
  }
}
.tagList {
  .title {
    text-align: center;
    font-weight: bold;
  }
  .handleButton {
    width: 100%;
    margin-bottom: 10px;
  }
  .tags {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    .el-icon-delete {
      cursor: pointer;
    }
  }
}
</style>