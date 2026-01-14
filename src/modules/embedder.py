import os
import tempfile
from langchain_community.document_loaders import CSVLoader, PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Embedder:

    def __init__(self):
        self.PATH = "embeddings"
        self.createEmbeddingsDir()

    def createEmbeddingsDir(self):
        """
        Creates a directory to store the embeddings vectors
        """
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)

    def storeDocEmbeds(self, file, original_filename):
        """
        Stores document embeddings using Langchain and FAISS native save
        """
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
            tmp_file.write(file)
            tmp_file_path = tmp_file.name
            
        def get_file_extension(uploaded_file):
            file_extension = os.path.splitext(uploaded_file)[1].lower()
            return file_extension
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=100,
            length_function=len,
        )
        
        file_extension = get_file_extension(original_filename)

        try:
            if file_extension == ".csv":
                loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={
                    'delimiter': ',',
                })
                data = loader.load()

            elif file_extension == ".pdf":
                loader = PyPDFLoader(file_path=tmp_file_path)  
                data = loader.load_and_split(text_splitter)
            
            elif file_extension == ".txt":
                loader = TextLoader(file_path=tmp_file_path, encoding="utf-8")
                data = loader.load_and_split(text_splitter)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
                
            embeddings = OpenAIEmbeddings()
            vectors = FAISS.from_documents(data, embeddings)
            
            # Use FAISS native save_local method instead of pickle
            save_path = f"{self.PATH}/{original_filename}"
            vectors.save_local(save_path)
                
        finally:
            # Clean up temp file
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def getDocEmbeds(self, file, original_filename):
        """
        Retrieves document embeddings using FAISS native load
        """
        save_path = f"{self.PATH}/{original_filename}"
        index_file = f"{save_path}/index.faiss"
        
        # Check if FAISS index exists
        needs_regeneration = not os.path.exists(index_file)
        
        if needs_regeneration:
            self.storeDocEmbeds(file, original_filename)

        # Load using FAISS native load_local
        embeddings = OpenAIEmbeddings()
        vectors = FAISS.load_local(
            save_path, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        
        return vectors
