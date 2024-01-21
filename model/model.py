import torch
import os 
import cv2


 
def save_model():
    torch.save(model.model, "weed_detector" )

def load_model():
    model.model = torch.load("weed_detector")



image_dir = "data/images/"
output_dir = "data/output/"
os.makedirs(output_dir, exist_ok=True)
model = torch.hub.load('ultralytics/yolov5', 'custom', path="custom3.pt")

def detect_image(image_path):
    for filename in os.listdir(image_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            # Load an image
            image_path = os.path.join(image_dir, filename)
            image = cv2.imread(image_path)

            # Preprocess the image
            img = model.preprocess(image)
            img = torch.from_numpy(img).to(device='cuda').unsqueeze(0)

            # Perform inference
            with torch.no_grad():
                prediction = model(img)[0]

            # Post-process the prediction
            prediction = model.postprocess(prediction)

            # Draw bounding boxes on the image
            result_image = model.show_result(image, prediction)

            # Save the result image
            output_path = os.path.join(output_dir, f'detected_{filename}')
            cv2.imwrite(output_path, result_image)


	