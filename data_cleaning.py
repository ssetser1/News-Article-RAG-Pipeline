import pandas as pd
import re
import yaml
import click

def clean_text(text, url_pattern, unwanted_phrases):
    """
    Cleans the input text by removing URLs and unwanted phrases.

    Args:
        text (str): The input text to be cleaned.
        url_pattern (str): Regular expression pattern to match URLs.
        unwanted_phrases (list): List of phrases to remove from the text.

    Returns:
        str: The cleaned text after applying transformations.
    """
    # Remove URLs based on the provided pattern
    text = re.sub(url_pattern, '', text)

    # Remove unwanted phrases from the text
    pattern = r'(' + '|'.join(unwanted_phrases) + r').*'
    text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    return text

@click.command()
@click.argument('configpath',type = click.Path(exists = True))
def main(configpath:click.Path): 
    """
    Main function to clean and preprocess article text data.

    Args:
        configpath (Path): Path to the YAML configuration file containing patterns and phrases.

    Returns:
        None
    """ 
    # Load configuration from the YAML file
    with open(configpath, 'r') as f:
        config = yaml.safe_load(f)

    # Extract patterns and unwanted phrases from configuration
    url_pattern = config['url_pattern']
    unwanted_phrases = config['unwanted_phrases']
    
    # Read article data and filter invalid entries
    df = pd.read_csv(r'C:\Users\juju\Documents\Programming Work\RAG Project\final_articles.tsv', sep='\t')
    df_filtered = df[~df['text'].str.contains("Javascript is required for you to be able to read premium content.", case=False, na=False)]
    df_filtered = df_filtered.reset_index(drop=True)

    # Clean the text using the specified patterns and phrases
    df_filtered['cleaned_text'] = df_filtered['text'].apply(lambda text: clean_text(text, url_pattern, unwanted_phrases))

    # Save the cleaned articles to a TSV file
    df_filtered[['cleaned_text']].to_csv('cleaned_articles.tsv',sep = '\t', index = False)
 
if __name__ == '__main__':
    main()