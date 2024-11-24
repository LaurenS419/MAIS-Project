import os
import time
import torch
import cv2
import shutil

def captureVideo2(file, output_video="output_video.mp4"):
    video_path = file
    cap = cv2.VideoCapture(video_path)
    second_rate = 2  # only save frames every 2 seconds to avoid spam
    frame_dir = "frames"
    confidence_cap = 0.6

    # remove frame directory if it already exists
    if os.path.exists(frame_dir):
        print("Removed old frames directory.")
        shutil.rmtree(frame_dir)
    os.makedirs(frame_dir)

    # video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frames_to_skip = int(fps * second_rate)

    # init the video writer with XVID codec
    fourcc = cv2.VideoWriter_fourcc(*'XVID') 
    out = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))

    frame_count = 0
    last_saved_frame = -frames_to_skip

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:  # if no more frames, stop
            break

        # do object detection
        results = model(frame) 

        # filter results based on confidence and labels
        filtered_results = []

        for i, (xmin, ymin, xmax, ymax, confidence, class_idx) in enumerate(results.xyxy[0]):
            label = model.names[int(class_idx)]  # get label
            
            if confidence > confidence_cap and label in {"car", "person", "animal"}:
                filtered_results.append((xmin, ymin, xmax, ymax, confidence, class_idx))

        # render filtered results on frame
        for xmin, ymin, xmax, ymax, confidence, class_idx in filtered_results:
            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)

            cv2.putText(frame, f"{model.names[int(class_idx)]} {confidence:.2f}", 
                        (int(xmin), int(ymin) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        out.write(frame) # write frame to output video

        # Save frames every second_rate to the frames directory
        if frame_count - last_saved_frame >= frames_to_skip and filtered_results:
            last_saved_frame = frame_count
            frame_filename = f'{frame_dir}/frame_{frame_count:04d}.jpg'
            cv2.imwrite(frame_filename, frame)

        frame_count += 1

    cap.release()
    out.release() 

    #print(f"Saved processed video as '{output_video}'")

if __name__ == "__main__":
    #load YOLOv5 model, ensure path to weights is correct
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt')

    captureVideo2("downloaded_video_0.mp4") 
