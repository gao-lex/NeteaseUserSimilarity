from selenium import webdriver
from selenium.webdriver import ActionChains
class User:
    def __init__(self,nikeName,level,fans,songsRank):
        self.nikeName = nikeName
        self.level = level
        self.fans = fans
        self.songsRank = songsRank

def crawler():
    ids = ['100544935']
    doneIds = []
    homeUrl = 'http://music.163.com/#/user/home?id='
    # 粉丝列表
    fansUrl = 'http://music.163.com/#/user/fans?id='
    # 听歌排行
    songsRankUrl = 'http://music.163.com/#/user/songs/rank?id='

    # driver = webdriver.Chrome()
    driver = webdriver.Firefox()

    while len(ids) != 0:
        driver.get(fansUrl+ids[0])
        # 获取g_iframe中的元素信息
        driver.switch_to_frame('g_iframe')

        # 获取nikeName和等级
        headBox = driver.find_element_by_id('head-box')
        nikeName,level = headBox.find_element_by_id('j-name-wrap').text.split('\n')

        # 获取前20个粉丝的Id
        mainBox = driver.find_element_by_id('main-box')
        fansBoxs = mainBox.find_elements_by_tag_name('li')
        for li in fansBoxs:
            ids.append(li.find_element_by_tag_name('a').get_attribute('href').split('id=')[-1])

        # 获取所有时间听歌排行前100
        driver.get(songsRankUrl + ids[0])
        # 获取g_iframe中的元素信息
        driver.switch_to_frame('g_iframe')

        # 点击进入所有时间的听歌排行
        songsAll = driver.find_element_by_css_selector('#songsall')
        driver.execute_script('arguments[0].click();',songsAll)
        songsBox = driver.find_element_by_id('m-record').find_elements_by_tag_name('li')
        for song in songsBox:
            print(song)


        doneIds.append(ids[0])

        del ids[0]

crawler()