
import sys
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

load_dotenv()

def load_pdfs(pdf_dir):
    text = ""
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            reader = PdfReader(os.path.join(pdf_dir, pdf_file))
            for page in reader.pages:
                text += page.extract_text()
    return text

pdf_dir = "./pdfs/"
raw_text = load_pdfs(pdf_dir)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_text(raw_text)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(texts, embeddings)
chat_model = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=chat_model,
    retriever=vectorstore.as_retriever()
)

chat_history = []

def ask_question(question):
    global chat_history
    result = qa_chain.invoke({"question": question, "chat_history": chat_history})
    chat_history.append((question, result["answer"]))
    return result["answer"]

if __name__ == "__main__":
    question = sys.argv[1]
    print(ask_question(question))
