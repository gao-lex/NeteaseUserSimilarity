import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
import pandas as pd
import json

# 粉丝列表
fansUrl = 'http://music.163.com/#/user/fans?id='
# 听歌排行
songsRankUrl = 'http://music.163.com/#/user/songs/rank?id='

def crawler(numberOfUsers):
    UserDict = {}
    ids = ['100544935']
    doneIds = []

    driver = webdriver.Chrome()
    # driver = webdriver.Firefox()
    driver.implicitly_wait(2)
    i = 1
    while len(ids) != 0 and len(doneIds)!=numberOfUsers :
        print('正在抓取第'+str(i)+'个用户'+ids[0]+'未抓取的数量为'+str(len(ids)-1))
        try:
            if ids[0] not in doneIds:
                driver.get(fansUrl+ids[0])
                # 获取g_iframe中的元素信息
                driver.switch_to_frame('g_iframe')

                # 获取nikeName和等级
                headBox = driver.find_element_by_id('head-box')
                nikeName,level = headBox.find_element_by_id('j-name-wrap').text.split('\n')
                fansList = []
                # 获取前20个粉丝的Id
                mainBox = driver.find_element_by_id('main-box')
                fansBoxs = mainBox.find_elements_by_tag_name('li')
                for li in fansBoxs:
                    fanid = li.find_element_by_tag_name('a').get_attribute('href').split('id=')[-1]
                    ids.append(fanid)
                    fansList.append(fanid)

                # 获取所有时间听歌排行前100
                driver.get(songsRankUrl + ids[0])
                # 获取g_iframe中的元素信息
                driver.switch_to_frame('g_iframe')

                # 点击进入所有时间的听歌排行
                songsAllRank = driver.find_element_by_id('songsall')
                driver.execute_script('arguments[0].click();',songsAllRank)
                songsBox = driver.find_element_by_id('m-record').find_elements_by_css_selector('span.txt')
                songsAllRankDict ={}
                for song in songsBox:
                    songID = song.find_element_by_tag_name('a').get_attribute('href').split('id=')[-1]
                    songNme = song.text
                    songsAllRankDict[songID] = songNme

                UserDict[ids[0]] = {
                    'nickName':nikeName,
                    'level':level,
                    'fans':fansList,
                    'songsAllRank':songsAllRankDict
                }

                doneIds.append(ids[0])
        except selenium.common.exceptions.NoSuchElementException as e:
            print('出错了，自动跳过')
        finally:
            del ids[0]
            i+=1
    with open('./info.json','w') as f:
        json.dump(UserDict,f)

crawler(100)