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

### Query 1: "Could you tell me about the current conflict between Russia and Ukraine?"
**ChatGPT (without RAG):**
> The conflict between Russia and Ukraine has been ongoing since 2014, when Russia annexed Crimea, a region of Ukraine. This led to a broader conflict in eastern Ukraine, where Russian-backed separatists have been fighting against Ukrainian government forces. The conflict has resulted in thousands of deaths and has caused a humanitarian crisis in the region.

> Efforts to resolve the conflict have been made through diplomatic means, including the Minsk agreements, which were signed in 2014 and 2015. However, the agreements have not been fully implemented, and fighting continues sporadically in eastern Ukraine.

> The international community has condemned Russia's actions in Ukraine and has imposed sanctions on Russia in response. The conflict remains a significant geopolitical issue, with implications for regional stability and international relations.

**RAG Assistant (with Context):**
> The Russia-Ukraine conflict began with Russia's annexation of Crimea in 2014 and escalated significantly on February 24, 2022, with Russia attacking all parts of Ukraine. The conflict has become the largest in Europe since World War II, resulting in hundreds of thousands of military casualties and tens of thousands of Ukrainian civilian casualties. The United States has been providing military support and financial aid to Ukraine, which has further escalated tensions. The roots of the conflict can be traced back to the Cold War era and the US's efforts to influence former Soviet republics towards Westernization, leading to geopolitical confrontation between the US and Russia. The conflict has been ongoing, with both sides engaging in military actions and facing international condemnation for the violence and casualties inflicted.

---

### Query 2: "What are the latest developments in AI regulation worldwide?"
**ChatGPT (without RAG):**
> As of now, AI regulation is still evolving and varies significantly from country to country. However, some recent developments in AI regulation worldwide include:

>1. The European Union released its proposal for the AI Act in April 2021, aiming to regulate AI systems considered high-risk. The Act includes requirements for transparency, accountability, and data governance.

>2. The United States has introduced various bills and initiatives related to AI regulation, including the Algorithmic Accountability Act and the National AI Initiative Act.

>3. Countries like Canada and Australia have also taken steps to develop guidelines and frameworks for the ethical use of AI.

>4. Organizations such as the OECD and the World Economic Forum have been actively working on developing international standards and guidelines for AI regulation.

>It is important to note that AI regulation is a complex and rapidly evolving field, and new developments are expected to continue in the coming years.

**RAG Assistant (with Context):**
> The latest developments in AI regulation worldwide include efforts by various countries such as the European Union, China, India, and the United States (specifically California) to enact laws and regulations to regulate AI technologies. For example, the European Union has adopted the Artificial Intelligence (AI) Act, China has implemented laws to regulate algorithms and generative AI, India is working on statutory rules to regulate AI, and California is considering SB1047, a bill that seeks to regulate advanced AI models. These efforts aim to establish comprehensive frameworks for AI governance, addressing issues related to data quality, accountability, transparency, human 
oversight, compliance mechanisms, and security assessments. The global trend is towards creating a unified regulatory environment for AI to avoid a patchwork of regulations that could pose challenges to developers and users alike.
































