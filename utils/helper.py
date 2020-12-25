import os
import pandas


def get_second_value(list_of_tuples, first_value):
	return next((y for x,y in list_of_tuples if x == first_value), None)

def get_url_citra(kelas):
    image_name = 'citra-kelas'
    image_filename = ['crassnaa.jpg', 'micro.jpg', 'sinensis.jpg', 'subintegra.jpg']


    if (kelas == 0):
        image_name = os.path.join(image_name, 'crassnaa.jpg')
    elif (kelas == 1):
        image_name = os.path.join(image_name, 'micro.jpg')
    elif (kelas == 2):
        image_name = os.path.join(image_name, 'sinensis.jpg')
    elif (kelas == 3):
        image_name = os.path.join(image_name, 'subintegra.jpg')
    else:
        image_name = None

    return image_name
