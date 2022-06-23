from forms import SearchForm
from flask import Flask, render_template, request, redirect, url_for, flash
import pymongo


client = pymongo.MongoClient('mongodb://127.0.0.1', serverSelectionTimeoutMS = 5000)
db = client.db.results


app = Flask(__name__)
app.config['SECRET_KEY']='THE SECRET KEY'


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
        questions = list(db.find({"$text": {"$search": searched}}))      
    
    return render_template("results.html", form=form, questions=questions, searched=searched)



if __name__ == '__main__':
    app.run(debug= True)
