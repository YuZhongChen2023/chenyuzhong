import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template,request
from datetime import datetime

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>陳昱中Python網頁12/01</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?johnson=陳昱中>傳送使用者暱稱</a><br>"
    homepage += "<a href=/about>簡介網頁</a><br>"
    homepage += "<a href=/account>網頁表單輸入帳密傳值</a><br><br>"
    homepage += "<a href=/wave>人選之人演員名單(按年齡由小到大)</a><br>"
    homepage += "<a href=/books>圖書館書本精選</a><br>"
    homepage += "<a href=/search>圖書查詢</a><br>"
    homepage += "<a href=/spider>網路爬蟲擷取課程資料</a><br>"
    return homepage

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html", datetime = str(now))

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("johnson")
    return render_template("welcome.html", name=user)

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/wave")
def read():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("人選之人─造浪者")    
    docs = collection_ref.get()    
    for doc in docs:         
        Result += "文件內容：{}".format(doc.to_dict()) + "<br>"    
    return Result

@app.route("/books")
def books():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("圖書精選")
    docs = collection_ref.order_by("anniversary").get()
    for doc in docs:
        bk = doc.to_dict()
        Result += "書名:" + bk["title"] + "<br>"
        Result += "作者:" + bk["author"] + "<br>"
        Result += str(bk["anniversary"]) + "週年紀念版" + "<br>"
        Result += "<img src=" + bk["cover"] +"></img><br><br>"
    return Result

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        keyword = request.form["keyword"]
        Result = "您輸入的關鍵字是：" + keyword
        db = firestore.client()
        collection_ref = db.collection("圖書精選")
        docs = collection_ref.order_by("anniversary").get()
        for doc in docs:
            bk = doc.to_dict()
            if keyword in bk["title"]:
                Result += "書名:<a href="  + bk["url"] + ">" + bk["title"] + "<br>"
                Result += "作者:" + bk["author"] + "<br>"
                Result += str(bk["anniversary"]) + "週年紀念版" + "<br>"
                Result += "<img src=" + bk["cover"] +"></img><br><br>"
        return Result
    else:
        return render_template("searchbk.html")

@app.route("/spider")
def spider():
    info = ""
    
    url = "https://www1.pu.edu.tw/~tcyang/course.html"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    #print(Data.text)
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".team-box")

    for x in result:
        info += "<a href=" + x.find("a").get("href") + ">" + x.find("h4").text + "</a><br>"
        info += x.find("p").text + "</a><br>"
        info += x.find("a").get("href") + "</a><br>"
        info += "<img src=https://www1.pu.edu.tw/~tcyang/" + x.find("img").get("src") + " width=200 height=300></img>+</br>"
    return info

if __name__ == "__main__":
    app.debug = True
    app.run()
    
