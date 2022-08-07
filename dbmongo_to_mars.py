# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# create flask app instance
app = Flask(__name__)

# create mongo app instance
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scraper")

# create route
@app.route("/")
def home():

    # find one entry in mongodb
    mars_info = mongo.db.mars_info.find_one()

    # render template
    return render_template("index.html", mars_dict=mars_info)



# create scrape route
@app.route("/scrape")
def data_scrape():

    # import
    import scrape_mars

    # connect
    mars_info = mongo.db.mars_info

    # save scrape dict from scrape file
    mars_data = scrape_mars.scrape()

    # update database
    mars_info.update({}, mars_data, upsert=True)

    # redirect to home page
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug=False)
