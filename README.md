# Gemini RAG Document Q&A

A full-stack Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their content. The application retrieves relevant document chunks using semantic search and uses Google Gemini to generate grounded answers with source information.

## Features

- Upload PDF documents
- Extract text from PDF files
- Split documents into manageable chunks
- Generate document embeddings using Google Gemini
- Store embeddings in ChromaDB
- Perform semantic similarity search
- Retrieve the most relevant document chunks
- Filter irrelevant queries using a distance threshold
- Generate answers using Google Gemini
- Prevent answers based on outside knowledge
- Display source document, page, chunk, and similarity distance
- List uploaded documents
- Delete documents
- React frontend
- FastAPI backend
- CORS support
- Automated retrieval evaluation
- API and configuration tests
- Docker support

## Tech Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Google Gemini API
- ChromaDB
- PyMuPDF
- Pydantic

### Frontend

- React
- Vite
- Axios
- JavaScript
- CSS

### Testing

- Pytest
- Custom RAG retrieval evaluation

### Deployment

- Docker

## Architecture

```text
                         React Frontend
                              |
                              | HTTP
                              v
                       FastAPI Backend
                              |
                 +------------+------------+
                 |                         |
                 v                         v
          Document Upload              User Query
                 |                         |
                 v                         v
          PDF Text Extraction        Query Embedding
                 |                         |
                 v                         v
               Chunking              ChromaDB Search
                 |                         |
                 v                         v
         Gemini Embeddings           Top-K Retrieval
                 |                         |
                 v                         v
             ChromaDB              Distance Filtering
                                           |
                                           v
                                  Relevant Context
                                           |
                                           v
                                  Gemini Generation
                                           |
                                           v
                                  Answer + Sources
                                           |
                                           v
                                  React Frontend
