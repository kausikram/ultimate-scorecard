from flask import Flask, request, render_template, redirect
from models import *


app = Flask(__name__)

@app.before_request
def before_request():
    database.connect()


@app.teardown_request
def after_request(ex):
    database.close()


@app.route('/')
def show_scores():
    """ list all matches here"""
    matches = Match.select().where(True)
    return render_template("list_matches.html",matches=matches, control=False)

@app.route('/control/')
def show_control():
    """ list all matches here"""
    matches = Match.select().where(True)
    return render_template("list_matches.html",matches=matches, control=True)


@app.route('/teams/')
def list_teams():
    """ list all matches here"""
    teams = Team.all()
    return render_template("list_teams.html",teams=teams)


@app.route('/create_team/', methods=['POST', 'GET'])
def create_team():
    if request.method == "GET":
        return render_template("new_team_form.html")
    if request.method == "POST":
        Team.create(team_name = request.form['team_name'])
        return redirect("/teams/")

@app.route('/create_match/', methods=['POST', 'GET'])
def create_match():
    teams = Team.all()
    if request.method == "GET":
        return render_template("new_match_form.html",teams=teams)
    if request.method == "POST":
        if request.form['team_1_id'] == request.form['team_2_id']:
            return redirect("/create_match/")
        t1 = Team.get(Team.id == request.form['team_1_id'])
        t2 = Team.get(Team.id == request.form['team_2_id'])
        m = Match.create_match(t1,t2)
        return redirect("/")


@app.route('/edit_score/<int:match_id>/', methods=['POST', 'GET'])
def enter_score_for_match(match_id):
    match = Match.get(Match.id==match_id)
    mts = [mt for mt in MatchTeam.filter(match__id=match_id)]
    if request.method == "GET":
        return render_template("edit_match_score.html",mts=mts)
    if request.method == "POST":
        for mt in mts:
            mt.score = request.form['{}_score'.format(mt.id)]
            mt.save()
        return redirect("/")

@app.route('/add_spirit_score/<int:mt_id>/', methods=['POST', 'GET'])
def enter_spirit_score_for_team(mt_id):
    mt = MatchTeam.get(MatchTeam.id == mt_id)
    if request.method == "GET":
        return render_template("spirit_form.html",mt=mt)
    if request.method == "POST":
        mt.spirit_score.rules = request.form["rules"]
        mt.spirit_score.fouls = request.form["fouls"]
        mt.spirit_score.fair = request.form["fair"]
        mt.spirit_score.positive = request.form["positive"]
        mt.spirit_score.our_spirit = request.form["our_spirit"]
        mt.spirit_score.save()
        mt.save()
        return redirect("/teams/")


if __name__ == '__main__':
    app.run(debug=True)