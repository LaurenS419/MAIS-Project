# YOLO Security

By Lauren Spee for MAIS 202

YOLO Security is a home security application that harnesses the power of computer vision to keep the user safer and in the loop about the security of their home. It connects to the cameras around the user's house, giving them the additional functionality of providing live updates of objects detected around their home. If the model sees a person, a car, or an animal, it will send the user an update with an image of what it found. This allows the homeowner to know in real-time what's happening outside their house, whether they're there or not. 

The product uses the YOLOv5 model, a lightweight and fast object-detection model that can detect objects in real-time. It was trained on the Pascal VOC 2007 and 2012 datasets to generate weights and optimize hyperparameters. The model is used to identify objects, classify them, and render bounding boxes on video frames as it's happening.

Currently, the prototype uses stock security camera footage to showcase what it does on a web app.

