import os, base64
import shutil
import subprocess
from datetime import time, datetime

import cv2
import numpy as np
from flask import request, jsonify, url_for, g, Response
from itsdangerous import json

from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import Task, Image, Tag, Imagetotag
import xml.dom.minidom as Dom
from PIL import Image as IMAGE

basedir = os.path.abspath(os.path.dirname(__file__))

@bp.route('/tasks', methods=['GET'])
# @token_auth.login_required
def get_tasks():
    '''返回任务集合，分页'''
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Task.to_collection_dict(Task.query.order_by(Task.create_time.desc()), page, per_page, 'api.get_tasks')
    return jsonify(data)


@bp.route('/unfinishedtasks', methods=['GET'])
def get_unfinished_tasks():
    '''返回未完成任务集合，分页'''
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Task.to_collection_dict(Task.query.filter(Task.IsFinished == False).order_by(Task.create_time.desc()), page, per_page, 'api.get_tasks')
    return jsonify(data)

@bp.route('/finishedtasks', methods=['GET'])
def get_finished_tasks():
    '''返回未完成任务集合，分页'''
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Task.to_collection_dict(Task.query.filter(Task.IsFinished == True).order_by(Task.create_time.desc()), page, per_page, 'api.get_tasks')
    return jsonify(data)

@bp.route('/gettask/<int:id>', methods=['GET'])
# @token_auth.login_required
def get_task(id):
    '''返回任务内容'''
    task = Task.query.get_or_404(id)
    result = task.to_dict()
    ImgList = []
    images = task.img_member
    for image in images:
        address = image.address
        img = open(address, 'rb')  # 读取图片文件
        data = base64.b64encode(img.read()).decode()  # 进行base64编码
        data = 'data:image/jpg;base64,' + data
        ImgList.append(data)
    result['Img'] = ImgList
    return jsonify(result)

@bp.route('/gettaskimg/<int:id>', methods=['GET'])
# @token_auth.login_required
def get_task_img(id):
    '''返回任务图片'''
    task = Task.query.get_or_404(id)
    ImgList = []
    images = task.img_member
    for image in images:
        address = image.address
        ImgList.append(address)
    return jsonify(ImgList)

@bp.route('/newtask/<int:id>', methods=['POST'])
def create_task(id):
    '''创建一个新任务'''
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')

    message = {}
    if 'title' not in data or not data.get('title', None):
        message['username'] = 'Please provide a valid task name.'
    if 'discription' not in data or not data.get('discription', None):
        message['discription'] = 'Please provide a valid discription.'
    if 'file' not in data or not data.get('file', None):
        message['list'] = 'Please add at least one image.'
    if message:
        return bad_request(message)

    task = Task()  # 先保存task，生成task-url
    task.from_dict(data, id)
    db.session.add(task)
    db.session.commit()
    count = 1
    path = basedir + "/images"
    os.chdir(path)
    os.mkdir(str(task.id))
    for imgData in data['file']:
        if ('data:image/jpeg;base64,' in imgData):
            imgData = imgData.replace('data:image/jpeg;base64,', '')
        elif ('data:image/jpg;base64,' in imgData):
            imgData = imgData.replace('data:image/jpg;base64,', '')
        elif ('data:image/png;base64,' in imgData):
            imgData = imgData.replace('data:image/png;base64,', '')
        image = Image()
        image.task_id = task.id
        # path = basedir + "/images" + "/" + str(task.id) + "/" + str(count) + ".jpg"
        # imgData.save(path)
        os.chdir(path + "/" + str(task.id))
        file = open(str(count) + ".jpg", 'wb')
        imgdata = base64.b64decode(imgData)
        file.write(imgdata)
        file.close()
        image.address = basedir + "/images" + "/" + str(task.id) + "/" + str(count) + ".jpg"
        db.session.add(image)
        db.session.commit()
        count = count + 1
    response = jsonify(task.to_dict())
    return response

