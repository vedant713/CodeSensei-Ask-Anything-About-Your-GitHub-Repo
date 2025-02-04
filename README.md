# GitHub Repo Chatbot 🤖

A project that allows you to chat with any GitHub repository and extract information from it using natural language. Built with **FastAPI**, **Streamlit**, **LangChain**, and **Ollama** (with DeepSeek models).



https://github.com/user-attachments/assets/f923abfe-5564-4782-a0ae-d62214aadb44



## Features ✨
- **Process any GitHub repository**: Fetch and index repository content (code, markdown, Jupyter notebooks, etc.).
- **Chat with the repository**: Ask questions about the codebase and get answers powered by **DeepSeek** models.
- **Support for multiple file types**: Handles `.py`, `.md`, `.ipynb`, `.js`, `.txt`, and more.
- **Vector-based search**: Uses **FAISS** for efficient similarity search over repository content.

---

## Tech Stack 🛠️
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Embeddings**: Ollama (DeepSeek)
- **Vector Database**: FAISS
- **Language Models**: Ollama (DeepSeek)
- **GitHub API**: PyGithub

---

## Getting Started 🚀

### Prerequisites
- Python 3.9+
- [Ollama](https://ollama.ai/) installed and running locally.
- A GitHub personal access token (with `repo` scope).

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vedant713/CodeSensei-Ask-Anything-About-Your-GitHub-Repo.git
   cd CodeSensei-Ask-Anything-About-Your-GitHub-Repo
   ```

2. **Set up the backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up the frontend**:
   ```bash
   cd ../frontend
   pip install -r requirements.txt
   ```

4. **Create a `.env` file in the `backend` folder** and add your credentials:
   ```env
   GITHUB_TOKEN=your_github_token
   DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

### Running the Project

1. **Start the backend**:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Start the frontend**:
   ```bash
   cd ../frontend
   streamlit run app.py
   ```

3. **Open the Streamlit app** in your browser (usually at `http://localhost:8501`).

---

## Usage 📖

1. **Process a Repository**:
   - Enter the GitHub repository URL in the sidebar (e.g., `https://github.com/facebook/react`).
   - Click "Process Repository" to fetch and index the repository content.

2. **Chat with the Repository**:
   - Ask questions about the repository in the chat interface.
   - Example questions:
     - "How does this repo handle error logging?"
     - "What are the main dependencies?"
     - "Explain the structure of the project."

---

## Project Structure 🗂️

```
github-repo-chatbot/
├── backend/                  # FastAPI backend
│   ├── main.py               # FastAPI app
│   ├── utils.py              # Helper functions (GitHub API, text processing)
│   ├── requirements.txt      # Backend dependencies
│   └── .env                  # Environment variables
├── frontend/                 # Streamlit frontend
│   ├── app.py                # Streamlit app
│   └── requirements.txt      # Frontend dependencies
├── README.md                 # Project documentation
└── .gitignore                # Ignore files
```

---

## Customization 🛠️

### Using Different Models
- Update the `OllamaEmbeddings` and `Ollama` model names in `backend/utils.py`:
  ```python
  embeddings = OllamaEmbeddings(model="deepseek-r1")  # Replace with your preferred model
  llm = Ollama(model="deepseek-r1")                  # Replace with your preferred model
  ```

### Adding Support for More File Types
- Update the `is_text_file` function in `backend/utils.py` to include additional file extensions.

---

## Contributing 🤝

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments 🙏
- [Ollama](https://ollama.ai/) for providing the DeepSeek models.
- [LangChain](https://www.langchain.com/) for the retrieval-augmented generation framework.
- [Streamlit](https://streamlit.io/) for the easy-to-use frontend framework.


