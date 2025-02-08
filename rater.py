from flask import Flask, render_template, request, redirect, url_for, session
from itertools import combinations
from collections import defaultdict
import random

app = Flask(__name__)
app.secret_key = '5co1vLXMOXL4L15yEmmJMJYR9AbLLqy5'  # Required for using sessions

# Initialize items and global variables
items = ["Louis", "Ben", "Dan", "Alisha", "Zak", "Corin", "Cuish", "Morgan", "Perry", "Sadie", "Leah", "Amy", "Charlie", "Harry", "Sean", "Ruby", "Tanith", "Reece", "Eleanor", "Makoto", "Masami", "Meriel"]
scores = defaultdict(int)
pairs = list(combinations(items, 2))
random.shuffle(pairs)

@app.route('/')
def index():
    if 'pair_index' not in session:
        session['pair_index'] = 0
        session['user_scores'] = defaultdict(int)  # Initialize user scores if it's their first time
    
    pair_index = session['pair_index']
    
    if pair_index < len(pairs):
        item1, item2 = pairs[pair_index]
        return render_template("vote.html", item1=item1, item2=item2)
    else:
        return redirect(url_for("results"))

@app.route('/vote', methods=['POST'])
def vote():
    choice = request.form.get("choice")
    pair_index = session['pair_index']
    item1, item2 = pairs[pair_index]
    
    # Ensure that both items exist in the user_scores dictionary before incrementing
    session['user_scores'].setdefault(item1, 0)
    session['user_scores'].setdefault(item2, 0)
    
    if choice == item1:
        session['user_scores'][item1] += 1
    else:
        session['user_scores'][item2] += 1

    # Move to the next pair
    session['pair_index'] += 1
    
    return redirect(url_for("index"))


@app.route('/results')
def results():
    sorted_items = sorted(items, key=lambda x: scores[x], reverse=True)
    ranked_items = [(rank + 1, item, scores[item]) for rank, item in enumerate(sorted_items)]  # Add rank and score
    return render_template("results.html", ranked_items=ranked_items)


if __name__ == '__main__':
    app.run(debug=True)
