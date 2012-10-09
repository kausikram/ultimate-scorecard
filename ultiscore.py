from flask import Flask
app = Flask(__name__)

@app.route('/')
def show_scores():
    return 'Hello World!'

@app.route('/add_score/')
def add_score_select_match_team():
    return 'Hello World!'

@app.route('/')
def add_score(team_id, match_id):
    return 'Hello World!'

if __name__ == '__main__':
    app.run()