# @bp.route('/task/upload',methods=["POST"]) # 方法要与前端一致
# def upload():
#     file_obj = request.files['file']  # Flask中获取文件
#     if file_obj is None:
#         return "未上传文件"
#     #保存文件
#     file_path = os.path.join(basedir/, "1.jpg")
#     file_obj.save(file_path)
#     return file_path

@bp.route('/addtag', methods=['POST'])
def add_tag():
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    tag = Tag()
    tag.id = data['tag_id']
    tag.tag_name = data['tag_name']
    db.session.add(tag)


@bp.route('/gettag', methods=['GET'])
# @token_auth.login_required
def get_tag():
    '''返回所有标签'''
    result = []
    tags = Tag.query.all()
    for tag in tags:
        result.append(tag.to_dict())
    print(result)
    return jsonify(result)


@bp.route('/getimgtag/<int:task_id>/<int:img_id>', methods=['GET'])
def get_img_tag(task_id, img_id):
    '''返回某图片的标签'''
    task = Task.query.get_or_404(task_id)
    image = task.img_member[img_id - 1]
    imgtotag = image.tags
    result = []
    for item in imgtotag:
        dic = {}
        dic['tag'] = item.tag_id
        tag = Tag.query.get_or_404(item.tag_id)
        dic['tagName'] = tag.tag_name
        pos = {}
        pos['x'] = item.x
        pos['x1'] = item.x1
        pos['y'] = item.y
        pos['y1'] = item.y1
        dic['position'] = pos
        dic['uuid'] = tag.uuid
        result.append(dic)
    print(result)
    return jsonify(result)

@bp.route('/loadtag/<int:id>', methods=['PUT'])
def loadTag(id):
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    task = Task.query.get_or_404(id)
    image = task.img_member[int(data['img_id'])-1]
    count = 1
    for info in data['allInfo']:
        tagtoimg = Imagetotag()
        if info['tagName'] == "请选择或添加新标签":
            print("请选择或添加新标签")
            continue
        if Imagetotag.query.filter(Imagetotag.image_id == image.id).filter(Imagetotag.tag_id == info['tag']).first():
            print(Imagetotag.query.filter(Imagetotag.image_id == image.id).filter(Imagetotag.tag_id == info['tag']))
            print("标签已存在1")
            continue
        if Tag.query.filter_by(tag_name=info['tagName']).first():
            tag = Tag.query.filter_by(tag_name=info['tagName']).first()
            print("标签已存在2")
        else:
            tag = Tag()
            tag.tag_name = info['tagName']
            tag.uuid = info['uuid']
            db.session.add(tag)
            db.session.commit()
        tagtoimg.tag_id = tag.id
        tagtoimg.tag_count = count
        tagtoimg.x = info['position']['x']
        tagtoimg.x1 = info['position']['x1']
        tagtoimg.y = info['position']['y']
        tagtoimg.y1 = info['position']['y1']
        tagtoimg.image_id = image.id
        db.session.add(tagtoimg)
        db.session.commit()
        count += 1
    response = jsonify(task.to_dict())
    return response

@bp.route('/finishtask/<int:id>', methods=['PUT'])
def finish_task(id):
    task = Task.query.get_or_404(id)
    images = task.img_member
    message = {}
    for image in images:
        if image.tags:
            continue
        message['warning'] = '仍有图片未完成标注'
    if message:
        print(message)
        return bad_request(message)
    task.IsFinished = True
    task.finish_time = datetime.now()
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict())

