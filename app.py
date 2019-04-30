from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    scraped_data = mongo.db.collection.find_one()

    # Assign all variables from returned dictionary
    first_article_title = scraped_data.get("first_article_title")
    first_article_teaser = scraped_data.get("first_article_teaser")
    featured_image_url = scraped_data.get("featured_image_url")
    mars_weather = scraped_data.get("mars_weather")
    mars_table = scraped_data.get("mars_table")
    hemisphere_image_urls = scraped_data.get("hemisphere_image_urls")

    # Return template and data
    return render_template("index.html", first_article_title=first_article_title, first_article_teaser=first_article_teaser, featured_image_url=featured_image_url, mars_weather=mars_weather, hemisphere_image_urls=hemisphere_image_urls)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
