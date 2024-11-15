import os
import shutil
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama import ChatOllama 
from langchain_community.document_loaders import PyMuPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_community.embeddings.fastembed import  FastEmbedEmbeddings 
from langchain_chroma import Chroma 
from langchain.prompts import PromptTemplate 
from langchain.chains import RetrievalQA 



#configurar FastAPI para que reciba la pregunta y devuelva la respues desde el fron
app=FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],     # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],     
)

#Configuracion de ollama 
llm= ChatOllama(model="llama3.2:1b")

#Defnir la ruta del archivo
file_path ="DocsPeliSoft.pdf"

#cargar el archivo pdf
loader= PyMuPDFLoader(file_path)

#cargar el contenido del pdf
data_pdf = loader.load()

#Definir el tamaño de los chunks y el overlap(superposicion de los chunk), osea separar el documento en partes
tex_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

#se divide el contenido del pdf en chunk
chunks= tex_splitter.split_documents(data_pdf)

#se define el modelo de embedding que se va a utilizar.
embed_model= FastEmbedEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#Se define el directorio dond ese va a guardar la base d edatos
persist_db="chroma_db_dir"
#nombre de la coleccion
collection_db="chroma_collection"

# Eliminar y regenerar la carpeta de la base de datos si existe
if os.path.exists(persist_db):
    shutil.rmtree(persist_db)
os.makedirs(persist_db, exist_ok=True)

#Se crea la base de datos con los chunks
vs=Chroma.from_documents(
    documents=chunks,
    embedding=embed_model,
    persist_directory=persist_db,
    collection_name=collection_db
)

#Se crea el retriever para buscar la info en la db
vectorstore= Chroma(
    embedding_function=embed_model,
    persist_directory=persist_db,
    collection_name=collection_db
)
#convertir el vectorstore en retriever
retriever= vectorstore.as_retriever(
   search_kwargs={'k': 10} #cantidad de chunks a retornar
)

#Se define el template de la pregunta 
custom_prompt_template = """
Usa la siguiente información para responder a la pregunta del usuario de manera precisa y detallada. 
Si la respuesta no se encuentra en dicha información, di "No sé la respuesta a tu pregunta" en lugar de generalidades.

Contexto: {context}
Pregunta: {question}
Solo devuelve la respuesta útil a continuación y nada más. Responde siempre en español 
Respuesta útil:
"""


#Se define el prompt template para la pregunta
prompt= PromptTemplate(
    template=custom_prompt_template,
    input_variables=['context','question']
)

#Se crea el chain de QA para realizar la búsqueda
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={'prompt': prompt}
)

#Se define el modelo de entrada
class Question(BaseModel):
    question:str

#Se define la ruta de la api para recibir preguntas
@app.post("/ask")
async def ask_question(question:Question):
    try:
        resp=qa.invoke({"query":question.question})
        return {"answer": resp['result']}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al procesar la pregunta.")



