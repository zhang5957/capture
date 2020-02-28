from selenium import webdriver
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import random
import time

USERNAME = '13585111531'
PASSWORD = 'jtyhzyc97'

class CrackDouBan:
    def __init__(self):
        self.url = "https://www.douban.com/"
        self.driver_path = r"G:\迅雷下载\chromedriver_win32(1)\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.username = USERNAME
        self.password = PASSWORD

    def login(self):
        self.driver.get(self.url)
        self.driver.switch_to_frame(0)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/ul[1]/li[2]").click()
        self.driver.find_element_by_xpath("//*[@id='username']").send_keys(self.username)
        self.driver.find_element_by_xpath("//*[@id='password']").send_keys(self.password)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[5]/a").click()

    def get_capture(self):
        # 找到验证码的frame，并且切换过去
        WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/iframe"))
        )
        self.iFrame = self.driver.find_element_by_xpath("/html/body/div[6]/iframe")
        self.driver.switch_to_frame(self.iFrame)
        # 下载验证码的背景图和滑块图
        self.backgroud_url = self.driver.find_element_by_id("slideBkg").get_attribute('src')
        self.slide_url = self.driver.find_element_by_id('slideBlock').get_attribute('src')
        r = requests.get(self.backgroud_url)
        with open('back_ground.jpg','wb') as f:
            f.write(r.content)
        t = requests.get(self.slide_url)
        with open('slide_pic.jpg','wb') as fp:
            fp.write(t.content)
        # 获取偏移量
        offset1 = self.get_img_offset()
        track = self.get_track(offset1+random.randint(30,40))
        print(track)
        # 模拟鼠标动作链，进行滑块操作
        button = self.driver.find_element_by_id("tcaptcha_drag_button")
        # 拖动操作用到ActionChains类，实例化
        action = ActionChains(self.driver)
        # perform()用来执行ActionChains中存储的行为
        action.click_and_hold(button).perform()
        # action.move_to_element_with_offset(to_element=button, xoffset=offset1, yoffset=0).perform()
        # 清除之前的action
        # action.reset_actions()
        for i in track:
            action.drag_and_drop_by_offset(button, xoffset=i, yoffset=0).perform()
            action.reset_actions()
            print("1")

        action.release().perform()
        time.sleep(3)



    def get_img_offset(self):
        self.back_img = "back_ground.jpg"
        self.slide_img = "slide_pic.jpg"
        block = cv2.imread(self.slide_img, 0)
        template = cv2.imread(self.back_img, 0)
        w, h = block.shape[::-1]
        print(w, h)
        # 二值化后的图片
        block_name = 'block.jpg'
        template_name = 'template.jpg'
        # 保存二值化后的图片
        cv2.imwrite(block_name, block)
        cv2.imwrite(template_name, template)
        # 将滑块图片灰度化
        block = cv2.imread(block_name)
        block = cv2.cvtColor(block, cv2.COLOR_RGB2GRAY)
        # 反转block的值
        block = abs(255 - block)
        cv2.imwrite(block_name, block)
        block = cv2.imread(block_name)
        template = cv2.imread(template_name)
        # 获取偏移量
        # 模板匹配，查找block在template中的位置，返回result是一个矩阵，是每个点的匹配结果
        result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(result.argmax(), result.shape)
        print(x, y)
        offset = y * (280 / 680)
        # 画矩形圈出匹配的区域
        # 参数解释：1.原图 2.矩阵的左上点坐标 3.矩阵的右下点坐标 4.画线对应的rgb颜色 5.线的宽度
        site = cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)
        cv2.imwrite("paint.jpg", site)
        return offset

    def get_track(self,offset):
        track = []
        current = 0
        mid = offset * 3 / 4
        t = random.randint(2, 3) / 10
        v = 0
        while current < offset:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move, 2))
        return track


    def run(self):
        self.login()
        self.get_capture()



if __name__ == '__main__':
    spider = CrackDouBan()
    spider.run()


