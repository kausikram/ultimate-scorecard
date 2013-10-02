from flask import Flask, request, render_template, redirect
from models import *

app = Flask(__name__)
app.config.from_object('settings')

@app.before_request
def before_request():
    database.connect()


@app.teardown_request
def after_request(ex):
    database.close()


@app.route('/')
def show_scores():
    matches = Match.select().where(True)
    return render_template("list_matches.html",matches=matches, control=False)

@app.route('/control/')
def show_control():
    matches = Match.select().where(True)
    return render_template("list_matches.html",matches=matches, control=True)


@app.route('/control/mvps/')
def show_team_mvps():
    teams = Team.all()
    return render_template("team_list_mvps.html", teams=teams)

@app.route('/control/mvps/<int:team_id>/')
def show_control_mvps(team_id):
    team = Team.get(Team.id == team_id)
    matches = Match.list_matches_for_team(team)
    return render_template("show_mvp_matches.html",matches=matches, team=team)

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
        return redirect("/control/")

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
        return redirect("/control/")


@app.route('/edit_score/<int:match_id>/', methods=['POST', 'GET'])
def enter_score_for_match(match_id):
    match = Match.get(Match.id==match_id)
    if request.method == "GET":
        return render_template("edit_match_score.html",match=match)
    if request.method == "POST":
        match.team_1_score = request.form['team_1_score']
        match.team_2_score = request.form['team_2_score']
        match.save()
        return redirect("/control/")

@app.route('/add_spirit_score/<int:match_id>/team/<int:team_id>/', methods=['POST', 'GET'])
def enter_spirit_score_for_team(match_id, team_id):
    match = Match.get(Match.id == match_id)
    team = Team.get(Team.id == team_id)
    opponent = match.get_opponent(team)

    if request.method == "GET":
        return render_template("spirit_form.html", match=match, team=team, opponent=opponent)

    if request.method == "POST":
        spirit_score = SpiritScore()
        spirit_score.team = team
        spirit_score.match = match
        spirit_score.rules = request.form["rules"]
        spirit_score.fouls = request.form["fouls"]
        spirit_score.fair = request.form["fair"]
        spirit_score.positive = request.form["positive"]
        spirit_score.our_spirit = request.form["our_spirit"]
        if app.config["ULTISCORE_SHOULD_COLLECT_MVP_NAMES"]:
            spirit_score.mvp_male_list = ""
            for i in range(1,app.config["ULTISCORE_NUMBER_OF_MALE_MVP_NAMES"]+1):
                spirit_score.mvp_male_list +="|"
                spirit_score.mvp_male_list += request.form["mvp_male_choice_{}".format(i)]

            spirit_score.mvp_female_list = ""
            for i in range(1,app.config["ULTISCORE_NUMBER_OF_FEMALE_MVP_NAMES"]+1):
                spirit_score.mvp_female_list +="|"
                spirit_score.mvp_female_list += request.form["mvp_female_choice_{}".format(i)]
        spirit_score.save()

        match.set_ranking_complete(team)
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')