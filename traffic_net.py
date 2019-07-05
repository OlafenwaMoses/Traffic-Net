from io import open
import requests
import shutil
from zipfile import ZipFile
from imageai.Prediction.Custom import ModelTraining, CustomImagePrediction
import os

execution_path = os.getcwd()

SOURCE_PATH = "https://github.com/OlafenwaMoses/Traffic-Net/releases/download/1.0/trafficnet_dataset_v1.zip"
FILE_DIR = os.path.join(execution_path, "trafficnet_dataset_v1.zip")
DATASET_DIR = os.path.join(execution_path, "trafficnet_dataset_v1.zip")


def download_traffic_net():
    if (os.path.exists(FILE_DIR) == False):
        print("Downloading trafficnet_dataset_v1.zip")
        data = requests.get(SOURCE_PATH,
                            stream=True)

        with open(FILE_DIR, "wb") as file:
            shutil.copyfileobj(data.raw, file)
        del data

        extract = ZipFile(FILE_DIR)
        extract.extractall(execution_path)
        extract.close()


def train_traffic_net():
    download_traffic_net()

    trainer = ModelTraining()
    trainer.setModelTypeAsResNet()
    trainer.setDataDirectory("trafficnet_dataset_v1")
    trainer.trainModel(num_objects=4, num_experiments=200, batch_size=32, save_full_model=True, enhance_data=True)

def run_predict():
    predictor = CustomImagePrediction()
    predictor.setModelPath(model_path="trafficnet_resnet_model_ex-055_acc-0.913750.h5")
    predictor.setJsonPath(model_json="model_class.json")
    predictor.loadFullModel(num_objects=4)

    predictions, probabilities = predictor.predictImage(image_input="images/1.jpg", result_count=4)
    for prediction, probability in zip(predictions, probabilities):
        print(prediction, " : ", probability)

#Un-comment the line below to train your model
#train_traffic_net()

#Un-comment the line below to run predictions
run_predict()

