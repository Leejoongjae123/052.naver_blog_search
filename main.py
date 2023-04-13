import datetime
import re

import requests
from bs4 import BeautifulSoup
import openpyxl
import time


def get_search(keyword):
    cookies = {
        'NNB': 'IZBJERH4DQMGI',
        'nx_ssl': '2',
        'ASID': '798f73fa0000018710b1765100000069',
        '_naver_usersession_': 'TL874wzdVUmzGRcRNe7Lcg==',
        'page_uid': 'ivR/PlprvmsssUHi6eCssssssSd-400126',
    }

    headers = {
        'authority': 'search.naver.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': 'NNB=IZBJERH4DQMGI; nx_ssl=2; ASID=798f73fa0000018710b1765100000069; _naver_usersession_=TL874wzdVUmzGRcRNe7Lcg==; page_uid=ivR/PlprvmsssUHi6eCssssssSd-400126',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="111.0.5563.147", "Not(A:Brand";v="8.0.0.0", "Chromium";v="111.0.5563.147"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }

    params = {
        'sm': 'tab_hty.top',
        'where': 'nexearch',
        'query': str(keyword),
        'oquery': str(keyword),
        'tqi': 'ivR+Ylp0JXossR45ew4sssssszd-473617',
    }

    response = requests.get('https://search.naver.com/search.naver', params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup
def get_urls(keyword):

    headers={"User-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    soup=get_search(keyword)

    type_a_urls = []
    type_b_urls = []
    type_c_urls = []
    urls = []


    all_smart_blocks=soup.find_all('section',attrs={'class':re.compile('sc_new sp_intent_block')})
    if len(all_smart_blocks)>=1:
        print("스마트블록많음",len(all_smart_blocks))
        for index,section in enumerate(all_smart_blocks):
            posting=""
            name=""
            try:
                title=section.find('div',attrs={'class':'title_area'}).get_text()
            except:
                title="없음"

            if title.find("인기 주제")>=0: #인기주제 URL 가져오기
                # text=section.find('strong',attrs={'class':'title'}).get_text()
                # print('text:', text)
                categorys=section.find_all('div',attrs={'class':'flick_bx'})
                for category in categorys: # 인기주제 내에서 칵 카드별 URL가져오기
                    url=category.find('a',attrs={'class':re.compile('popular_block_wrap')})
                    if url==None:
                        break
                    url=url['href']
                    # print('url:', url)
                    # type_a_urls_pre.append(url)
                    urls.append(url)
                #각 서칭 결과 확인하기
                for url in urls:
                    res=requests.get(url,headers=headers)
                    soup=BeautifulSoup(res.text,'lxml')
                    ul_tag=soup.find('ul',attrs={'class':re.compile('keyword_challenge_list')})
                    # print('ul_tag:',ul_tag)
                    li_tags=ul_tag.find_all('li')
                    # print(len(li_tags))
                    for index,li_tag in enumerate(li_tags): # 각 카드 안에 들어가서 url 모두 가져오기
                        if index==5:
                            break
                        url=li_tag.find('a',attrs={'class':'title _intent_cross_collection_trigger'})['href']
                        name=li_tag.find('a',attrs={'class':'name'}).get_text()
                        posting = li_tag.find('a', attrs={'class': 'title _intent_cross_collection_trigger'}).get_text()
                        type_a_urls.append([index+1,name,url,posting])
                        # print('url:',url)
            else:
                type_c_url_element = []
                text = section.find('strong', attrs={'class': 'intent_title'}).get_text()
                print('text:', text)
                if text.find("인플루언서")>=0:
                    contents_cards=section.find_all('a',attrs={'class':'title _intent_cross_collection_trigger'})
                    for index,contents_card in enumerate(contents_cards):
                        url=contents_card['href']
                        name = section.find_all('a',attrs={'class':'name'})[index].get_text()
                        posting = section.find_all('a', attrs={'class': 'title _intent_cross_collection_trigger'})[index].get_text()
                        type_b_urls.append([index+1,name,url,posting])
                else:
                    contents_cards = section.find_all('a', attrs={'class': 'title _intent_cross_collection_trigger'})
                    for index,contents_card in enumerate(contents_cards):
                        url = contents_card['href']
                        name = section.find_all('a', attrs={'class': 'name'})[index].get_text()
                        posting = section.find_all('a', attrs={'class': 'title _intent_cross_collection_trigger'})[index].get_text()
                        type_c_urls.append([index+1,name,url,posting])
    else:
        print("스마트블록1개짜리")
        section=soup.find('section',attrs={'class':re.compile('sc_new sp_nreview _prs_rvw _au_view_collection')})
        contents_cards = section.find_all('li', attrs={'class': 'bx _svp_item'})
        for index, contents_card in enumerate(contents_cards):
            url = contents_card.find('a',attrs={'class':'api_txt_lines total_tit _cross_trigger'})['href']
            name = contents_card.find('a', attrs={'class': 'sub_txt sub_name'}).get_text()
            posting = contents_card.find('a', attrs={'class': 'api_txt_lines total_tit _cross_trigger'}).get_text()
            type_c_urls.append([index + 1, name, url, posting])


    print('type_a_urls:',type_a_urls)
    print('type_b_urls:',type_b_urls)
    print('type_c_urls:',type_c_urls)

    return type_a_urls,type_b_urls,type_c_urls
def load_excel():
    wb = openpyxl.load_workbook('keyword.xlsx')
    ws = wb.active
    no_row = ws.max_row
    print("행갯수:", no_row)
    data_list = []
    for i in range(2, no_row + 1):
        name = ws.cell(row=i, column=1).value
        if name == "" or name == None:
            print('데이타 더 이상 없음')
            break
        keyword=ws.cell(row=i, column=2).value
        data = [name, keyword]
        data_list.append(data)
    print(data_list)
    return data_list
fff
wb=openpyxl.Workbook()
ws=wb.active
column_name=['제품','키워드','카테고리','블로그명','글제목',"URL",'키워드별상위노출개수','순위']
ws.append(column_name)

time_now_string=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
keyword_infos=load_excel() # 키워드가 져오기
time_period=0.5
for keyword_info in keyword_infos:
    count=0
    print("keyword:",keyword_info[1])
    type_a_urls,type_b_urls,type_c_urls=get_urls(keyword_info[1]) #키워드에 대한 URL 모두 발췌하기

    search_list=['위크나인','워크나인','위트나인','워터나인']
    headers={"User-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    type_a_result=[]
    type_b_result=[]
    type_c_result=[]

    for type_a_url in type_a_urls:
        res=requests.get(type_a_url[2],headers=headers)
        soup=BeautifulSoup(res.text,'lxml')
        try:
            info_iframe=soup.find('iframe',attrs={'id':'mainFrame'})['src']
        except:
            print("확인불가블로그")
            continue
        real_url='https://blog.naver.com'+soup.find('iframe',attrs={'id':'mainFrame'})['src']
        print('real_url:',real_url)
        res = requests.get(real_url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        # print(soup.prettify())
        find_flag=False
        try:
            contents=soup.find('div',attrs={'class':'se-main-container'}).get_text()
        except:
            print("에러인듯")
            continue
        category="스마트블록"
        for search_elem in search_list:
            if contents.find(search_elem)>=0:
                data=[keyword_info[0],keyword_info[1],category,type_a_url[1],type_a_url[3],type_a_url[2],"",type_a_url[0]]
                count=count+1
                type_a_result.append(data)
        time.sleep(time_period)

    for type_b_url in type_b_urls:
        res=requests.get(type_b_url[2],headers=headers)
        soup=BeautifulSoup(res.text,'lxml')
        try:
            info_iframe=soup.find('iframe',attrs={'id':'mainFrame'})['src']
        except:
            print("확인불가블로그")
            continue
        real_url='https://blog.naver.com'+soup.find('iframe',attrs={'id':'mainFrame'})['src']
        print('real_url:',real_url)
        res = requests.get(real_url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        # print(soup.prettify())
        find_flag=False
        try:
            contents=soup.find('div',attrs={'class':'se-main-container'}).get_text()
        except:
            print("에러인듯")
            continue
        category="인플루언서탭"
        for search_elem in search_list:
            if contents.find(search_elem)>=0:
                data=[keyword_info[0],keyword_info[1],category,type_b_url[1],type_b_url[3],type_b_url[2],"",type_b_url[0]]
                count = count + 1
                type_b_result.append(data)
        time.sleep(time_period)

    for type_c_url in type_c_urls:
        res=requests.get(type_c_url[2],headers=headers)
        soup=BeautifulSoup(res.text,'lxml')
        # print(soup.prettify())
        try:
            info_iframe=soup.find('iframe',attrs={'id':'mainFrame'})['src']
        except:
            print("확인불가블로그")
            continue
        real_url='https://blog.naver.com'+soup.find('iframe',attrs={'id':'mainFrame'})['src']
        print('real_url:',real_url)
        res = requests.get(real_url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        # print(soup.prettify())
        find_flag=False
        try:
            contents=soup.find('div',attrs={'class':'se-main-container'}).get_text()
        except:
            print("에러인듯")
            continue
        category="VIEW"
        for search_elem in search_list:
            if contents.find(search_elem)>=0:
                data=[keyword_info[0],keyword_info[1],category,type_c_url[1],type_c_url[3],type_c_url[2],"",type_c_url[0]]
                count = count + 1
                type_c_result.append(data)
        time.sleep(time_period)

    print('type_a_result:',type_a_result)
    print('type_b_result:',type_b_result)
    print('type_c_result:',type_c_result)

    for type_a_result_elem in type_a_result:
        type_a_result_elem[6]=count
        ws.append(type_a_result_elem)

    for type_b_result_elem in type_b_result:
        type_b_result_elem[6] = count
        ws.append(type_b_result_elem)

    for type_c_result_elem in type_c_result:
        type_c_result_elem[6] = count
        ws.append(type_c_result_elem)
    wb.save('result_{}.xlsx'.format(time_now_string))


