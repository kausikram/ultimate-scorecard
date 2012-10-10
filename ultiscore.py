from flask import Flask
app = Flask(__name__)

@app.route('/')
def show_scores():
    """ list all matches here"""
    return 'Hello World!'

@app.route('/create_team/')
def create_team():
    return 'Hello World!'

@app.route('/create_match/')
def create_match():
    return 'Hello World!'

@app.route('/list_spirit_scores/')
def enter_score_for_match():
    return 'Hello World!'

@app.route('/add_spirit_score/<match_id>/<team_id>/')
def enter_spirit_score_for_team(team_id, match_id):
    return 'Hello World!'

if __name__ == '__main__':
    app.run()