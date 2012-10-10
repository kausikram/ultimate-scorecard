import peewee


import peewee

database = peewee.SqliteDatabase('data.db')

class BaseModel(peewee.Model):
    class Meta:
        database = database

class Team(BaseModel):
    team_name = peewee.TextField()

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

    @classmethod
    def create_match_team(cls, match, team):
        spirit_score = SpiritScore()
        spirit_score.save()
        cm = cls(match=match, team=team, spirit_score=spirit_score)
        cm.save()
        return cm