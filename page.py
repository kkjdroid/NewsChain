from flask import Flask, render_template, request, redirect
from article import article
import json
from markov import markov
import os
app = Flask(__name__)

@app.route('/')
def index(*args):
    articles = []
    try:
        with open('articles.json') as f:
            try:
                articles = [article(_) for _ in json.load(f)]
            except json.decoder.JSONDecodeError:
                os.remove('articles.json')
                return redirect('refresh', code = 303)
    except FileNotFoundError:
        return redirect('refresh', code = 303)
    print(articles)
    return render_template('main.html', lines = articles)

@app.route('/refresh/')
def refresh():
    articles = [article()]
    try:
        with open('articles.json') as f:
            articles += [article(_) for _ in json.load(f)]
    except FileNotFoundError:
        pass
    except json.decoder.JSONDecodeError:
        os.remove('articles.json')
    with open('articles.json', 'w+') as f:
        json.dump([a.__dict__ for a in articles], f)
    return redirect('/', code = 303)

@app.route('/articles/<guid>')
def articles():
    try:
        with open('articles.json') as f:
            articles = [article(_) for _ in json.load(f)]
            for art in articles:
                if(art.guid == guid): 
                    return render_template('article.html', article = art)
    except FileNotFoundError:
        return redirect('refresh', code = 303)
    return redirect('/', code = 303)
    
