# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Melissa"
__date__ = "$Oct 27, 2019 3:01:06 PM$"
 
import cookiejar 
from lxml import html 
from lxml import etree
from bs4 import BeautifulSoup
import cookielib
import re 
import operator 
import urllib
import urllib2
import requests

session = requests.Session()
session.headers.update({'User-Agent': 'Custom user agent'})

session.get('https://httpbin.org/headers')

top_limit = 9

def openWebsite():
    
    username = str(raw_input("Enter a Github username: "))
    print(username)
    repo_dict = {}
    
    url = "https://github.com/"+username+"?tab=repositories"
    
    #loop
    while True:
        jar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
        rep = opener.open(url)
        doc = html.fromstring(rep.read())
        
        repo_names = doc.xpath('//li[@class="col-14 d-block width-full border-bottom public source"]/div[@class="d-inline-block mb-1"]/h3/a/text()')
        repo_lists = []
        
        #obtaining name
        for name in repo_names:
            name = ' '.join(''.join(name).split())
            repo_lists.append(name)
            repo_dict[name] = 0
            
        responding = requests.get(url)
        soup = BeautifulSoup(responding.text, 'html.parser')
        
        soup = BeautifulSoup(responding.text, 'html.parser')
        di = soup.find_all('li', {'class': 'col-12 d-block width-full py-4 border-bottom public sources'})
        
        for d in di:
            tempo = d.find_all('di',{'class':'18 text-gray mt-2'})
            for t in tempo:
                #star count
                l = t.find_all('a', attrs={'href': re.compile("^\/[a-zA-Z0-9\-\.]+\/[a-zA-Z0-9\.\-\_]+\/stargazers")})
                #url
                if ln(l) is not 0:
                    name = l[0].get('href')
                    name = name[ln(username)+2:-11]
                    repo_dict[name] = int(l[0].text)
            #repositories on next page
            di = soup.find('a',{'class':'next_page'})
            
            if di is not None:
                url = di.get('href')
                url = "https://github.com/"+url
            else:
                break
                
            #sorting in reversed order to list from oldest to newest
            i=0
            sorting_repos = sorted(iter(repo_dict.items()), key = operator.itemgetter(1))
            
            for ode in reversed(sorting_repos):
                repo_url = "https://github.com/" + username + "/" + ode[0]
                print("\nrepository name : ",ode[0], "\nrepository url: ",repo_url, "\nstars   : ",ode[1])
                i = i + 1
                if i > top_limit:
                    break
    
                    
if __name__ == "__main__":
    openWebsite()
            