# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 12:55:29 2019

@author: Jiwitesh_Sharma
"""
# Importing the necessary Libraries
from flask_cors import CORS, cross_origin
from imagescrapperservice.ImageScrapperService import ImageScrapperService
from imagescrapper.ImageScrapper import ImageScrapper
from flask import Flask, render_template, request, jsonify


# import request
app = Flask(__name__)  # initialising the flask app with the name 'app'

#response = 'Welcome!'


@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/showImages')  # route to show the images on a webpage
@cross_origin()
def show_images(keyWord):
    scraper_object = ImageScrapper()  # Instantiating the object of class ImageScrapper
    # obtaining the list of image files from the static folder
    list_of_jpg_files = scraper_object.list_only_jpg_files('static')
    print(list_of_jpg_files)
    try:
        if(len(list_of_jpg_files) > 0):  # if there are images present, show them on a wen UI
            return render_template('showImage.html', user_images=list_of_jpg_files, keyWord=keyWord)
        else:
            # show this error message if no images are present in the static folder
            print("Please try with a different string")
            return render_template("404.html", keyWord=keyWord)
    except Exception as e:
        print('no Images found ', e)
        print("Please try with a different string")
        return render_template("404.html", keyWord=keyWord)


@app.route('/searchImages', methods=['GET', 'POST'])
@cross_origin()
def searchImages():
    print(request.method)
    if request.method == 'POST':
        print("entered post")
        # assigning the value of the input keyword to the variable keyword
        keyWord = request.form['keyword']

    else:
        print("did not enter post")
    print('printing = ' + keyWord)

    scraper_object = ImageScrapper()  # instantiating the class
    # obtaining the list of image files from the static folder
    list_of_jpg_files = scraper_object.list_only_jpg_files('static')
    # deleting the old image files stored from the previous search
    scraper_object.delete_existing_image(list_of_jpg_files)
    # splitting and combining the keyword for a string containing multiple words

    image_name = keyWord.split()
    image_name = '+'.join(image_name)
    print('keyword = ', keyWord, image_name)
    # adding the header metadata
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    service = ImageScrapperService()  # instantiating the object of class ImageScrapperService
    # (imageURLList, header, keyWord, fileLoc)
    print(keyWord, header)
    masterListOfImages = service.downloadImages(
        keyWord, header)  # getting the master list from keyword
    imageList = masterListOfImages[0]  # extracting the list of images from the master list
    # extracting the list of type of images from the masterlist
    imageTypeList = masterListOfImages[1]

    response = "We have downloaded ", len(imageList), "images of " + image_name + " for you"

    return show_images(keyWord)  # redirect the control to the show images method


# route to return the list of file locations for API calls
@app.route('/api/showImages', methods=['GET', 'POST'])
@cross_origin()
def get_image_url():
    if request.method == 'POST':
        print("entered post")
        # assigning the value of the input keyword to the variable keyword
        keyWord = request.json['keyword']

    else:
        print("Did not enter  post")
    print('printing = ' + keyWord)
    # splitting and combining the keyword for a string containing multiple words
    image_name = keyWord.split()
    image_name = '+'.join(image_name)
    # adding the header metadata
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    service = ImageScrapperService()  # instantiating the object of class ImageScrapperService
    url_enum = service.get_image_urls(keyWord, header)  # getting the URL enumeration
    url_list = []  # initializing and empty url list
    for i, (img, Type) in enumerate(url_enum[0:5]):
        # creating key value pairs of image URLs to be sent as json
        dict = {'image_url': img}
        url_list.append(dict)
    return jsonify(url_list)  # send the url list in JSON format


@app.errorhandler(404)
@cross_origin()
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8000) # port to run on local machine
    app.run(debug=True)  # to run on cloud
