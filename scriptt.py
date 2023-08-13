import bs4
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import csv
URL = input('Enter home page URL : ')
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="tabular")
aaa=results.find('a')
jk=(aaa['href'])
cmlik="https://classic.clinicaltrials.gov"+jk

filename = 'scraped.csv'
f = open(filename,'w',newline = '')
music = csv.writer(f)

html = cmlik
npag=requests.get(html)
bsobj = BeautifulSoup(npag.content, "html.parser")
tbody = bsobj('table',{'class':'ct-data_table'})[0].findAll('tr')
xl = []
for row in tbody:
    cols = row.findChildren(recursive = False)
    cols = [element.text.strip() for element in cols]
    music.writerow(cols) 
    xl.append(cols)
#keywords on the page
import pandas as pd
df=pd.read_csv("scraped.csv",encoding='latin1',on_bad_lines='skip',header=None, names=range(2))
col_list = df.iloc[:,0].values.tolist()
col_list2 = df.iloc[:,1].values.tolist()
textt=' '.join(str(e) for e in col_list)
textt2=' '.join(str(e) for e in col_list2)
import nltk
ppp=nltk.tokenize.WordPunctTokenizer().tokenize(textt)
ppp2=nltk.tokenize.WordPunctTokenizer().tokenize(textt2)
print(ppp)
print(ppp2)
#selecting specific key word
keywordin=input("Insert keyword from above data : ")
dataFrame = pd.read_csv("scraped.csv",encoding='latin1',on_bad_lines='skip',header=None, names=range(2))
dataFrame = dataFrame.loc[dataFrame.iloc[:,0].str.contains(keywordin,na=False)].values.tolist()
textt3=' '.join(str(e) for e in dataFrame)
print(textt3)
#summarize
from transformers import pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
nofw=int(input("Enter number of words: "))
summary = summarizer(textt3, max_length=nofw, min_length=30)
import re
listToStr = ' '.join([str(elem) for elem in summary])
clean_text = re.sub(r'[^\w\s]', '', listToStr)
print(clean_text)
lent=len(clean_text)
print("Number of characters:"+str(lent))