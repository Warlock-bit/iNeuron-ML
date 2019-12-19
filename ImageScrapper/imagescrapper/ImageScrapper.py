# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 12:11:13 2019

@author: Jiwitesh_Sharma
"""
from bs4 import BeautifulSoup as bs
import os
import json
import urllib.request
import urllib.parse
import urllib.error
from urllib.request import urlretrieve


class ImageScrapper:
    def delete_existing_image(self, list_of_images):
        for self.image in list_of_images:
            try:
                os.remove("./static/"+self.image)
            except Exception as e:
                print('error in deleting:  ', e)
        return 0

    def list_only_jpg_files(self, folder_name):
        self.list_of_jpg_files = []
        self.list_of_files = os.listdir(folder_name)
        print('list of files==')
        print(self.list_of_files)
        for self.file in self.list_of_files:
            self.name_array = self.file.split('.')
            if(self.name_array[1] == 'jpg'):
                self.list_of_jpg_files.append(self.file)
            else:
                print('filename does not end withn jpg')
        return self.list_of_jpg_files

    def createURL(self, keyWord):
        keyWord = keyWord.split()
        keyWord = '+'.join(keyWord)
        url = "https://www.google.co.in/search?q=" + keyWord + "&source=lnms&tbm=isch"
        return url
        # print (url)
        # add the directory for your image here

    def get_RawHtml(self, url, header):
        # url = "https://acadgild.com/customers/reviews"
        # header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        req = urllib.request.Request(url, headers=header)
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        html = bs(respData, 'html.parser')
        return html

    # contains the link for Large original images, type of  image
    def getimageUrlList(self, rawHtml):
        imageUrlList = []
        for a in rawHtml.find_all("div", {"class": "rg_meta"}):
            link, imageExtension = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
            imageUrlList.append((link, imageExtension))

        print("there are total", len(imageUrlList), "images")
        return imageUrlList

    @staticmethod
    def clean_image(self):
        os.chdir('./static')
        for _, _, filename in os.walk(os.getcwd()):
            for file in filename:
                if file.endswith('.jpg'):
                    try:
                        img = Image.open(os.getcwd()+'/'+file)  # open the image file
                        img.verify()  # verify the image file
                    except (IOError, SyntaxError) as e:
                        os.remove(file)

    def downloadImagesFromURL(self, imageUrlList, image_name, header):
        masterListOfImages = []
        count = 0
        # print images
        imageFiles = []
        imageTypes = []
        # header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        #        }
        image_counter = 0
        # print(imageUrlList)
        for i, (img, Type) in enumerate(imageUrlList):
            if Type in ['jpg', 'png']:
                print(Type)
                try:
                    if (count > 5):
                        break
                    else:
                        count = count + 1
                    req = urllib.request.Request(img, headers=header)
                    try:
                        urllib.request.urlretrieve(
                            img, "./static/"+image_name+str(image_counter)+".jpg")
                        image_counter = image_counter+1
                    except Exception as e:
                        print("Image write failed:  ", e)
                        image_counter = image_counter + 1
                    respData = urllib.request.urlopen(req)
                    raw_img = respData.read()
                    # soup = bs(respData, 'html.parser')

                    imageFiles.append(raw_img)
                    imageTypes.append(Type)

                except Exception as e:
                    print("could not load : " + img)
                    print(e)
                    count = count + 1
        masterListOfImages.append(imageFiles)
        masterListOfImages.append(imageTypes)

        return masterListOfImages

    ''' for i , (img , Type) in enumerate( imageUrlList):
           try:
               req = urllib.request.Request(img, headers = header)
               respData = urllib.request.urlopen(req)
               raw_img = respData.read()

               cntr = len([i for i in os.listdir(fileLoc) if image_type in i]) + 1
               print (cntr)
               if len(Type)==0:
                   f = open(os.path.join(fileLoc , image_type + "_"+ str(cntr)+".jpg"), 'wb')
               else :
                   f = open(os.path.join(fileLoc , image_type + "_"+ str(cntr)+"."+Type), 'wb')


               f.write(raw_img)
               f.close()
           except Exception as e:
               print ("could not load : "+img)
               print (e)'''
