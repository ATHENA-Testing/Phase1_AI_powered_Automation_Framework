from ollama import chat
# Define a system prompt

def read_file_to_string(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return None
    except Exception as e:
         print(f"An error occurred: {e}")
         return None

file_path = R'C:\local-LLM-with-RAG-main\Test_Documents\Amazon_Site.txt'
output_file_path = R'C:\local-LLM-with-RAG-main\Test_Steps\Result.txt'

file_string = read_file_to_string(file_path)
taststr= file_string

# system_prompt = "Act as an Browser Agent generate test steps "
# # Chat with a system prompt  qwen2.5:7b
# response = chat('llama3.1:8b',
#     messages=[
#         {'role': 'system', 'content': system_prompt},
#         {'role': 'user', 'content': taststr}
#     ])

# temp = response.message.content 

# print(temp)
# with open(output_file_path, "a") as file:
#         file.write(temp)

# lines = temp.split('\n')
# for line in lines:
#     if line[:1].isdigit():
#         #print (line[:1])
#         with open(output_file_path, "a") as file:
#             file.write(line + '\n')


#from langchain_community.chat_models.ollama import ChatOllama
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

# Path to persisted ChromaDB directory
persist_directory = "C:/local-LLM-with-RAG-main/storage"  #chroma.sqlite3  Update to your DB path
EMBED_MODEL = "nomic-embed-text"  # Example; replace with your actual model
LLM_MODEL = "llama3"   
# Initialize Ollama Embeddings (must match embeddings used when building vector DB)
embeddings = OllamaEmbeddings(model=EMBED_MODEL)  # Or whatever model you used
# Load the existing vector database
vector_db = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings,
)
# Initialize the ChatOllama LLM
llm = ChatOllama(model=LLM_MODEL)  # You can use llama3, mistral, etc., if available
# Set up RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_db.as_retriever(),
)
query =  taststr 
response = qa_chain({"query": query})

print(response["result"])
with open(output_file_path, "a") as file:
        file.write(response["result"])
