from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
# mongo = PyMongo(app)

# Or set inline
client = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")


# clear all existing data out of the collection.
# For demo purposes only, 
# you may not want to do this for an app you're building!
# mongo.db.listings.drop()

@app.route("/")
def index():
    mars = client.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = client.db.mars
    mars_data = scrape_mars.scrape()
    print(mars_data)
    mars.update({}, mars_data, upsert = True)
    return "Did that work???"


if __name__ == "__main__":
    app.run(debug=True)