@bp.route('/download_VOC/<int:id>', methods=['POST'])
def download(id):
    task = Task.query.get_or_404(id)
    images = task.img_member
    path = basedir + "/PascalVOC"
    newdir = basedir + "/Zip_1"
    os.chdir(path)
    if os.path.exists(str(id)):
        print(1)
    else:
        os.mkdir(str(id))
        os.chdir(path + "/" + str(id))
        path_old = basedir + "/images" + "/" + str(id)
        path_new = basedir + "/PascalVOC" + "/" + str(id) + "/" + "JPEGImages"
        shutil.copytree(path_old, path_new)
        os.mkdir('Annotations')
        os.chdir(path + "/" + str(id) + "/Annotations")
        annopath = path + "/" + str(id) + "/Annotations"
        count = 1
        data = ""
        for image in images:
            data = data + str(count) + ".jpg" + '\n'
            im = IMAGE.open(image.address)
            width = im.size[0]
            height = im.size[1]
            createXML(id, str(count), width, height, image.tags, annopath)
            count += 1

        print(data)
        os.chdir(path + "/" + str(id))
        os.mkdir('ImageSets')
        os.chdir(path + "/" + str(id) + "/ImageSets")
        os.mkdir('Main')
        os.chdir(path + "/" + str(id) + "/ImageSets/Main")
        file = open("images.txt", 'w')
        file.write(data)
        file.close()
        shutil.make_archive(newdir+"/"+str(id), 'zip', path + "/" + str(id), )

    os.chdir(newdir)
    f = open(str(id)+".zip", 'rb')
    return f.read()

def createXML(id, img, width, height, items, annopath):
    doc = Dom.Document()
    root_node = doc.createElement("annotation")

    folder_node = doc.createElement("folder")
    folder_value = doc.createTextNode(str(id))
    folder_node.appendChild(folder_value)
    root_node.appendChild(folder_node)

    filename_node = doc.createElement("filename")
    filename_value = doc.createTextNode(img+".jpg")
    filename_node.appendChild(filename_value)
    root_node.appendChild(filename_node)

    source_node = doc.createElement("source")
    source_value = doc.createTextNode("")
    source_node.appendChild(source_value)
    root_node.appendChild(source_node)


    size_node = doc.createElement("size")

    size_width_node = doc.createElement("width")
    size_width_value = doc.createTextNode(str(width))
    size_width_node.appendChild(size_width_value)
    size_node.appendChild(size_width_node)

    size_height_node = doc.createElement("height")
    size_height_value = doc.createTextNode(str(height))
    size_height_node.appendChild(size_height_value)
    size_node.appendChild(size_height_node)

    size_depth_node = doc.createElement("depth")
    size_depth_value = doc.createTextNode("3")
    size_depth_node.appendChild(size_depth_value)
    size_node.appendChild(size_depth_node)

    root_node.appendChild(size_node)

    segmented_node = doc.createElement("segmented")
    segmented_value = doc.createTextNode("0")
    segmented_node.appendChild(segmented_value)
    root_node.appendChild(segmented_node)

    for item in items:
        tag = Tag.query.get_or_404(item.tag_id)
        object_node = doc.createElement("object")

        name_node = doc.createElement("name")
        name_value = doc.createTextNode(tag.tag_name)
        name_node.appendChild(name_value)
        object_node.appendChild(name_node)

        pose_node = doc.createElement("pose")
        pose_value = doc.createTextNode("Unspecified")
        pose_node.appendChild(pose_value)
        object_node.appendChild(pose_node)

        truncated_node = doc.createElement("truncated")
        truncated_value = doc.createTextNode("0")
        truncated_node.appendChild(truncated_value)
        object_node.appendChild(truncated_node)

        difficult_node = doc.createElement("difficult")
        difficult_value = doc.createTextNode("0")
        difficult_node.appendChild(difficult_value)
        object_node.appendChild(difficult_node)

        bndbox_node = doc.createElement("bndbox")
        xmin_node = doc.createElement("xmin")
        aa = float(item.x.strip('%'))  # 去掉s 字符串中的 %
        bb = aa / 100.0
        xmin_value = doc.createTextNode(str(bb*width))
        xmin_node.appendChild(xmin_value)
        bndbox_node.appendChild(xmin_node)

        ymin_node = doc.createElement("ymin")
        aa = float(item.y.strip('%'))  # 去掉s 字符串中的 %
        bb = aa / 100.0
        ymin_value = doc.createTextNode(str(bb*height))
        ymin_node.appendChild(ymin_value)
        bndbox_node.appendChild(ymin_node)

        xmax_node = doc.createElement("xmax")
        aa = float(item.x1.strip('%'))  # 去掉s 字符串中的 %
        bb = aa / 100.0
        xmax_value = doc.createTextNode(str(bb*width))
        xmax_node.appendChild(xmax_value)
        bndbox_node.appendChild(xmax_node)

        ymax_node = doc.createElement("ymax")
        aa = float(item.y1.strip('%'))  # 去掉s 字符串中的 %
        bb = aa / 100.0
        ymax_value = doc.createTextNode(str(bb*height))
        ymax_node.appendChild(ymax_value)
        bndbox_node.appendChild(ymax_node)

        object_node.appendChild(bndbox_node)
        root_node.appendChild(object_node)

    doc.appendChild(root_node)
    filepath = annopath + "/" + img + ".xml"
    f = open(filepath, "wb")
    f.write(doc.toprettyxml(indent="\t", newl="\n", encoding="utf-8"))
    f.close()


