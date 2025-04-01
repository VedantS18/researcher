# Research Paper Assistant

An AI-powered research assistant that helps fetch, process, and analyze academic papers. Using a combination of arXiv for paper retrieval, Grobid for PDF processing, and GPT-4 for intelligent interactions, this tool streamlines the research paper reading process.

## Features

- 📚 Fetch relevant papers from arXiv based on search queries
- 📄 Process PDFs using Grobid for text extraction
- 🔍 Vector store-based retrieval for relevant context
- 💬 Interactive chat interface with GPT-4
- 🧠 Conversation memory for contextual responses

## Prerequisites

- Python 3.9+
- Java 11 (for Grobid)
- OpenAI API key
- Grobid server running locally

## Setup

1. **Install Grobid:**
   ```bash
   curl -L -O https://github.com/kermitt2/grobid/archive/0.8.1.zip
   unzip 0.8.1.zip
   cd grobid-0.8.1
   ./gradlew clean install
   ./gradlew run
   ```

2. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Configure environment variables in .env file:**
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   export GROBID_SERVER_URL="http://localhost:8070"
   ```

## Usage
1. **Start the application:**
   ```bash
   python main.py
   ```
2. **Enter a research topic** when prompted
3. **Chat with the assistant** to get information about the papers
4. **Type 'quit'** to exit the application

## Project Structure

- `fetch_papers.py`: Handles paper retrieval and processing
- `rag.py`: Implements the research assistant using LangChain
- `main.py`: Entry point for the application
- `requirements.txt`: List of dependencies
- `papers/`: Directory for downloaded papers
- `chroma_db/`: Chroma vector store for paper embeddings

## How it works

1. **Paper Fetching**: Uses arXiv API to find relevant papers
2. **Processing**: Converts PDFs to text chunks using Grobid
3. **Storage**: Stores processed text in a vector database
4. **Retrieval**: Uses similarity search to find relevant content
5. **Interaction**: Provides conversational interface using GPT-4

## Future Improvements

- Add support for more file formats
- Implement caching for faster responses
- Add error handling and user feedback
- Enhance the chat interface with better UX
- Add support for more complex queries/interactions