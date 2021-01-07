""" This module contains functions that manipulate local_var.encrypted and resizes images"""

from os import listdir, rename, mkdir
from PIL import Image, UnidentifiedImageError, ImageFile
LOAD_TRUNCATED_IMAGES = True


def resize_images_in_folder(path):
    """ This function is run at the start of the program.
        It crops and resizes images in candidate_photos to 300x300 px """

    # Iterates through all images in the given folder
    try:
        for image in listdir(path):
            picture_path = path+'/'+image

            try:
                # Resizes and crops images depending on the orientation of the image
                pic = Image.open(picture_path)
                aspect_ratio = pic.size[1]/pic.size[0]

                if aspect_ratio >= 1:  # If image is in portrait/square orientation
                    pic = pic.resize((300, int(300*aspect_ratio)))
                    pic = pic.crop(
                        (0, (pic.size[1]-300)/2, 300, pic.size[1]-(pic.size[1]-300)/2))
                    pic.save(picture_path)

                elif aspect_ratio < 1:  # If the image in landscape orientation
                    aspect_ratio = pic.size[0]/pic.size[1]
                    pic = pic.resize((int(300*aspect_ratio), 300))
                    pic = pic.crop(
                        ((pic.size[0]-300)/2, 0, pic.size[0]-(pic.size[0]-300)/2, 300))
                    pic.save(picture_path)

            except UnidentifiedImageError:
                # Run if the file is not an image file
                # Places '[Corrupt] at the beginning of the file name
                image_name = picture_path[len(
                    picture_path)-picture_path[::-1].index('/'):]
                if not image_name.startswith('[Corrupt]'):
                    rename(picture_path, picture_path[:len(picture_path)-picture_path[::-1]
                                                      .index('/')-1]+'/[Corrupt] '+image_name)
    except FileNotFoundError:
        try:
            mkdir('candidate_photos')
        except FileExistsError:
            pass


def store_house_choice(choice, *type):
    """ Adds house choice to the file local_vars.encrypted """

    open_type = 'r+' if not type else 'w+'
    with open('local_vars.encrypted', open_type) as file:

        # Attempts to retreive db uri; default is blank
        try:
            uri = file.readlines()[-1]
        except IndexError:
            uri = 'DB URI: '

        # File is overwritten with the given house choice and db uri
        file.truncate(0)
        file.seek(0)
        file.writelines([f'House Choice: {choice.lower()}'+'\n', uri])


def get_house_choice():
    """ Retrieves the house choice from local_vars.encrypted """

    try:
        with open('local_vars.encrypted', 'r+') as file:
            return file.readlines()[0][14:-1]
    except FileNotFoundError:
        store_house_choice('kingfisher', 'w+')
        return get_house_choice()


def store_db_uri(uri):
    """ Adds database connection string to the file local_vars.encrypted """

    try:
        with open('local_vars.encrypted', 'r+') as file:
            house_choice = file.readlines()[0]
            file.truncate(0)
            file.seek(0)
            file.writelines([house_choice, f'DB URI: {uri}'])
    except (IndexError, FileNotFoundError):
        with open('local_vars.encrypted', 'w+') as file:
            file.writelines(['House Choice: ', f'DB URI: {uri}'])


def get_db_uri():
    """ Retrieves the db uri from local_vars.encrypted """

    try:
        with open('local_vars.encrypted', 'r+') as file:
            try:
                uri = file.readlines()[1][8:]
            except IndexError:
                return 'mongodb://localhost:27017/'
            if '/' not in uri:
                return 'mongodb://localhost:27017/'
            return uri
    except FileNotFoundError:
        return 'mongodb://localhost:27017/'
