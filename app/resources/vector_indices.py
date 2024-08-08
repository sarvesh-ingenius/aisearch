from app.models.vectors import VectorIndex
from app.resources.embedding_models import embedding_model
from flask import current_app as app
import pandas as pd 
import os 

create_index_flag = app.config['CREATE_INDEX']
table_index_path = app.config['TABLE_INDEX_PATH']

try:
    table_index = VectorIndex(embedding_model)
    few_shots_index = VectorIndex(embedding_model)
    if create_index_flag:
        dbschema = pd.read_csv('./app/model_artifacts/data/Text2SQL - Schemas.csv')
        index_column = 'Schema'
        metadata_columns = ['Team', 'Table']
        table_index.create_store(dbschema, index_column, metadata_columns)
        table_index.save_db('./app/model_artifacts/table_index')
        app.logger.info('Successfully Created Table Index From Database Schema')
        few_shots = pd.read_csv('./app/model_artifacts/data/Text2SQL - Sample Queries.csv')
        index_column = 'Question'
        metadata_columns = ['Team', 'Table', 'Query', 'Query Type']
        few_shots_index.create_store(few_shots, index_column, metadata_columns)
        few_shots_index.save_db('./app/model_artifacts/few_shot_index')
        app.logger.info('Successfully Created Few Shots Index From Query Examples')
        
        del dbschema, few_shots, index_column, metadata_columns
    else:
        table_index.load_db(app.config['TABLE_INDEX_PATH'])
        app.logger.info('Successfully Loaded Table Index')   
except Exception as e:
    app.logger.info(f"Failed To Load The Table Index")
    app.logger.info(e)