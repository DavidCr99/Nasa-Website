from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_info = mongo.db.collection.find().limit(3).sort([('_id', 1)])

    # return template and data
    return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scrape():

    # Run scraped functions
    mars = scrape_mars.scrape_mars()

    # Store results into a dictionary
    mars_info = {
            "news_title": mars["news_title"],
            "news_paragraph": mars["news_paragraph"],
            "featured_image_url": mars["featured_image_url"],
            "mars_weather": mars["mars_weather"],
            "mars_facts": mars["mars_facts"],
            "mars_hemispheres": mars["mars_hemispheres"]
    }

    # Insert mars info into database
    mongo.db.collection.insert_one(mars_info)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)






