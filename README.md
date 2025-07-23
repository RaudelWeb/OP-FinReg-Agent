# OP FinReg Agent

### Presentation video (partially in Finnish)

[https://supercut.ai/share/lopez/RLRQp_II-X-yR4HNWBYtkl](https://supercut.ai/share/lopez/RLRQp_II-X-yR4HNWBYtkl)

[Watch presentation on YouTube](https://www.youtube.com/watch?v=B1JneUuknDk)

### Fictional Business Need

The volume and complexity of regulatory requirements are growing rapidly.  
The FinReg ESG Agent is designed to streamline the analysis of ESG reports.

As its base data source in a RAG setup, the agent can use the Finanssivalvonta and EBA documents found in the `/downloads/` folder.

## Agent Process Flow (in finnish to facilitate business context)

![Process Flow Diagram](https://github.com/RaudelWeb/FIVA_FinReg_Copilot/blob/main/images/prosessikaavio.png?raw=true)

## Installation

### Prerequisites
- Python 3.9 or higher installed  
- `git` available locally  
- Access to environment variables (e.g. via a `.env` file)  
- Azure resources:
  - Azure AI Search Service (2 indexes: one for regulations & guidelines, one for reports)
  - Azure Blob Storage
  - Azure OpenAI deployments:
    - `o3-mini`
    - `text-embedding-ada-002`

### Steps

1. Install required Python packages:
    
    ```bash
    pip install -r requirements.txt

2.	Create a .env file with the following variables:
   
       ```ini
        AZURE_OPENAI_ENDPOINT=https://<your-openai-endpoint>.openai.azure.com/
        AZURE_OPENAI_KEY=<your-key>
        AZURE_OPENAI_API_VERSION=2024-12-01-preview
        
        SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
        SEARCH_KEY=<your-search-key>
        SEARCH_IDX_NAME=<index_name>
        REGULATION_SEARCH_IDX_NAME=finreg-rag
        REPORT_SEARCH_IDX_NAME=reports
        REPORT_INDEXER_NAME=reports-indexer
        
        EMBED_DEPLOY=text-embedding-ada-002
        CHAT_DEPLOY=o3-mini
        
        AZURE_STORAGE_CONN=<your-blob-connection-string>
        BLOB_STORAGE_NAME=finregtstor
