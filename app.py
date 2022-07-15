from forms import SearchForm
from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo 


client = pymongo.MongoClient('mongodb://127.0.0', serverSelectionTimeoutMS = 5000)
db = client.database



app = Flask(name)
app.config['SECRET_KEY']='0000'


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@app.route('/results', methods=["POST"])
def results():
    form = SearchForm()
    if form.validate_on_submit():
        searched = request.form['searched']
        output =(db.data.find({'$text': {'$search': searched}}))

    return render_template("results.html", form=form,searched=searched, output=output)


if name == 'main':
   app.run(debug= True)
