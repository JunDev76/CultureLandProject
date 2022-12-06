def main():
    import math
    import sys
    import time

    import chromedriver_autoinstaller
    import requests
    from selenium import webdriver

    path = chromedriver_autoinstaller.install()

    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    driver = webdriver.Chrome(path, options=options)
    # py [~~~.py "~~~"]
    gets = sys.argv[1].split('/')

    nickname = gets[0]
    del gets[0]

    pincodes = gets

    time.sleep(2)

    driver.get("https://m.cultureland.co.kr/csh/cshGiftCard.do")

    # 로그인이 되어있지 않을때.
    if driver.current_url != "https://m.cultureland.co.kr/csh/cshGiftCard.do":
        # 로그인 사이트로~!
        driver.get("https://m.cultureland.co.kr/mmb/loginMain.do")

        Cul_ID = requests.get("https://www.crsbe.kr/cul_pay/getID").text
        Cul_PW = "@@@@@@@@@@@@@@@@@@@@Changed@@@@@@@@@@@@@@@@@@@@@"

        # 아이디 입력
        driver.find_element_by_id("txtUserId").send_keys(Cul_ID)

        # 키보드창 띄우기
        driver.find_element_by_id("passwd").click()
        for key in Cul_PW:
            # 보안 키패드 누르기
            driver.find_element_by_xpath('//*[@alt="' + key + '"]').click()

        # 입력 완료 버튼
        driver.find_element_by_xpath('//*[@id="mtk_done"]/div/img').click()

        # 로그인 버튼
        driver.find_element_by_xpath('//*[@id="btnLogin"]').click()

    index = 0
    for code in pincodes:
        index += 1
        count = -1
        open_keypad = False
        for key in list(code):
            count += 1
            index_slot = str(index)
            slot = str(math.floor(count / 4) + 1)
            if slot == "5":
                slot = "4"

            element = driver.find_element_by_id("txtScr" + index_slot + slot)
            if slot == "4":
                if not open_keypad:
                    open_keypad = True
                    element.click()

                driver.execute_script(
                    driver.find_element_by_xpath('//*[@alt="' + key + '"]/../..').get_attribute("onmousedown"))
                if count / 4 == 0.75:
                    # 입력 완료 버튼
                    driver.find_element_by_xpath('//*[@id="mtk_done"]/div/img').click()
            else:
                element.send_keys(key)

    driver.find_element_by_xpath('//*[@id="btnCshFrom"]').click()

    money = driver.find_element_by_class_name('charge_result')
    charge_krw = money.find_element_by_tag_name('dd').text

    now = time.localtime()
    driver.save_screenshot(
        "cashed/{0}년_{1}월{2}일_{3}시_{4}분_{5}초__" + nickname + ".png".format(now.tm_year, now.tm_mon, now.tm_mday,
                                                                           now.tm_hour,
                                                                           now.tm_min, now.tm_sec))

    import re

    charge_krw = re.sub(r'[^0-9]', '', charge_krw)

    import requests

    requests.get("https://www.crsbe.kr/cul_pay/finish?nick=" + nickname + "&pay=" + charge_krw)

    quit()
    return


if __name__ == "__main__":
    main()
