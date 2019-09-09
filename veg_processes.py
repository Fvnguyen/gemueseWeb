import re
import requests
import os
import random
import time
import os
import pandas as pd
from datetime import datetime

#Calculates the normalized Levenshtein distance of 2 strings
def levenshtein(s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    matrix = [list(range(l1 + 1))] * (l2 + 1)
    for zz in list(range(l2 + 1)):
      matrix[zz] = list(range(zz,zz + l1 + 1))
    for zz in list(range(0,l2)):
      for sz in list(range(0,l1)):
        if s1[sz] == s2[zz]:
          matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
        else:
          matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
    distance = float(matrix[l2][l1])
    result = 1.0-distance/max(l1,l2)
    return result


#Untested matching function
def matching(text,master_list):
    result_list = [levenshtein(text, x) for x in master_list]
    result = max(result_list)
    return result

def veggyrecipe():
    ingredient_list = ','.join(random.sample(eng_seasonal(),2))
    uniseasonal = []
    for x in eng_unseasonal():
        uniseasonal.append('excluded='+x)
    uniseasonal = '&'.join(uniseasonal)
    appid = '&app_id='+os.environ['EDAMAM_app']
    appapi = '&app_key='+os.environ['EDAMAM_api']
    url = 'https://api.edamam.com/search?q='+ingredient_list+'&'+uniseasonal+appid+appapi+'&health=vegetarian'
    response = requests.request("GET", url)
    recipe = response.json()['hits'][0]['recipe']
    summary = '<a href='+recipe['url']+'>'+recipe['label']+'</a>'
    image = recipe['image']
    title = recipe['label']
    url = recipe['url']
    source = recipe['source']
    return 'Versuche es mal mit diesem leckeren Rezept:',summary, image,title,url,source

def veganrecipe():
    ingredient_list = ','.join(random.sample(eng_seasonal(),2))
    uniseasonal = []
    for x in eng_unseasonal():
        uniseasonal.append('excluded='+x)
    uniseasonal = '&'.join(uniseasonal)
    appid = '&app_id='+os.environ['EDAMAM_app']
    appapi = '&app_key='+os.environ['EDAMAM_api']
    url = 'https://api.edamam.com/search?q='+ingredient_list+'&'+uniseasonal+appid+appapi+'&health=vegan'
    response = requests.request("GET", url)
    recipe = response.json()['hits'][0]['recipe']
    summary = '<a href='+recipe['url']+'>'+recipe['label']+'</a>'
    image = recipe['image']
    title = recipe['label']
    url = recipe['url']
    source = recipe['source']
    return 'Versuche es mal mit diesem leckeren Rezept:',summary, image,title,url,source

def getrecipe():
    ingredient_list = ','.join(random.sample(eng_seasonal(),2))
    uniseasonal = []
    for x in eng_unseasonal():
        uniseasonal.append('excluded='+x)
    uniseasonal = '&'.join(uniseasonal)
    appid = '&app_id='+os.environ['EDAMAM_app']
    appapi = '&app_key='+os.environ['EDAMAM_api']
    url = 'https://api.edamam.com/search?q='+ingredient_list+'&'+uniseasonal+appid+appapi
    response = requests.request("GET", url)
    recipe = response.json()['hits'][0]['recipe']
    summary = '<a href='+recipe['url']+'>'+recipe['label']+'</a>'
    image = recipe['image']
    title = recipe['label']
    url = recipe['url']
    source = recipe['source']
    return 'Versuche es mal mit diesem leckeren Rezept:',summary, image,title,url,source

# Gemuesefunktionen

def seasonal():
    ledger = pd.read_csv("gemuese_full.csv",encoding = "utf-8", sep = ",")
    current_month = datetime.today().month
    seasonal = ledger.query("Month == "+str(current_month)).query("Seasonal == True")["gemuese"].tolist()
    return 'Diese Gemüsesorten sind diesen Monat in Saison:',seasonal

def unseasonal():
    ledger = pd.read_csv("gemuese_full.csv",encoding = "utf-8", sep = ",")
    current_month = datetime.today().month
    unseasonal = ledger.query("Month == "+str(current_month)).query("Seasonal == False")["gemuese"].tolist()
    return 'Diese Gemüsesorten sind diesen Monat NICHT in Saison:',unseasonal

def eng_seasonal():
    ledger = pd.read_csv("gemuese_full.csv",encoding = "utf-8", sep = ",")
    current_month = datetime.today().month
    seasonal = ledger.query("Month == "+str(current_month)).query("Seasonal == True")["vegetable"].tolist()
    return seasonal

def eng_unseasonal():
    ledger = pd.read_csv("gemuese_full.csv",encoding = "utf-8", sep = ",")
    current_month = datetime.today().month
    unseasonal = ledger.query("Month == "+str(current_month)).query("Seasonal == False")["vegetable"].tolist()
    return unseasonal

def in_list():
    ledger = pd.read_csv("gemuese_full.csv",encoding = "utf-8", sep = ",")
    master = ledger["gemuese"].tolist()
    return master

def suggestion():
    suggestion = random.sample(seasonal()[1],1)
    return 'Warum kochst Du heute nicht etwas mit:',suggestion

def look_up(veggie):
    season_list = [x.lower() for x in seasonal()[1]]
    master = [x.lower() for x in in_list()]
    approval = matching(veggie.lower(),season_list)
    in_master = matching(veggie.lower(),master)
    if approval > 0.7:
        approval = "Mmmmh, Saisonal...( ͡° ͜ʖ ͡°)"
    else:
        if in_master > 0.7:
            approval = "Igitt, importiert ಠ_ಠ"
        else:
            approval = "Ich kann das Gemüse in meiner Liste nicht finden. Ist es richtig geschrieben und auch ein heimisches Gemüse? Obst, Exotische Gemüse oder Getreide (wie Kartoffeln) sind in meiner Liste nicht enthalten."
    return approval