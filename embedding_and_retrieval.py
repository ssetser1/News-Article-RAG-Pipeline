import os
import numpy as np
import pandas as pd
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
import click
import yaml

# Initialize API clients for OpenAI and Pinecone
openai_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=openai_key)
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

def chunk_text(articles, size, overlap):
    """
    Splits article texts into smaller chunks with overlaps for processing.

    Args:
        articles (pd.DataFrame): DataFrame containing articles with a 'cleaned_text' column.
        size (int): Size of each text chunk.
        overlap (int): Overlap between consecutive chunks.

    Returns:
        list: A list of dictionaries containing chunked text data.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    articles['text_id'] = articles.index
    all_chunks = []

    for _, row in articles.iterrows():
        article_id = row['text_id']
        article_text = row['cleaned_text']
        
        # Split the article text into chunks
        chunks = text_splitter.split_text(article_text)
        
        # Create chunk data for each split chunk
        chunk_data = [
            {
                'article_id': article_id,
                'chunk_index': chunk_index,
                'chunk_text': chunk
            }
            for chunk_index, chunk in enumerate(chunks)
        ]
        
        # Extend all_chunks with this article's chunk data
        all_chunks.extend(chunk_data)
    
    return all_chunks

def get_embedding(text, model="text-embedding-3-small"):
    """
    Generates embeddings for input text using OpenAI's embedding model.

    Args:
        text (list): List of input texts to embed.
        model (str): The OpenAI model to use for embedding generation.

    Returns:
        np.ndarray: An array of embeddings for the input text.
    """
    res = client.embeddings.create(input=text, model=model)
    return  np.array([res.data[i].embedding for i in range(len(text))])

def generate_embeddings(chunked_df, model="text-embedding-3-small", batch_size=750):
    """
    Generates embeddings for all text chunks in batches.

    Args:
        chunked_df (pd.DataFrame): DataFrame containing text chunks.
        model (str): The OpenAI model to use for embedding generation.
        batch_size (int): Number of chunks to process in each batch.

    Returns:
        list: List of embedding vectors for all chunks.
    """
    num_batches = int(np.ceil(len(chunked_df['chunk_text']) / batch_size))
    emb_list = []
    
    for i in range(num_batches):
        batch_texts = chunked_df['chunk_text'][i * batch_size : (i + 1) * batch_size].tolist()
        embeddings = get_embedding(batch_texts, model=model)
        emb_list.extend(embeddings)
    
    return emb_list

def upsert_to_pinecone(chunked_df, index):
    """
    Uploads embeddings and metadata to a Pinecone index.

    Args:
        chunked_df (pd.DataFrame): DataFrame containing chunks and embeddings.
        index (pinecone.Index): Pinecone index to upload the data.

    Returns:
        None
    """
    vectors = []
    for _, row in chunked_df.iterrows():
        vectors.append({
            "id": f"{row['article_id']}_{row['chunk_index']}",  
            "values": row["embedding"],  
            "metadata": {
                "article_id": row["article_id"],
                "chunk_index": row["chunk_index"],
                "chunk_text": row["chunk_text"]
            }
        })
    
    batch_size = 100  
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)

@click.command()
@click.argument('configpath',type = click.Path(exists = True))
def main(configpath:click.Path):  
    """
    Main function to process articles and upload embeddings to Pinecone.

    Args:
        configpath (Path): Path to the configuration YAML file.

    Returns:
        None
    """
    # Load configuration from YAML file
    with open(configpath, 'r') as f:
        config = yaml.safe_load(f)

    size = config['size']
    overlap = config['overlap']
    
    # Define Pinecone index name
    index_name = "embedded-articles"

    # Create index if it doesn't exist
    if index_name not in pc.list_indexes():
        pc.create_index(
            name=index_name,
            dimension=1536,  
            metric="cosine",
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )

    index = pc.Index(index_name)

    # Load and process articles
    articles = pd.read_csv(r'C:\Users\juju\Documents\Programming Work\RAG Project\cleaned_articles.tsv', sep='\t')
    
    # Chunk text, generate embeddings, and upload to Pinecone
    chunked_df = pd.DataFrame(chunk_text(articles, size, overlap))
    chunked_df['embedding'] = generate_embeddings(chunked_df)
    upsert_to_pinecone(chunked_df, index)
    print("Embeddings successfully uploaded to Pinecone!")
    print(index.describe_index_stats())

if __name__ == '__main__':
    main() 
    
