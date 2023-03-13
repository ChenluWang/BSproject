# backend

### 1. 主要代码解释

主要代码全部存在于 app 文件夹中，对该文件夹内容作出一点解释：

- app/models 保存了所有用到的类（与数据库中存储方式对应）
- app/api 中主要实现了与前端的接口
  - .py 文件记录了后端与前端通信的所有 API 接口
  - images 保存了前端传来的图片文件（目前只留下了 id=58 任务的图片，仅作展示）
  - video 保存了前端传来的视频文件（实际工作中将视频文件转为图片后保存在 images 文件夹中，然后删除 video 中的视频原文件【节省空间】）
  - COCO 保存了生成的 COCO 数据集类型任务结果（目前只留下了 id=58 任务的结果，仅作展示）
  - Pascal VOC 保存了生成的 Pascal VOC 数据集类型任务结果（目前只留下了 id=58 任务的结果，仅作展示）
  - Zip_1 保存了 Pascal VOC 数据集类型任务结果的压缩包（目前只留下了 id=58 任务的结果，仅作展示）
  - Zip_2 保存了 COCO 数据集类型任务结果的压缩包（目前只留下了 id=58 任务的结果，仅作展示）



### 2. 运行指南

app 的初始化在 main.py 中完成，初始化设置时请将 main.py 作为运行目录

config.py 中记录了在我的环境下与我的 mysql 连接的端口及密码，更换环境后请修改SQLALCHEMY_DATABASE_URI ，否则会导致连接数据库失败



### 3. 数据库建立指南

推荐通过Migrate管理项目数据库，具体方法如下：

#### (1) 创建迁移存储库

```
(venv) D:\python-code\flask-vuejs-madblog\back-end>flask db init
```

#### (2) 生成迁移脚本

```
(venv) D:\python-code\flask-vuejs-madblog\back-end>flask db migrate -m "你的描述"
```

#### (3) 将迁移脚本应用到数据库中

```
(venv) D:\python-code\flask-vuejs-madblog\back-end>flask db upgrade
```

> 说明： `flask db downgrade` 命令可以回滚上次的迁移

