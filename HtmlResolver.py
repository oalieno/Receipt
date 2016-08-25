from bs4 import BeautifulSoup
import logging as log

class HtmlResolver(object):
    def __init__(self):
        pass
    def solve(self,content):
        soup = BeautifulSoup(content,"lxml")
        data = (soup.select(".lpTb tr")[1]).select("td")
        log.debug("soup : {}".format(data))
        if len(data) == 0:
            return False,0
        elif len(data) == 3:
            return True,0
        else:
            return True,int((soup.select(".lpTb tr")[1]).select("td")[4].text.strip().replace(",",""))