@bp.route('/download_COCO/<int:id>', methods=['POST'])
def downloadCOCO(id):
    task = Task.query.get_or_404(id)
    images = task.img_member
    path = basedir + "/COCO"
    newdir = basedir + "/Zip_2"
    os.chdir(path)
    if os.path.exists(str(id)):
        print(1)
    else:
        os.mkdir(str(id))
        os.chdir(path + "/" + str(id))
        path_old = basedir + "/images" + "/" + str(id)
        path_new = basedir + "/COCO" + "/" + str(id) + "/" + "JPEGImages"
        shutil.copytree(path_old, path_new)
        os.mkdir('Annotations')
        annopath = path + "/" + str(id) + "/Annotations"
        os.chdir(annopath)
        jsonresult = createJson(id, images)
        file = open("instances.json", 'w')
        file.write(jsonresult)
        file.close()
        shutil.make_archive(newdir + "/" + str(id), 'zip', path + "/" + str(id), )

    os.chdir(newdir)
    f = open(str(id) + ".zip", 'rb')
    return f.read()

def createJson(id, images):
    jsontext = {"info":{},
     "licenses": {},
     "images": [],
     "annotation": [],
     "categories":[]}
    count = 1
    task = Task.query.get_or_404(id)
    taglist = []
    for image in images:
        image_dic={}
        image_dic["lisence"] = ""
        image_dic["name"] = str(count)+".jpg"
        image_dic["coco_url"] = ""
        im = IMAGE.open(image.address)
        width = im.size[0]
        height = im.size[1]
        image_dic["height"] = height
        image_dic["width"] = width
        image_dic["date_captured"] = str(task.finish_time)
        image_dic["flicker_url"] = ""
        image_dic["id"] = count
        jsontext["images"].append(image_dic)
        for tag in image.tags:
            flag = 1
            ano_dic={}
            ano_dic["segmentation"] = []
            ano_dic["area"] = height*width
            ano_dic["iscrowd"] = 0
            ano_dic["image_id"] = count
            x = float(tag.x.strip('%')) / 100.0
            y = float(tag.y.strip('%')) / 100.0
            x1 = float(tag.x1.strip('%')) / 100.0
            y1 = float(tag.y1.strip('%')) / 100.0
            w = (x1-x)*width
            h = (y1-y)*height
            ano_dic["bbox"] = [x*width, y*height, w, h]
            ano_dic["category_id"] = tag.tag_id
            ano_dic["id"] = flag
            flag += flag
            jsontext["annotation"].append(ano_dic)

            if tag.tag_id not in taglist:
                findtag = Tag.query.get_or_404(tag.tag_id)
                tag_dic = {}
                tag_dic["supercategory"] = findtag.tag_name
                tag_dic["id"] = tag.tag_id
                tag_dic["name"] = findtag.tag_name
                taglist.append(tag.tag_id)
                jsontext["categories"].append(tag_dic)
        count += count
    jsondata = json.dumps(jsontext, indent=4, separators=(',', ': '))
    return jsondata

