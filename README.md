# RAG-Article-Processing-Pipeline

## Overview
This project implements a Retrieval-Augmented Generation (RAG) pipeline for collecting, cleaning, embedding, and retrieving articles. It uses OpenAI, Pinecone, and NewsData.io APIs to preprocess text, generate embeddings, and enable semantic search.

---

## Setup Instructions

### Environment Variables
Before running the code, set up the following environment variables:


**OpenAI API Key**
   - Create an account at [OpenAI](https://platform.openai.com/) and generate an API key.
   - Set the key in your environment:
     ```bash
     export OPENAI_API_KEY=your_openai_api_key
     ```

**Pinecone API Key**
   - Create an account at [Pinecone](https://www.pinecone.io/) and set up an index.
   - Set the key in your environment:
     ```bash
     export PINECONE_API_KEY=your_pinecone_api_key
     ```

---

### Pinecone Index Setup
Create a Pinecone index for storing embeddings:
1. Log in to the Pinecone dashboard.
2. Create an index with the following settings:
   - **Name:** `embedded-articles`
   - **Dimension:** `1536`
   - **Metric:** `cosine`
   - **Cloud Provider:** `AWS`
   - **Region:** `us-east-1`

Alternatively, you can create the index programmatically using:
```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
pc.create_index(
    name="embedded-articles",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(cloud='aws', region='us-east-1')
)
```

---

## Running the Code

Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

Run the scripts in order:

**Note:** Running data_collection is not required as the articles are already provided in the dataset and access to the API is not free.

   - Collect raw articles from NewsData.io.
     ```bash
     python data_collection.py config.yaml
     ```

   - Clean and preprocess the collected articles.
     ```bash
     python data_cleaning.py config.yaml
     ```

   - Generate embeddings and store them in Pinecone for retrieval.
     ```bash
     python embedding_and_retrieval.py config.yaml
     ```

   - Run the RAG assistant to query and retrieve information.
     ```bash
     python rag_pipeline.py config.yaml
     ```

---



## Dataset
The datasets are hosted externally due to size limitations.

### Download Links:
- [Final Articles Dataset (TSV)](https://drive.google.com/your-link-here)


---
## Example Queries

### Query 1: "Could you tell me about the Russia and Ukraine Conflict?"
**ChatGPT (without RAG):**
> The Russia-Ukraine conflict began in earnest in 2014 when Russia annexed Crimea, a move widely condemned by the international community as illegal. This was followed by fighting in Eastern Ukraine, particularly in the Donetsk and Luhansk regions, where separatist movements, backed by Russia, clashed with Ukrainian forces.

> Tensions escalated dramatically in February 2022 when Russia launched a full-scale invasion of Ukraine. This invasion has led to widespread destruction, significant loss of life, and a major humanitarian crisis. The conflict has drawn international condemnation of Russia's actions and resulted in a range of sanctions against Russia by Western countries and their allies. It has also led to significant geopolitical shifts, with NATO and European countries reassessing their defense strategies and Ukraine seeking closer ties with the West, including applying for membership in the European Union and NATO.

> The situation remains volatile, with ongoing military engagements and complex diplomatic negotiations. The conflict has far-reaching implications for global security, energy markets, and international law.

**RAG Assistant (with Context):**
> The Russia-Ukraine conflict began with Russia's annexation of Crimea in 2014 and escalated significantly on February 24, 2022, with Russia attacking all parts of Ukraine. The conflict has become the largest in Europe since World War II, resulting in hundreds of thousands of military casualties and tens of thousands of Ukrainian civilian casualties. The United States has been providing military support and financial aid to Ukraine, which has further escalated tensions. The roots of the conflict can be traced back to the Cold War era and the US's efforts to influence former Soviet republics towards Westernization, leading to geopolitical confrontation between the US and Russia. The conflict has been ongoing, with both sides engaging in military actions and facing international condemnation for the violence and casualties inflicted.

---
































