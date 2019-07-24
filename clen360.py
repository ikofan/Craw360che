import re
import requests
from bs4 import BeautifulSoup
import xlwt, xlrd



def get_seeds():

    page = requests.get("http://www.360che.com/qianyinche/")
    soup = BeautifulSoup(page.content,"html5lib")
    a_tags = soup.find_all(href=re.compile(".66_index.html"))
    div_tags = soup.select('.xll_center2_a1_y2 dt')
    source_urls = xlwt.Workbook(encoding='utf-8')
    ws = source_urls.add_sheet('urls')
    r=0
    for tag in div_tags:
        ws.write(r,0,tag.a.string)
        ws.write(r,1,tag.a.get('href'))
        param = tag.a.get('href').replace('index','param')
        ws.write(r,2,param)
        r+=1
    source_urls.save('urls.xls')

def get_tb(seed):
    page = requests.get(seed)
    soup = BeautifulSoup(page.content, 'html5lib')
    talbe = soup.select_one("table")
    tr_class = talbe.find_all('tr', class_ = 'param-row')
    ws_name = soup.find("div", class_='detail-header').h1.a.string.strip()
    ws = wb.add_sheet(ws_name)
    xl_col = 0
    for tr in tr_class:
        td_tag = tr.find('td', id=re.compile("ai_p_\d"))
        div_tags = tr.find_all('div')
        ws.write(0, xl_col, td_tag.string)
        i=1
        for div in div_tags:
            ws.write(i,xl_col,div.find(text=True).strip())
            i+=1
        xl_col+=1
    wb.save(ws_name+'.xls')

    seeds_wb = xlrd.open_workbook('urls.xls')
    seeds_ws = seeds_wb.sheet_by_name('urls')
    seeds = seeds_ws.col_values(2)
    return seeds


def main():
    seeds = load_seeds()
    for seed in seeds:
        get_tb(seed)


main()
