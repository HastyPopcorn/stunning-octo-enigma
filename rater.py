from flask import Flask, render_template, request, redirect, url_for, session
from itertools import combinations
from collections import defaultdict
import random

app = Flask(__name__)
app.secret_key = '5co1vLXMOXL4L15yEmmJMJYR9AbLLqy5'  # Required for using sessions

# Initialize items and global variables
#items = ["Louis", "Ben", "Dan", "Alisha", "Zak", "Corin", "Cuish", "Morgan", "Perry", "Sadie", "Leah", "Amy", "Charlie", "Harry", "Sean", "Ruby", "Tanith", "Reece", "Eleanor", "Makoto", "Masami", "Meriel"]
items = ["Louis", "Ben", "Dan"]
scores = defaultdict(int)
pairs = list(combinations(items, 2))
random.shuffle(pairs)

@app.route('/')
def index():
    global pair_index
    if pair_index < len(pairs):  # Only show the voting page if there are pairs left
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
    global pair_index
    pair_index = 0  # Reset the index when results are shown
    sorted_items = sorted(items, key=lambda x: scores[x], reverse=True)
    return render_template("results.html", results=sorted_items, scores=scores)



if __name__ == '__main__':
    app.run(debug=True)
