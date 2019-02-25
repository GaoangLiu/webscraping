#!/user/bin/python3
from douban import Douban
import os
import sys 

def is_image(fname):
	return fname.endswith(tuple(['.jpg', '.png', 'jpeg', '.svg', '.gif']))

args = sys.argv[1::]
text = ' '
text = '\n'.join([i for i in args if not is_image(i)])
imgs = [str(os.path.realpath(i)) for i in args if is_image(i)]

Douban().postMedia(text, imgs)

