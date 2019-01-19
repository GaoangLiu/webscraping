import requests
from bs4 import BeautifulSoup

params = {'atc_content':'马刺输的有点小惨啊。。。'}
s = requests.Session()


text = "@bbli 保存图片 ls 不知道啊"

res = text.replace('保存图片','...').replace('@', '#')
print(res)

import random
print('bre' + str(random.randint(1,3)))