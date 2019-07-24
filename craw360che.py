import re
import requests
from bs4 import BeautifulSoup
import xlwt, xlrd
#
#在写css时，标签名不加任何修饰，类名前加点，id名前加 #，我们可以用类似的方法来筛选元素，用到的方法是soup.select()，返回类型是list。




def get_seeds():

    page = requests.get("http://www.360che.com/qianyinche/")
    soup = BeautifulSoup(page.content,"html5lib")
    a_tags = soup.find_all(href=re.compile(".66_index.html"))
    #brand = soup.select('.xll_center2_a1_z dd')
    #
    #
    # #for tag in a_tags:#  print(tag.get('href'), " ",tag.string)
    # #print(soup.dt.string)
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
    tr_class = talbe.find_all('tr', class_ = 'param-row')            #搜索所有param-row的class，输出列表，tr_class就是包含了所有列
    #td_tags = tr_class[2].find_all('td')
    #div_tags = tr_class[50].find_all('div')
    #print(td_tags)
    #print(div_tags[0].find(text=True).strip())
    #print(len(tr_class))
    ws_name = soup.find("div", class_='detail-header').h1.a.string.strip()          #做表的名字需要注意，可能爬的字符又特殊字符或者空格，所以运行出错，加上strip成功
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(ws_name)
    xl_col = 0
    for tr in tr_class:
        td_tag = tr.find('td', id=re.compile("ai_p_\d"))            #td_tag是excel的行标题
        div_tags = tr.find_all('div')
        ws.write(0, xl_col, td_tag.string)
        i=1
        for div in div_tags:
            ws.write(i,xl_col,div.find(text=True).strip())
            i+=1
        xl_col+=1
    wb.save(ws_name+'.xls')
"""
        try:
            df = td_tag.string
        except Exception:
            df = ''
        print(df)
        一开始爬的时候总是出错，AttributeError: 'NoneType' object has no attribute 'string，后来发现tr_class长度94，应该是47
        原来网页别的地方还有table标签，还有param-row，所以出了问题。
"""
        #print(td_tag.string)
        #div_tags = tr.find_all('div')
        #for div in div_tags:
        #    print(div.find(text=True).strip())
def load_seeds():           #从excel表格读取种子页面的url，返回一个要抓取列表
    seeds_wb = xlrd.open_workbook('urls.xls')
    seeds_ws = seeds_wb.sheet_by_name('urls')
    seeds = seeds_ws.col_values(2)
    return seeds

#get_table("https://product.360che.com/s25/6488_66_param.html")
#get_tb("https://product.360che.com/s27/6778_66_param.html")

def main():
    seeds = load_seeds()
    for seed in seeds:
        get_tb(seed)

main()
