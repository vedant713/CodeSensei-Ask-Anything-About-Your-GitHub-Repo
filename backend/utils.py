from github import Github
import logging
from github import Github, UnknownObjectException
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
import os
import json
from dotenv import load_dotenv

load_dotenv()

def parse_github_url(url):
    parts = url.strip("/").split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL")
    return parts[-2], parts[-1]

def is_text_file(filename):
    text_extensions = [".py", ".md", ".txt", ".js", ".java", ".html", ".css", ".ipynb"]
    return any(filename.endswith(ext) for ext in text_extensions)

def parse_ipynb(file_content):
    """
    Parse a Jupyter Notebook file and extract text from code and markdown cells.
    """
    try:
        notebook = json.loads(file_content)
        text = ""
        for cell in notebook.get("cells", []):
            if cell["cell_type"] in ["code", "markdown"]:
                text += "".join(cell["source"]) + "\n"
        return text
    except Exception as e:
        logging.error(f"Failed to parse .ipynb file: {e}")
        return ""

def process_repo(github_url):
    try:
        # Parse URL
        owner, repo = parse_github_url(github_url)
        logging.info(f"Processing repository: {owner}/{repo}")

        # Fetch files via GitHub API
        g = Github(os.getenv("GITHUB_TOKEN"))
        repo = g.get_repo(f"{owner}/{repo}")
        files = []

        def fetch_contents(contents):
            for content in contents:
                if content.type == "file" and is_text_file(content.name):
                    try:
                        if content.name.endswith(".ipynb"):
                            # Parse .ipynb files
                            notebook_text = parse_ipynb(content.decoded_content.decode())
                            if notebook_text:
                                files.append(notebook_text)
                                logging.info(f"Added .ipynb file: {content.path}")
                        else:
                            # Handle other text files
                            files.append(content.decoded_content.decode())
                            logging.info(f"Added file: {content.path}")
                    except Exception as e:
                        logging.error(f"Failed to decode {content.path}: {e}")
                elif content.type == "dir":
                    try:
                        fetch_contents(repo.get_contents(content.path))
                    except UnknownObjectException:
                        logging.warning(f"Directory not found: {content.path}")

        fetch_contents(repo.get_contents(""))
        logging.info(f"Total files processed: {len(files)}")

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.create_documents(files)

        # Create vector DB
        embeddings = OllamaEmbeddings(model="deepseek-r1")
        vector_db = FAISS.from_documents(chunks, embeddings)
        return vector_db

    except Exception as e:
        logging.error(f"Error processing repository: {e}")
        raise

def answer_question(vector_db, question):
    llm = Ollama(model="deepseek-r1")
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever()
    )
    return qa.run(question)