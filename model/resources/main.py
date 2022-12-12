import numpy as np
import cv2
import random
import string
# step 1 - load the model
import datetime
net = cv2.dnn.readNet('./runs/train/exp24/weights/best.onnx')


# step 2 - feed a 640x640 image to get predictions

def format_yolov5(frame):
    row, col, _ = frame.shape
    _max = max(col, row)
    result = np.zeros((_max, _max, 3), np.uint8)
    result[0:row, 0:col] = frame
    return result


# input_path ='./CovidDataSet/test/images/img_244.jpg'
# file_name = input_path.split('/')[-1]
def detect(img):
    image = img
    input_image = format_yolov5(image)  # making the image square
    blob = cv2.dnn.blobFromImage(input_image, 1 / 255.0, (640, 640), swapRB=True)
    net.setInput(blob)
    predictions = net.forward()

    # step 3 - unwrap the predictions to get the object detections
    class_ids = []
    confidences = []
    boxes = []
    output_data = predictions[0]
    image_width, image_height, _ = input_image.shape
    x_factor = image_width / 640
    y_factor = image_height / 640

    for r in range(25200):
        row = output_data[r]
        confidence = row[4]
        if confidence >= 0.4:

            classes_scores = row[5:]
            _, _, _, max_indx = cv2.minMaxLoc(classes_scores)
            class_id = max_indx[1]
            if (classes_scores[class_id] > .25):
                confidences.append(confidence)

                class_ids.append(class_id)

                x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                left = int((x - 0.5 * w) * x_factor)
                top = int((y - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)

    class_list = []
    with open("classes.txt", "r") as f:
        class_list = [cname.strip() for cname in f.readlines()]

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45)

    result_class_ids = []  #识别图片中所有框的类别
    result_confidences = []
    result_boxes = []

    for i in indexes:
        result_confidences.append(confidences[i])
        result_class_ids.append(class_ids[i])
        result_boxes.append(boxes[i])
    total_sum=0
    pass_sum=0;
    for i in range(len(result_class_ids)):
        if result_class_ids[i]==0 or result_class_ids[i]==3 or result_class_ids[i]==5:
            total_sum=total_sum+1
        if result_class_ids[i]==6:
            pass_sum=pass_sum+1
    print("总数量：",total_sum)
    print()
    print("及格数量：",pass_sum)
    for i in range(len(result_class_ids)):
        box = result_boxes[i]
        class_id = result_class_ids[i]
        cv2.rectangle(image, box, (255, 0, 0), 2)
        cv2.putText(image, class_list[class_id], (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255))
    #获取当前的检测时间
    now_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result={"s_num":total_sum,"v_num":pass_sum,"image":image,"now_date":now_date}
    return result



import base64

from flask import request, json

from flask import Flask

app = Flask(__name__)  # 一个flask类的对象
app.debug = True  # 开启debug 在调试过程中不需要每次修改都重新运营


@app.route('/model', methods=['POST', 'GET'])
def model():
    print("aaaaaaaaa")
    if request.method == 'POST':
        edit_attr = request.form.get("attr")  # 从网络请求输入中获取参数
        print("input edit_attr:", edit_attr)
        # 从网络请求输入中获取base64编码后进行传输的图片
        origin_image=request.files.get("image").read()
        # origin_image = base64.b64decode(request.files.get("image"))
        # print(origin_image)
        # 将图片存在代码同目录下的static文件夹中，存为11111.jpg
        origin_image_Name=create_string_number(8)
        origin_image_Path="../static/originImage/"+origin_image_Name+".jpg"
        with open(origin_image_Path, "wb") as f:
            f.write(origin_image)
        detect_image=cv2.imread(origin_image_Path)
        result = detect(detect_image)
        result_img=result.get("image")
        img_local_path = '../static/detectImage/'+origin_image_Name+".jpg"
        cv2.imwrite(img_local_path,result_img)
        # 将处理结束存在static中的222.jpg图片先base64编码再转为字符串
        with open(img_local_path, 'rb') as f:
            img_stream = f.read()
            img_stream = str(base64.b64encode(img_stream),encoding='utf-8')
        # 将要返回小程序的数据存进列表中
        info = {'result': 'successfully edited!', 'editimg': img_stream,'s_num':result.get("s_num"),'v_num':result.get("v_num"),'now_date':result.get("now_date")}
    else:
        info = {'result': 'failed!'}
    # 数据返回小程序
    return json.dumps(info, ensure_ascii=False)


# 路由 装饰器的方式
@app.route('/index')  # 地址
def index():
    print("aaaa")
    return "Hello work"

def create_string_number(n):
    """生成一串指定位数的字符+数组混合的字符串"""
    m = random.randint(1, n)
    a = "".join([str(random.randint(0, 9)) for _ in range(m)])
    b = "".join([random.choice(string.ascii_letters) for _ in range(n - m)])
    return ''.join(random.sample(list(a + b), n))
if __name__ == '__main__':
    # img = cv2.imread("./CovidDataSet/test/images/img_1221.jpg")
    # img = detect(img)
    # cv2.imshow("output",img)
    # cv2.waitKey()
    app.run('localhost', 8082)  # run_simple("localhost", 4000, hello)
