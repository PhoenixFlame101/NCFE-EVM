# This module contains functions that are device specific

from PIL import Image, UnidentifiedImageError
from os import listdir, rename

def resize_image(picture_path):
	try:
		pic = Image.open(picture_path)
		aspect_ratio = pic.size[1]/pic.size[0]
		if aspect_ratio >= 1:
			pic = pic.resize((300, int(300*aspect_ratio)))
			pic = pic.crop((0, (pic.size[1]-300)/2, 300, pic.size[1]-(pic.size[1]-300)/2))
			pic.save(picture_path)
		elif aspect_ratio < 1:
			aspect_ratio = pic.size[0]/pic.size[1]
			pic = pic.resize((int(300*aspect_ratio), 300))
			pic = pic.crop(((pic.size[0]-300)/2, 0, pic.size[0]-(pic.size[0]-300)/2, 300))
			pic.save(picture_path)
	except UnidentifiedImageError:
		image_name = picture_path[len(picture_path)-picture_path[::-1].index('/'):]
		if not image_name.startswith('[Corrupt]'):
			rename(picture_path, picture_path[:len(picture_path)-picture_path[::-1].index('/')-1]+'/[Corrupt] '+image_name)


def resize_images_in_folder(path):
	for image in listdir(path):
		resize_image(path+'/'+image)


def store_house_choice(choice):
	with open('local_vars.encrypted', 'r+') as f:
		try:
				uri = f.readlines()[-1]
		except:
				uri = ''
		f.truncate(0)
		f.seek(0)
		f.writelines([f'House Choice: {choice.lower()}'+'\n', uri])


def get_house_choice():
	try:
		with open('local_vars.encrypted', 'r+') as f:
			return f.readlines()[0][14:-1]
	except FileNotFoundError:
		store_house_choice('kingfisher')
		return get_house_choice()


def store_db_uri(uri):
	try:
		with open('local_vars.encrypted', 'r+') as f:
			house_choice = f.readlines()[0]
			f.truncate(0)
			f.seek(0)
			f.writelines([house_choice, f'DB URI: {uri}'])
	except:
		with open('local_vars.encrypted', 'w+') as f:
			f.writelines(['\n', f'DB URI: {uri}'])


def get_db_uri():
	try:
		with open('local_vars.encrypted', 'r+') as f:
			uri = f.readlines()[1][8:]
			if '/' not in uri:
				return 'mongodb://localhost:27017/'
			else:
				return uri
	except FileNotFoundError:
		store_db_uri('')
		return get_db_uri()
