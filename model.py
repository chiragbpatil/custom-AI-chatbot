import os
import pickle
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

os.environ["OPENAI_API_KEY"] = config.get('OPENAI', 'OPENAI_API_KEY')

vector_store_path = os.path.join('data', 'faiss_store_openai.pkl')
with open(vector_store_path, "rb") as f:
    VectorStore = pickle.load(f)

chain = ConversationalRetrievalChain.from_llm(llm=ChatOpenAI(
    temperature=0.0, model_name='gpt-3.5-turbo'), retriever=VectorStore.as_retriever())


def get_response(query):
    result = chain({"question": query, "chat_history": {}})
    return result


get_response("hello")
