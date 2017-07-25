需要：

* firefox 浏览器
* pip install selenium
* 浏览器驱动:
    * firefox[https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)
        * chmod +x geckodriver
        * sudo cp geckodriver /usr/bin
    * chrome[chromedriver](./chromedriver)
        * chmod +x chromedriver
        * sudo cp chromedriver /sur/bin
    
个性化运行时可能需要修改的地方：

* crawler.py Ids换为您需要的id，也可保持不变
* 



遇到过的障碍：

* selenium的span单击报错：
    * `</iframe> is not clickable at point` 
    * 解决办法：
    ```python
        # change
        songsAll = driver.find_element_by_css_selector('#songsall')
        action_chains = ActionChains(driver)
        action_chains.click(songsAll)
        action_chains.perform()
      
        # to
        songsAll = driver.find_element_by_css_selector('#songsall')
        driver.execute_script('arguments[0].click();',songsAll)
    ```
    