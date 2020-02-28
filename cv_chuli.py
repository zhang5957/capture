import cv2
import numpy as np
from matplotlib import pyplot as plt


back_img = "back_ground.jpg"
slide_img = "slide_pic.jpg"
# 滑块图片二值化
block = cv2.imread(slide_img, 0)
# 背景文件二值化
template = cv2.imread(back_img, 0)
w,h = block.shape[::-1]
print(w,h)
# 二值化后的图片
block_name = 'block.jpg'
template_name = 'template.jpg'
# 保存二值化后的图片
cv2.imwrite(block_name,block)
cv2.imwrite(template_name,template)
# 将滑块图片灰度化
block = cv2.imread(block_name)
block = cv2.cvtColor(block,cv2.COLOR_RGB2GRAY)
# 反转block的值
block = abs(255-block)
cv2.imwrite(block_name,block)
block = cv2.imread(block_name)
template = cv2.imread(template_name)
# 获取偏移量
# 模板匹配，查找block在template中的位置，返回result是一个矩阵，是每个点的匹配结果
result = cv2.matchTemplate(block,template,cv2.TM_CCOEFF_NORMED)
x,y = np.unravel_index(result.argmax(),result.shape)
print(x,y)
offset = y*(280/680)
print(offset)
# 画矩形圈出匹配的区域
# 参数解释：1.原图 2.矩阵的左上点坐标 3.矩阵的右下点坐标 4.画线对应的rgb颜色 5.线的宽度
site = cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)
cv2.imwrite("paint.jpg", site)
# return offset





