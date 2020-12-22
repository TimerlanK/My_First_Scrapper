import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import io

def request_github_trending(url):
    page = requests.get(url)
    page.status_code
    # print(page.content)
    # print("-"*100)
    # print(page.text)
    return page.text

def extract(page_text):
    soup = BeautifulSoup(page_text, features="html.parser") 
    return soup

def transform(html_repos):
    
    REPOS_NAME = []
    NAME = []
    NBR_STARS = []
    COD_LANG = []
    
    developer = html_repos.findAll('h1', attrs = {'class' : 'h3 lh-condensed'})
    for span in developer: 
        span = span.text.replace('\n','').replace(' ','') 
        if "/" in span:
            value = (span.split("/"))[0]
            NAME.append(value)


    repos_name = html_repos.findAll('h1', attrs = {'class' : 'h3 lh-condensed'}) # or span by class name
    for span in developer: 
        span = span.text.replace('\n','').replace(' ','')
        if "/" in span:
            span, value = span.split("/",-1)
            REPOS_NAME.append(value)
    
        
    nbr_star = html_repos.findAll('a', attrs = {'class' : 'muted-link d-inline-block mr-3'}) 
    for span in nbr_star:
        NBR_STARS.append(span.text.replace('\n','').replace(' ','').replace(',',''))
    NBR_STARS= NBR_STARS[::2] 
    
    code = html_repos.findAll('span', attrs = {'class' : 'd-inline-block ml-0 mr-3'}) 
    for span in code:
        COD_LANG.append(span.text.replace('\n','').replace(' ',''))
        
    final_dic = [{'developer': NAME, 'repository_name': REPOS_NAME, 'nbr_stars': NBR_STARS, 'code_lang':COD_LANG}]

    # print(len(REPOS_NAME))
    # print(len(NAME))
    # print(len(NBR_STARS))
    # print(len(COD_LANG))
    # print(NBR_STARS)
    
    return final_dic

def format(repositories_data):
    col_names = ['Developer', 'Repository Name', 'Number of Stars', 'Coding Language']    
    df = pd.DataFrame(repositories_data[0]) 
    df_res = df.rename(columns = {'developer': 'Developer', 'repository_name': 'Repository Name', 'nbr_stars': 'Number of Stars', 'code_lang':'Coding Language'}, inplace = False)
    # print(df_res.head())
    
    csv_string = df_res.to_csv(index = False)
    return csv_string

url ="https://github.com/trending"
page_text = request_github_trending(url)
html_repos = extract(page_text)
repositories_data = transform(html_repos)
# print(repositories_data)
result_csv = format(repositories_data)
print(result_csv)
