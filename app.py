from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# @TODO: setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# @TODO: connect to mongo db and collection
# client = pymongo.MongoClient(conn)
# db = client.mars_db

@app.route("/")
def home():
    news = mongo.db.news.find_one()
    featured_image_url = mongo.db.featured_image_url.find_one()
    mars_weather = mongo.db.mars_weather.find_one()
    mars_info = mongo.db.mars_info.find_one()
    mars_hemispheres = mongo.db.mars_hemispheres.find()
    return render_template("index.html", news=news, featured_image_url=featured_image_url, mars_weather=mars_weather, mars_info=mars_info, mars_hemispheres=mars_hemispheres)

@app.route("/scrape")
def scrape():
    scrape_mars.scrape()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)