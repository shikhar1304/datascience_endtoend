from src.datascience.constants import *
from src.datascience.utils.common import read_yaml,create_directories
from src.datascience.entity.config_entity import (DataIngestionConfig)

class ConfigurationManager:
    def __init__(self,
                 config_fiePath=CONFIG_FILE_PATH,
                 params_filePath = PARAMS_FILE_PATH,
                 schema_filePath = SCHEMA_FILE_PATH):
        self.config = read_yaml(config_fiePath)
        self.params = read_yaml(params_filePath)
        self.schema = read_yaml(schema_filePath)

        create_directories([self.config.artifacts_root])
    def get_data_ingestion_config(self)->DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )
        return data_ingestion_config