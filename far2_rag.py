import logging
import sys
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import torch
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt


class RAGImplementation:
    def __init__(self, file_dir, model_path="./model/mistral-7b-instruct-v0.1.Q2_K.gguf", 
                embed_model_name="thenlper/gte-large", temperature=0.1, max_new_tokens=256, context_window=3900,
                generate_kwargs={}, model_kwargs={"n_gpu_layers": 40}, verbose=False):
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

        self.embed_model = HuggingFaceEmbeddings(model_name=embed_model_name)
        self.llm = LlamaCPP(
            model_path=model_path,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            context_window=context_window,
            generate_kwargs=generate_kwargs,
            model_kwargs=model_kwargs,
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=verbose
        )

        self.service_context = ServiceContext.from_defaults(
            chunk_size=256,
            llm=self.llm,
            embed_model=self.embed_model
        )

        self.index = None
        self.query_engine = None
        self.file_dir = file_dir

    def create_index(self):
        documents = SimpleDirectoryReader(self.file_dir).load_data()
        self.index = VectorStoreIndex.from_documents(documents, service_context=self.service_context)
        self.query_engine = self.index.as_query_engine()

    def query(self, prompt):
        if self.query_engine is None:
            self.create_index()
        response = self.query_engine.query(prompt)
        return response


"""query_engine = RAGImplementation(file_dir="./file")
prompt = "Please provide 5 points from the extracted privacy policy, each framed as 'this website,' strictly not as 'I' or 'We,' with precisely 30 words each, discussing data collection, and ensure it's not your own privacy policy."
response = query_engine.query(prompt)
print(response)"""
