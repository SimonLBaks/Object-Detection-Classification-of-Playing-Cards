from ultralytics import YOLO
from comet_ml import Experiment

if __name__ == '__main__':
    # Create an experiment with your api key
    experiment = Experiment(
        api_key=" ",
        project_name="Training",
        workspace="chinesewarlord",
    )

    model = YOLO("yolov8m.pt")

    model.train(data = "data.yaml",imgsz=640,epochs=100,batch=-1,workers=8)