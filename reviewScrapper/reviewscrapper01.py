from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)
fname = None


@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return render_template('indexrs01.html')


@app.route('/show_details', methods=['POST', 'GET'])
@cross_origin()
def show_details():
    # global fname
    print(request.method)
    searchString = request.form['pname']  # request.args.get('pname')
    print('searchString', searchString)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    # return render_template('detailsrs01.html', searchString=searchString)
    if request.method == 'POST':
        try:
            # searchString = request.form['content'].replace(" ", "")
            searchString = request.form['pname'].replace(" ", "")
            print('searchString', searchString)
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "bhgxx2 col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink, headers=headers)
            prodRes.encoding = 'utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            # print(prod_html)
            commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})
            reviews = []
            # fname = searchString+'.txt'
            # with open(fname, 'w', encoding="utf-8") as fw:
            for commentbox in commentboxes:
                try:
                    # name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all(
                        'p', {'class': '_3LYOAd _3sxSiS'})[0].text

                except:
                    name = 'No Name'

                try:
                    # rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text

                except:
                    rating = 'No Rating'

                try:
                    # commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    # comtag = commentbox.div.div.find_all('div', {'class': ''})
                    comtag = commentbox.div.div.find('div', {'class': 'qwjRop'})

                    # custComment.encode(encoding='utf-8')
                    # custComment = comtag[0].div.text
                    custComment = comtag.div.div.text
                except Exception as e:
                    print(custComment)
                    # print("Exception while creating dictionary: ", e)
                    custComment = 'No Customer Comment'

                # review = searchString+','+name + ',' + rating + ',' + commentHead+',' + custComment
                # fw.write(review)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
            return render_template('detailsrs01.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ', e)
            return render_template("404.html")

    else:
        return render_template('indexrs01.html')


@app.errorhandler(404)
@cross_origin()
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/return-files/')
@cross_origin()
def return_files_tut(fname):
    try:
        print(fname)
        return send_file('fname', attachment_filename=fname)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
