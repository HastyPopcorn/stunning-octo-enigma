from flask import Flask, render_template, request, redirect, url_for
from itertools import combinations
from collections import defaultdict
import random

app = Flask(__name__)

items = ["Louis", "Ben", "Dan", "Alisha", "Zak", "Corin", "Cuish", "Morgan", "Perry", "Sadie", "Leah", "Amy", "Charlie", "Harry", "Sean", "Ruby", "Tanith", "Reece", "Eleanor", "Makoto", "Masami", "Meriel"]


scores = defaultdict(int)
pairs = list(combinations(items, 2))
random.shuffle(pairs)
pair_index = 0

@app.route('/')
def index():
    global pair_index
    if pair_index < len(pairs):
        item1, item2 = pairs[pair_index]
        return render_template("vote.html", item1=item1, item2=item2)
    else:
        return redirect(url_for("results"))

@app.route('/vote', methods=['POST'])
def vote():
    global pair_index
    choice = request.form.get("choice")
    item1, item2 = pairs[pair_index]
    if choice == item1:
        scores[item1] += 1
    else:
        scores[item2] += 1
    
    pair_index += 1
    return redirect(url_for("index"))

@app.route('/results')
def results():
    sorted_items = sorted(items, key=lambda x: scores[x], reverse=True)
    return render_template("results.html", results=sorted_items, scores=scores)

if __name__ == '__main__':
    app.run(debug=True)
