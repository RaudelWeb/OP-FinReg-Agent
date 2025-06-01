# FinReg ESG Agent

### Keksitty liiketoimintatarve

Sääntelyvaatimusten määrä ja monimutkaisuus kasvaa hurjasti. 
FinReg ESG-Agentti on tehty tehostamaan ESG-raporttien analysointia.

Pohja-aineistona RAG-agentti voi käyttää esimerkiksi `/downloads/`-kansiossa löytyviä
Finanssivalvonnan ja EBA:n aineistoja.


## Agentin prosessikaavio

![Prosessikaavio](https://github.com/RaudelWeb/FIVA_FinReg_Copilot/blob/main/images/prosessikaavio.png?raw=true)

## Asentaminen

Vaatimukset:
- Python 3.9+ asennettuna
- `git` paikallisesti
- Pääsy ympäristömuuttujiin (esim. `.env`-tiedosto tai vastaava)
- Azure-palvelut:
    - Azure Search Service (2 indeksiä: 1 indeksi määräyksille- ja ohjeille ja 1 indeksi raporteille)
    - Azure Blob Storage
    - Azure OpenAI deploymentit
        - o3-mini
        - text-embedding-ada-002

1. Asenna tarvittavat paketit
`pip install -r requirements.txt`
2. Luo .env tiedosto, jossa on seuraavat muuttujat:
    ```
    AZURE_OPENAI_ENDPOINT=https://<sinun‐openai‐endpoint>.openai.azure.com/
    AZURE_OPENAI_KEY=<avaimesi>
    AZURE_OPENAI_API_VERSION=2024-12-01-preview

    SEARCH_ENDPOINT=https://<sinun‐search‐palvelu>.search.windows.net
    SEARCH_KEY=<search‐avain>
    SEARCH_IDX_NAME=<indeksin_nimi>
    REGULATION_SEARCH_IDX_NAME=finreg-rag
    REPORT_SEARCH_IDX_NAME=reports
    REPORT_INDEXER_NAME=reports-indexer
    
    EMBED_DEPLOY=text-embedding-ada-002
    CHAT_DEPLOY=gpt-4o
    
    AZURE_STORAGE_CONN=<blob‐connection‐string>
    BLOB_STORAGE_NAME=finregtstor
   ```



