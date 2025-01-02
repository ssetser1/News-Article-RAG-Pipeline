import os
from newsdataapi import NewsDataApiClient
import pandas as pd
import yaml
import click

# Initialize NewsData API client
news_key = os.environ.get('NEWS_IO_KEY')
api = NewsDataApiClient(apikey=news_key)

# Temporary storage for articles
articles_temp = []

def keyword_search(keyword, start_date, end_date):
    """
    Searches for articles containing a specific keyword within a given date range.

    Args:
        keyword (str): The keyword to search for.
        start_date (str): The start date for the search in 'YYYY-MM-DD' format.
        end_date (str): The end date for the search in 'YYYY-MM-DD' format.

    Returns:
        None
    """
    res = api.archive_api(q=keyword,from_date=start_date,to_date=end_date,max_result=5000,scroll=True, language = 'en', full_content=True)
    
    for i in range(len(res['results'])):
        articles_temp.append(res['results'][i]['title'])
        
    return

def category_search(cat, start_date, end_date):
    """
    Searches for articles within a specific category and date range.

    Args:
        cat (str): The category to search within.
        start_date (str): The start date for the search in 'YYYY-MM-DD' format.
        end_date (str): The end date for the search in 'YYYY-MM-DD' format.

    Returns:
        None
    """
    res = api.archive_api(category = cat,from_date= start_date,to_date=end_date,max_result=5000,scroll=True, language = 'en', full_content=True)
    
    for i in range(len(res['results'])):
        articles_temp.append(res['results'][i]['title'])

    return

def get_articles(keywords, categories, start_date, end_date):
    """
    Retrieves articles based on keywords and categories within a specified date range.

    Args:
        keywords (list): List of keywords for searching articles.
        categories (list): List of categories for searching articles.
        start_date (str): Start date for the search in 'YYYY-MM-DD' format.
        end_date (str): End date for the search in 'YYYY-MM-DD' format.

    Returns:
        None
    """
    for i in range(len(keywords)):
        keyword_search(keywords[i], start_date, end_date)

    for i in range(len(categories)):
        category_search(categories[i], start_date, end_date)
    
    return

@click.command()
@click.argument('configpath',type = click.Path(exists = True))
def main(configpath:click.Path):
    """
    Main function to fetch and save articles based on configuration settings.

    Args:
        configpath (Path): Path to the YAML configuration file.

    Returns:
        None
    """
    # Load configuration from the YAML file
    with open(configpath, 'r') as f:
        config = yaml.safe_load(f)

    # Extract configuration values
    keywords = config['keywords']    
    categories = config['categories']
    start_date = config['start_date']
    end_date = config['end_date']

    # Fetch articles based on configuration
    get_articles(keywords, categories, start_date, end_date)

    # Save the articles to a TSV file
    df = pd.DataFrame(articles_temp, columns = ['text']).drop_duplicates(subset=['text'])
    df.to_csv('final_articles.tsv',sep = '\t', index = False)

if __name__ == '__main__':
    main()