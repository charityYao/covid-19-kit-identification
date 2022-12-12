# Project Name
A novel coronavirus antigen kit recognition method based on yolov5 and opencv

# Project Introduction

Nucleic acid testing has become an essential part of people's lives in order to reduce the spread of the novel coronavirus,which has swept the world and has yet to be effectively treated and controlled. However, nucleic acid testing requires special testing machines and specialized laboratories, which are highly sensitive and usually take 4-6 hours to produce results. Therefore, nucleic acid testing is expensive and time-consuming. The novel coronavirus antigen self-testing kit has low cost,convenient and fast detection, which is favored by the market and effectively realizes home-based monitoring. Therefore, the industry has a good development prospect.  

There are a large number of people in China who need nucleic acid testing every day. Under such circumstances, the use of COVID-19 antigen detection kits for self-testing has played a huge role in improving the efficiency of COVID-19 detection and achieving better control.  
At present, the detection and classification of COVID-19 reagent results mainly rely on manual work. The rectangular structure detection of the label frame required on 
the dense COVID-19 antigen reagent detection strip is a tedious and relatively easy work, which often requires a large number of manpower for classification and   statistics. Therefore, this technology proposes an AI-based parallel detection method for the label frame required on the detection strip using the OPEN CV     library,which can simultaneously detect and classify all results in high-resolution images without reducing the accuracy of the results.  

In order to minimize the amount of human and material resources needed to detect COVID-19, we decided to use OPEN CV to design a neural network to train images
of COVID-19 antigen detection kits. It is also hoped that it can identify the number of kits in the newly imported COVID-19 antigen detection kit pictures, 
the number of reagent test strips, the area where the reagent test strips should be tested,and whether the test results of the reagent test strips are effective,
and then output a new picture label frame to save the time and cost of manual identification.

miniprogram-1 file stored the foreground code of the project, and model placed the model code of the project adapted from yolov5.There is no training set for the novel crown reagent in the project, only a few sample pictures are provided. If researchers need it, please send your request to gdut_wangyao@163.com.
# Environment    
The environment configuration of this project is as follows (requirements.txt) :  
Albumentations = = 1.3.0  
Comet_ml = = 3.31.20  
Coremltools = = 6.1  
Flask = = 2.2.2  
Ipython = = 8.7.0  
Matplotlib = = 3.6.2  
MSS = = 7.0.1  
Numpy = = 1.21.6  
Onnx = = 1.12.0  
Onnxruntime = = 1.13.1  
Onnxsim = = 0.4.10  
Opencv_python = = 4.5.5.62  
Openvino = = 2022.2.0  
Paddle = = 1.0.2  
Pafy = = 0.5.5  
Pandas = = 1.5.1  
Pillow = = 9.3.0  
Psutil = = 5.9.4  
Pycocotools = = 2.0.6  
PyYAML = = 6.0  
Requests the = = 2.28.1  
Scipy = = 1.9.3  
Seaborn = = 0.12.1  
Setuptools = = 65.5.1  
Tensorflow = = 2.11.0  
Tensorflowjs = = 4.1.0  
Tensorrt = = 8.5.1.7  
Tflite_runtime = = 2.11.0  
Tflite_support = = 0.4.3  
Thop = = while post2209072238  
The torch = = 1.7.1  
Torchvision = = 0.8.2  
TQDM = = 4.64.1  
Tritonclient = = 2.28.0  
X2paddle = = 1.3.9  
 
# Testing
```python
python detect.py  --weights runs/train/exp16/weights/best.pt --source ./CovidDataSet/test/image
```

# Training
```python
python train.py --img 640 --batch 8 --epochs 200 --data ./CovidDataSet/data.yaml --cfg models/yolov5x.yaml --weights weights/yolov5x.pt --cache ram
```

