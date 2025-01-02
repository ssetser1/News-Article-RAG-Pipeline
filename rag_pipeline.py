import os
from pinecone import Pinecone
from openai import OpenAI
import click
import yaml

# Initialize OpenAI and Pinecone clients
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# Specify the Pinecone index name
index = pc.Index("embedded-articles")

def generate_query_embedding(query, model):
    """
    Generate an embedding vector for a given query using OpenAI's embedding model.

    Args:
        query (str): The input text query to embed.
        model (str): The name of the OpenAI embedding model to use.

    Returns:
        list: The embedding vector representing the query.
    """
    response = client.embeddings.create(
        input=query,
        model=model
    )
    return response.data[0].embedding

def query_pinecone(query_embedding, top_k):
    """
    Query the Pinecone index for similar documents based on the given embedding.

    Args:
        query_embedding (list): The embedding vector of the query.
        top_k (int): The number of top results to retrieve.

    Returns:
        dict: A dictionary containing the query results including metadata.
    """
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    return results

def generate_chatgpt_response(query, results, conversation_history):
    """
    Generate a response from ChatGPT based on the provided query and retrieved context.

    Args:
        query (str): The input user query.
        results (dict): The results retrieved from Pinecone, containing contextual information.
        conversation_history (list): A list of messages representing the chat history.

    Returns:
        tuple: The generated response as a string and the updated conversation history.
    """
    # Extract context from query results
    context = "\n".join([res["metadata"]["chunk_text"] for res in results["matches"]])
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"

    # Append user query and context to the conversation history
    conversation_history.append({"role": "user", "content": prompt})
    
    # Generate response using ChatGPT 
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=conversation_history,
        max_tokens=300,
    )

    # Extract and return the reply
    reply = response.choices[0].message.content.strip()
    conversation_history.append({"role": "assistant", "content": reply})

    return reply, conversation_history

@click.command()
@click.argument('configpath',type = click.Path(exists = True))
def main(configpath:click.Path):  
    """
    Main function to execute the RAG assistant.

    Args:
        configpath (Path): Path to the YAML configuration file containing model settings.
    """
    # Load configuration from YAML file
    with open(configpath, 'r') as f:
        config = yaml.safe_load(f)

# Extract configuration parameters
    model = config['model']
    top_k = config['top_k']

    print("Welcome to the ChatGPT RAG Assistant!")
    
    # Initialize conversation history
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."}
    ]

    # Enter interactive query loop
    while True:
        user_query = input("\nAsk a question (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            print("Goodbye!")
            break
        
        #Generate query embedding
        query_embedding = generate_query_embedding(user_query, model)
        
        #Query Pinecone
        results = query_pinecone(query_embedding, top_k)
        
        #Generate response usingChatGPT
        answer, conversation_history = generate_chatgpt_response(user_query, results, conversation_history)
        
        print("\nAnswer:", answer)

if __name__ == '__main__':
    main() 

