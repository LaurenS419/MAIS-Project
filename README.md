# YOLO Security

By Lauren Spee for MAIS 202

## Information
YOLO Security is a home security application that harnesses the power of computer vision to keep the user safer and in the loop about the security of their home. It connects to the cameras around the user's house, giving them the additional functionality of providing live updates of objects detected around their home. If the model sees a person, a car, or an animal, it will send the user an update with an image of what it found. This allows the homeowner to know in real-time what's happening outside their house, whether they're there or not. 

The product uses the YOLOv5 model, a lightweight and fast object-detection model that can detect objects in real-time. It was trained on the Pascal VOC 2007 and 2012 datasets to generate weights and optimize hyperparameters. The model is used to identify objects, classify them, and render bounding boxes on video frames as it's happening.

Currently, the prototype uses stock security camera footage to showcase what it does on a web app. Check it out here ____

## How to run

### Website
Check it out here! _____

### Scripts

#### Training
Run the training notebook either in Google Colab or on your laptop with CUDA and cuDNN installed. The model takes care of downloading the dataset and setting training/validation paths. Go into yolov5/runs/train/expX/weights (replace *X* with your most recent training run number) to get your learned weights from the training.

#### Running
Import the weights file into the working directory where all the scripts are located, and run the process_footage.py script.