@bp.route('/newtask_test/<int:id>', methods=['POST'])
def create_task_test(id):
    '''创建一个新任务'''
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    message = {}
    if 'title' not in data or not data.get('title', None):
        message['username'] = 'Please provide a valid task name.'
    if 'discription' not in data or not data.get('discription', None):
        message['discription'] = 'Please provide a valid discription.'
    if ('file' not in data or not data.get('file', None)) and ('video' not in data or not data.get('video', None)):
        message['list'] = 'Please add at least one image or video.'
    if message:
        return bad_request(message)

    task = Task()  # 先保存task，生成task-url
    task.from_dict(data, id)
    db.session.add(task)
    db.session.commit()
    count = 1
    if 'file' in data or data.get('file', None):
        path = basedir + "/images"
        os.chdir(path)
        os.mkdir(str(task.id))
        for imgData in data['file']:
            if ('data:image/jpeg;base64,' in imgData):
                imgData = imgData.replace('data:image/jpeg;base64,', '')
            elif ('data:image/jpg;base64,' in imgData):
                imgData = imgData.replace('data:image/jpg;base64,', '')
            elif ('data:image/png;base64,' in imgData):
                imgData = imgData.replace('data:image/png;base64,', '')
            image = Image()
            image.task_id = task.id
            # path = basedir + "/images" + "/" + str(task.id) + "/" + str(count) + ".jpg"
            # imgData.save(path)
            os.chdir(path + "/" + str(task.id))
            file = open(str(count) + ".jpg", 'wb')
            imgdata = base64.b64decode(imgData)
            file.write(imgdata)
            file.close()
            image.address = basedir + "/images" + "/" + str(task.id) + "/" + str(count) + ".jpg"
            db.session.add(image)
            db.session.commit()
            count = count + 1

    if 'video' in data or data.get('video', None):
        flag = 0
        path = basedir + "/video"
        for viData in data['video']:
            if ('data:video/mp4;base64,' in viData):
                viData = viData.replace('data:video/mp4;base64,', '')
            os.chdir(path)
            file = open(str(flag) + ".mp4", 'wb')
            vidata = base64.b64decode(viData)
            file.write(vidata)
            file.close()

            videopath = path + "/" + str(flag) + ".mp4"
            cap = cv2.VideoCapture(videopath)  # 获取视频对象
            isOpened = cap.isOpened  # 判断是否打开
            # 视频信息获取
            fps = cap.get(cv2.CAP_PROP_FPS)
            imageNum = 0
            sum = 0
            timef = 50  # 隔50帧保存一张图片

            while (isOpened):
                sum += 1
                (frameState, frame) = cap.read()  # 记录每帧及获取状态
                if frameState == True and (sum % timef == 0):
                    # 格式转变，BGRtoRGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # 转变成Image
                    frame = IMAGE.fromarray(np.uint8(frame))
                    frame = np.array(frame)
                    # RGBtoBGR满足opencv显示格式
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    imageNum = imageNum + 1
                    fileName = basedir + "/images/" + str(task.id) + "/" + str(count) + '.jpg'  # 存储路径
                    cv2.imwrite(fileName, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
                    print(fileName + " successfully write in")  # 输出存储状态
                    newimage = Image()
                    newimage.task_id = task.id
                    newimage.address = basedir + "/images" + "/" + str(task.id) + "/" + str(count) + ".jpg"
                    db.session.add(newimage)
                    db.session.commit()
                    count += 1

                elif frameState == False:
                    break
            print('finish!')
            cap.release()
            flag += 1

    shutil.rmtree(basedir + "/video")
    os.chdir(basedir)
    os.mkdir("video")
    response = jsonify(id)
    return response

