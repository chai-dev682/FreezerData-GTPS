#  AI-Driven GTPS (Generative Technical Problem Solvers) for Technical

A Streamlit-based chatbot application powered by OpenAI that helps users analyze and understand freezing and cooling systems. The application combines vector similarity search and SQL querying capabilities to set up an interactive troubleshooting dialogue with a technician.

## Features

- 📊 CSV file upload and processing
- 💬 Interactive chat interface
- 🔍 Hybrid search (SQL + Vector) for FreezerData
- 🤖 AI-powered natural language understanding
- 📋 Comprehensive data management

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Databases**:
  - MySQL (Structured data storage)
  - Pinecone (Vector database for semantic search)
- **AI/ML**:
  - OpenAI GPT-4
  - LangChain
  - LangGraph

## Prerequisites

- Python 3.8+
- MySQL Server (We used [Aiven sql database](https://aiven.io/) for this project)
- Pinecone Account
- OpenAI API Key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/chai-dev682/FreezerData-GTPS.git
cd FreezerData-GTPS
```

2. Create a virtual environment:
```bash
python -m virtualenv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables with your own API keys:
```bash
cp .env.example .env
```


## Project Structure

```README.MD
├── dataset/                      # Dataset(pdf, csv) for sql and vector database
├── app/
│   ├── core/
│   │   ├── config.py             # Application configuration
│   │   ├── logging.py            # Logging setup
│   │   ├── prompt_templates/     # LLM prompt templates
│   │   └── function_templates/   # LLM function templates
│   ├── db/
│   │   ├── mysql.py              # MySQL database service
│   │   └── vectordb.py           # Pinecone vector database service
│   ├── schemas/
│   │   └── freezer_data.py       # Data models
│   ├── services/
│   │   ├── chat.py               # Chat service
│   │   └── graph/                # LangGraph workflow
│   ├── utils/
│   │   └── pdf_tools.py          # PDF processing utilities
├── scripts/
│   ├── process_pdf.py        # Process pdf files to embed and store in vector database
│   └── process_csv.py        # Process csv files to store in mysql database
├── main.py                       # Application entry point
├── requirements.txt              # Project dependencies
├── .env                          # Environment variables
└── README.md                     # README file
```

## Usage

Start the application:
```bash
streamlit run main.py
```