from forms import SearchForm
from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo 


client = pymongo.MongoClient('mongodb://rina:up5O6LEMOlJlbedD@ac-pvajawv-shard-00-00.simkoz8.mongodb.net:27017,ac-pvajawv-shard-00-01.simkoz8.mongodb.net:27017,ac-pvajawv-shard-00-02.simkoz8.mongodb.net:27017/?ssl=true&replicaSet=atlas-83ia8w-shard-0&authSource=admin&retryWrites=true&w=majority', serverSelectionTimeoutMS = 5000)
db = client.database



app = Flask(name)
app.config['SECRET_KEY']='\xde\xcd\x0b\x85\xd7\x11O1)\x16\xd5\x1b\xd1y\x80\x9f\xa7\xd1w9\xe5\x95\xd6\xba'


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
