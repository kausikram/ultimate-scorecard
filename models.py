import peewee


import peewee

database = peewee.SqliteDatabase('data.db')

class BaseModel(peewee.Model):
    class Meta:
        database = database

class Team(BaseModel):
    team_name = peewee.TextField()

    @classmethod
    def all(cls):
        return [t for t in cls.select().where(True)]

    def get_average_spirit_scores(self):
        mts = MatchTeam.get_played_matches(team=self)
        count = len(mts)
        total = {
            "rules" : 0,
            "fouls" : 0,
            "fair" : 0,
            "positive" : 0,
            "our_spirit" : 0,
        }
        if count == 0:
            total["total"] = 0
            return total

        for mt in mts:
            for k in total:
                total[k] += getattr(mt.spirit_score,k)

        average = {"total":0}
        for k in total:
            average[k] = float(total[k])/count
            average["total"]+=average[k]

        return average

    def __unicode__(self):
        return "<Team :{}>".format(self.team_name)

class Match(BaseModel):
    comments = peewee.TextField(default="")

    @classmethod
    def create_match(cls,t1,t2,comments=""):
        m = cls(comments=comments)
        m.save()
        mt1 = MatchTeam.create_match_team(m, t1)
        mt2 = MatchTeam.create_match_team(m, t2)

    def get_matchteams(self):
        return [mt for mt in self.matchteam_set]

    def get_teams(self):
        return [mt.team for mt in self.get_matchteams()]

    def get_score_string(self):
        mts = self.get_matchteams()
        return "{} - {}".format(mts[0].score, mts[1].score)

class SpiritScore(BaseModel):
    rules = peewee.IntegerField(default=0)
    fouls = peewee.IntegerField(default=0)
    fair = peewee.IntegerField(default=0)
    positive = peewee.IntegerField(default=0)
    our_spirit = peewee.IntegerField(default=0)


class MatchTeam(BaseModel):
    match = peewee.ForeignKeyField(Match)
    team = peewee.ForeignKeyField(Team)
    score = peewee.IntegerField(default=0)
    spirit_score = peewee.ForeignKeyField(SpiritScore)

    def get_opponent_mt(self):
        mts = self.match.get_matchteams()
        for mt in mts:
            if mt.id != self.id:
                return mt

    def get_opponent(self):
        return self.get_opponent_mt().team

    @classmethod
    def get_played_matches(cls, team):
        all_mts = cls.filter(team = team)
        played_matches = []
        for mt in all_mts:
            if mt.score == 0 and mt.get_opponent_mt().score == 0:
                pass
            else:
                played_matches.append(mt)
        return played_matches

    @classmethod
    def create_match_team(cls, match, team):
        spirit_score = SpiritScore()
        spirit_score.save()
        cm = cls(match=match, team=team, spirit_score=spirit_score)
        cm.save()
        return cm