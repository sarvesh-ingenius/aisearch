# from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from flask import current_app as app

try:
    embedding_model = HuggingFaceEmbeddings(
        # model_name='all-MiniLM-L6-v2',
        model_name = app.config['EMBEDDING_MODEL'],
        model_kwargs={
            # "device": "cuda"
            "trust_remote_code":"True",
        },
        # encode_kwargs={"device": "cuda", "batch_size": 100}
    )
    app.logger.info(f"Successfully Loaded The Embedding Model : {app.config['EMBEDDING_MODEL']}")
except Exception as e:
    app.logger.info(f"Failed To Load The Embedding Model : {app.config['EMBEDDING_MODEL']}")
    app.logger.info(e)