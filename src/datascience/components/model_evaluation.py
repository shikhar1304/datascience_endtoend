import os
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import joblib
from src.datascience import logger

from src.datascience.entity.config_entity import ModelEvaluationConfig
from src.datascience.constants import *
from src.datascience.utils.common import read_yaml, create_directories,save_json

import os
os.environ["MLFLOW_TRACKING_URI"]="https://dagshub.com/shikharmathur43/datascience_endtoend.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"]="shikharmathur43"
os.environ["MLFLOW_TRACKING_PASSWORD"]="be3dbaa491639ac6fee295b25ea386c3f1c00a4c"


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self,actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2
    
    def log_into_mlflow(self):

        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[[self.config.target_column]]


        mlflow.set_tracking_uri(self.config.mlflow_uri)  #allows you to specify the location where MLflow should store and manage your registered models.
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():

            predicted_qualities = model.predict(test_x)

            (rmse, mae, r2) = self.eval_metrics(test_y, predicted_qualities)
            
            # Saving metrics as local
            scores = {"rmse": rmse, "mae": mae, "r2": r2}
            save_json(path=Path(self.config.metric_file_name), data=scores)

            mlflow.log_params(self.config.all_params)

            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mae", mae)


            # Model registry does not work with file store
            try:
                mlflow.sklearn.log_model(
                    sk_model=model,
                    artifact_path="model"
                )
                logger.info("Model logged successfully to MLflow.")
            except Exception as e:
                logger.warning(f"Failed to log model to registry, logged as artifact only: {e}")


    
