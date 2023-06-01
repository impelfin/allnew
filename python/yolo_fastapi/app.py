import cv2
import numpy as np
from PIL import Image
from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os.path

app = FastAPI()

os.makedirs("./images", exist_ok=True)
os.makedirs("./results", exist_ok=True)
app.mount("/images", StaticFiles(directory="./images"), name='images')
app.mount("/results", StaticFiles(directory="./results"), name='results')

# “/”로 접근할 때 보여줄 HTML 코드 (가장 기본적으로 보여지는 부분)
@app.get("/")
async def main():
    content = """
        <head>
        <script>
            function getImages() {
                const xhr = new XMLHttpRequest();
                const method = "GET";
                const url = "/getImageList";
                xhr.open(method, url);
                xhr.send();

                xhr.onreadystatechange = function () {
                    if (xhr.readyState !== 4) return;

                    if (xhr.status === 200) {
                        const res = JSON.parse(xhr.response);
                        var imgList = document.getElementById('imgSelect');
                        if (imgList.length === 0) {
                            imgList.innerHTML = "";
                            for (var i = 0; i < res.length; i++) {
                                val = res[i];
                                console.log(val)
                                var option = document.createElement('option')
                                option.innerHTML = val;
                                imgList.append(option)                             
                            }  
                        } else {
                            console.log(imgList.value)
                            predict(imgList.value)
                        }
                    } else {
                        console.log("HTTP error", xhr.status, xhr.statusText);
                    }
                };
            }
            function predict(filename) {
                const xhr = new XMLHttpRequest();
                const method = "GET";
                var url = "/predictYolo";
                url += "?imgName=" + filename;
                xhr.open(method, url);
                xhr.setRequestHeader("content-type", "application/json");
                xhr.send();

                xhr.onload = () => {
                    if (xhr.status === 200) {
                        const res = JSON.parse(xhr.response);
                        console.log(res);
                        const element = document.getElementById("ss1");
                        var tag = '<img src="/results/' + res +  '"' + ' width="600px" height="600px"' + '>';
                        element.innerHTML = tag;
                    } else {
                        console.log("HTTP error", xhr.status, xhr.statusText);
                    }
                };
            }
        </script>
        </head>
        <body>
        <h3>OpenCV Yolo Object Detection</h3>
        <hr />
        <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
        <input name="files" type="file">
        <input type="submit">
        <hr />
        <select id="imgSelect" style="width=100px">
        <input type="button" value="get Images and Predict" onclick="getImages()">
        <div id="section1" style="margin-top: 20px;">
         <span id="ss1"></span>
        </div>
        </form>
        </body>
    """
    return HTMLResponse(content=content)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=3000)

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    UPLOAD_DIRECTORY = "./images"
    for file in files:
        contents = await file.read()
        with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as fp:
            fp.write(contents)
    filename = [file.filename for file in files]
    print({"filename": filename})  
    return {"filename": filename}

@app.get('/getImageList')
async def get_Image_List():
    path_dir = './images'
    file_list = os.listdir(path_dir)
    print(file_list)
    return file_list

@app.get('/predictYolo')
async def predict_yolo(imgName):
    # Yolo 로드
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # 이미지 가져오기
    os.chdir('./images')
    img = cv2.imread(imgName)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # 정보를 화면에 표시
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # 좌표
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # 노이즈 제거
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(boxes), 3))
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            confidence = str(int(round(confidences[i],2) * 100)) + "%"
            label = str(classes[class_ids[i]]) + " " + confidence
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
    imgName = imgName[:-4]
    result = imgName+"_result.jpg"
    os.chdir('../results')
    cv2.imwrite(result, img)
    os.chdir('../')
    return result
