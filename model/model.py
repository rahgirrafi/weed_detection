import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path="custom3.pt",force_reload=True)

torch.save(model.model, "weed_detector.pth" )

    