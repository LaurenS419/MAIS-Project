# YOLO Security

By Lauren Spee for MAIS 202

YOLO Security is a home security application that harnesses the power of computer vision to keep the user safer and in the loop about the security of their home. It connects to the cameras around the user's house to keep an extra set of eyes on the perimeter. If the model sees a person, a car, or an animal, it will send the user a notification with an image of what it saw. This allows the homeowner to know in real-time what's happening outside their house, whether they're there or not.

Currently, the prototype is run on a web app, with a place where the user can upload a video of their own to see the model in action.

## Information
The product uses the YOLOv5 model, a lightweight and fast object-detection model that can run in real-time. It was trained on the Pascal VOC 2007 and 2012 datasets to generate weights and optimize hyperparameters. The model is used to identify objects, classify them, and render bounding boxes on video frames as it's happening.

### Performance 
The final model has a mean average precision value of 71%

### Organization

This repository holds the training notebook and video processing scripts, along with the code for the webapp.
\n```Deliverables/``` holds MAIS 202 project reports
\n```webapps/``` holds the code to run the flask webapp
\n```heroku_attepmts/``` contain my wip code to get this webapp running on heroku
\n```YOLOv5_Training.ipynb``` the jupyter notebook used to train the model
\n```process_footage.py```  the python script used to run the security footage through the model

### Possible improvements
Given time, my plan is to get this webapp running on heroku, and improve the weights for better performance.

## How to run

### Webapp
1. Clone this repository
2. Navigate to ```/webapp```
3. Download the dependencies via ```pip install -r requirements.txt```
4. Run the app with ```flask run```
5. It should give you a locally hosted link to access the site

### Scripts
1. Training
     1. Run the training notebook either in Google Colab or on your laptop (must have an NVIDIA GPU and have CUDA and cuDNN installed)
     2. To get weights, go to ```yolov5/runs/train/expX/weights``` (replace X with your most recent training run number)
2. Running
    1. Import the weights file into the root directory of this project
    2. Download a video you want processed into the root directory, and make sure the paths in ```process_footage.py``` are right
    3. Run ```process_footage.py```
