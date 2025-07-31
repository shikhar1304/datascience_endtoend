import os
import urllib.request as request
import pandas as pd
from src.datascience import logger
import zipfile
from sklearn.model_selection import train_test_split

from src.datascience.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(self,config:DataTransformationConfig):
        self.config = config

    def trainTestSplit(self)->bool:
        data = pd.read_csv(self.config.data_path)

        train,test = train_test_split(data)
        train.to_csv(os.path.join(self.config.root_dir,"train.csv"),index = True)
        test.to_csv(os.path.join(self.config.root_dir,"test.csv"),index = True)

        logger.info("Splited data into training and test sets")
        logger.info(train.shape)
        logger.info(test.shape)

        print(train.shape)
        print(test.shape)
