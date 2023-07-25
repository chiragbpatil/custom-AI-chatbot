import requests
import xmltodict
import pickle
import faiss
import os

from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

os.environ["OPENAI_API_KEY"] = config.get('OPENAI', 'OPENAI_API_KEY')

def generate_vector_db(web_page_urls,vector_db_path="data/faiss_store_openai.pkl"):

    loaders = UnstructuredURLLoader(urls=web_page_urls)
    data = loaders.load()

    text_splitter = CharacterTextSplitter(separator='\n')
    docs = text_splitter.split_documents(data)

    text_splitter = CharacterTextSplitter(separator='\n',
                                        chunk_size=1000,
                                        chunk_overlap=200)

    docs = text_splitter.split_documents(data)

    embeddings = OpenAIEmbeddings()


    vectorStore_openAI = FAISS.from_documents(docs, embeddings)

    with open(vector_db_path, "wb") as f:
        pickle.dump(vectorStore_openAI, f)


web_page_urls = ["https://en.wikipedia.org/wiki/India#:~:text=India%20has%20been%20a%20federal,almost%201.4%20billion%20in%202022."]
if __name__ == "__main__":
    generate_vector_db(web_page_urls)