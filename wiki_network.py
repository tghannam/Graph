import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import wikipedia
import networkx as nx
import warnings
import csv
from operator import itemgetter
#import wikipediaapi as wpi
import tqdm
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
#import community
from itertools import chain, groupby
from collections import Counter
import os
import re
import dateutil.parser as dparser
from pandas.io.html import read_html
import bs4
import requests
import urllib
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlretrieve 
from urllib.request import urlopen, Request
import wikidata
import pywikibot
from pathlib import Path
import pickle
from dash import Dash, html, dcc
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
#from demos import dash_reusable_components as drc


def wiki_network(seed, thread, iter, seed_df=None):
    
    from tqdm import tqdm
     
    seed_links = list(set(wikipedia.page(seed, auto_suggest=False).links))
    '''for x in seed_links:
             if thread in wikipedia.page(x, auto_suggest=True).content.lower():
                 cycle.append(x)'''
    
    cycle_temp = []
    nodes= []
    thread = thread.lower()
    
    if seed_df == None:
        
        for link in tqdm(seed_links):
            try:
                content =wikipedia.page(link, auto_suggest=True).content
                if thread not in content.lower():
                    seed_links.remove(link)
                    
            except wikipedia.exceptions.DisambiguationError as e:
                                    #leonardo_edges.append(x + '_ambiguity')
                continue
            except wikipedia.exceptions.PageError:
                continue
        pd.DataFrame(seed_links, columns=['name']).to_csv('seed_links.csv')
        cycle_ = seed_links
    else:
        cycle_ = list(pd.read_csv(seed_df)['name'])
    
    for i in tqdm(range(iter)):
         for x in tqdm(cycle_):
             try:
                   L = wikipedia.page(x, auto_suggest = True).links
                   for y in L:
                       if thread in re.findall(thread, wikipedia.page(y, auto_suggest=True).content.lower()):
                            cycle_temp.append(y)
                            if y not in nodes:
                                nodes.append(y)
                            pd.DataFrame(nodes).to_csv('cycle.csv')
                            #cycle[i] = cycle[i].drop_duplicates(keep='first')
                            #cycle[i] = cycle[i].replace(r'_ambiguity', np.NaN, regex = True)
                            #cycle[i] = cycle[i].dropna()
             except wikipedia.exceptions.DisambiguationError as e:
                                   #leonardo_edges.append(x + '_ambiguity')
                    continue
             except wikipedia.exceptions.PageError:
                    continue
         
         cycle_ = list(set(cycle_temp))
         cycle_temp=[]
         pd.DataFrame(nodes).to_csv(f'nodes_{seed}.csv')
    
    B = nodes
    A = np.zeros((len(B), len(B)))
   
    links = {}
    for x in tqdm(B):
        try:
            L = wikipedia.page(x.lower()).links
        except wikipedia.exceptions.DisambiguationError as e:
                                    #leonardo_edges.append(x + '_ambiguity')
            continue
        except wikipedia.exceptions.PageError:
            continue
        links[x] = L
        
    for x in links.keys():
            for y in links.keys():
                i = B.index(x)
                j = B.index(y)
                if x != y:
                    if y in links[x]:
                        A[j][i] = 1
                    if x in links[y]:
                        A[i][j] = 1
    pd.DataFrame(A).to_csv('edges_matrix.csv')
    
    G = nx.from_numpy_array(A, create_using=nx.DiGraph())
    
    nx.relabel_nodes(G, dict(enumerate(B)), copy = False)
    adj = nx.to_pandas_adjacency(G)
    nx.write_graphml(G, f'{seed}_Wiki_1.graphml', )
    return G
     
