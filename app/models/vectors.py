import os
from langchain_community.vectorstores import FAISS

class VectorIndex:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def create_store(self, data, index, metadata={}):
        if index not in data:
            print(f'Error - Index {index} not found in data')
            return
        for meta_col in metadata:
            if meta_col not in data:
                print(f'Error - Metadata {meta_col} not found in data')
                return

        chunks = data[index].tolist()
        if len(metadata)!=0:
            meta_data = data[metadata].to_dict(orient='records')
        else:
            meta_data = None

        self.vectorstore = FAISS.from_texts(
            chunks,
            embedding=self.embedding_model,
            metadatas = meta_data
        )

    def search(self, query, k=5, filter=None, fetch_k=20):
        results = self.vectorstore.similarity_search(query, k=k, filter=filter, fetch_k = fetch_k)
        # [doc] returned by similarity_search has following attributes : page_content->string, metadata->dict
        return [doc.page_content for doc in results], [doc.metadata for doc in results]

    def save_db(self, path):
        dir_name = os.path.dirname(path)
        if dir_name == "":
            dir_name = "."
        if os.path.isdir(dir_name):
            self.vectorstore.save_local(path)
            print(f'Successfully saved the db at {path}')
        else:
            print(f'Directory {dir_name} does not exist')
        
    def load_db(self, path):
        if os.path.isdir(path):
            self.vectorstore = FAISS.load_local(path, embeddings=self.embedding_model, allow_dangerous_deserialization=True)
            print(f'Successfully loaded the db from {path}')
        else:
            print(f'File not found at {path}')

    def add_vectors(self, data, index, metadata={}):
        if index not in data:
            print(f'Error - Index {index} not found in data')
            return
        for meta_col in metadata:
            if meta_col not in data:
                print(f'Error - Metadata {meta_col} not found in data')
                return

        chunks = data[index].tolist()
        if len(metadata)!=0:
            meta_data = data[metadata].to_dict(orient='records')
        else:
            meta_data = None

        self.vectorstore.add_texts(chunks, metadatas = meta_data)