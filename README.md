⚠️ The pdf2chunks project is currently in early development phase and is not yet stable for production use. ⚠️

# pdf2chunks

A Python tool designed to create vectorized chunks from PDF documents for integration into a vector database (Milvus), enabling RAG (Retrieval-Augmented Generation) pipeline queries.

## Learning Project

This project serves as a learning experience in:
- Python development and best practices
- AI/ML concepts implementation
- Vector databases manipulation
- RAG pipeline architecture
- Large Language Models integration

## Overview

pdf2chunks processes PDF documents to:
1. Extract and preserve document structure
2. Create meaningful text chunks
3. Generate vector embeddings using SFR-embedding-mistral
4. Store data in Milvus vector database
5. Enable efficient retrieval for RAG applications using Mistral-7B

## Installation

### Prerequisites
- Python 3
- UV package manager
- Milvus database
- Ollama (for SFR-embedding-mistral and Mistral-7B models)

### Setup
```shell
uv venv
source .venv/bin/activate
uv sync
```

## Usage
```shell
uv run start.py
```

## Technologies

- **PDF Processing**: camelot-py, pdfplumber
- **Vector Database**: Milvus
- **AI Models**:
  - SFR-embedding-mistral (vector embeddings)
  - Mistral-7B (text generation)
- **Development Tools**: Python 3, UV package manager

## License

MIT
