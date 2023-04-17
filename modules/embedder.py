import os
import pickle
import tempfile
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings


class Embedder:
    def __init__(self):
        pass

    async def storeDocEmbeds(self, file, filename):
        """
        Stores document embeddings using Langchain and FAISS
        """
        # Write the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
            tmp_file.write(file)
            tmp_file_path = tmp_file.name

        # Load the data from the file using Langchain
        loader = PyPDFLoader(file_path=tmp_file_path)
        data = loader.load_and_split()

        # Create an embeddings object using Langchain
        embeddings = OpenAIEmbeddings()

        # Store the embeddings vectors using FAISS
        vectors = FAISS.from_documents(data, embeddings)
        os.remove(tmp_file_path)

        # Save the vectors to a pickle file
        with open(filename + ".pkl", "wb") as f:
            pickle.dump(vectors, f)

    async def getDocEmbeds(self, file, filename):
        """
        Retrieves document embeddings
        """
        # Check if embeddings vectors have already been stored in a pickle file
        if not os.path.isfile(filename + ".pkl"):
            # If not, store the vectors using the storeDocEmbeds function
            await self.storeDocEmbeds(file, filename)

        # Load the vectors from the pickle file
        with open(filename + ".pkl", "rb") as f:
            global vectors
            vectors = pickle.load(f)

        return vectors
