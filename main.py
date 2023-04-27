import sys
import json
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from settings import *

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)


@app.route('/')
def index():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item: item['date'], reverse=True)
    with open('settings.json', encoding='utf8') as config:
        data = config.read()
        settings = json.loads(data)
    return render_template('index.html', posts=posts, bigheader=True, **settings)


@app.route('/posts/<name>/')
def post(name):
    path = f'{POST_DIR}/{name}'
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)


@app.route('/snake')
def snake():
    return render_template('snake.html', post=post)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='127.0.0.1', port=8000, debug=True)
