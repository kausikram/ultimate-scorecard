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
        scores = [ s for s in SpiritScore.select().where(SpiritScore.team==self)]
        count = len(scores)
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

        for score in scores:
            for k in total:
                total[k] += getattr(score,k)

        average = {"total":0}
        for k in total:
            average[k] = float(total[k])/count
            average["total"]+=average[k]

        return average

    def __unicode__(self):
        return "<Team :{}>".format(self.team_name)

class Match(BaseModel):
    comments = peewee.TextField(default="")
    team_1 = peewee.ForeignKeyField(Team)
    team_2 = peewee.ForeignKeyField(Team)
    team_1_score = peewee.IntegerField(default=0)
    team_2_score = peewee.IntegerField(default=0)
    team_1_assessed = peewee.BooleanField(default=False)
    team_2_assessed = peewee.BooleanField(default=False)

    @classmethod
    def create_match(cls,t1,t2,comments=""):
        m = cls(team_1 = t1, team_2= t2, comments=comments)
        m.save()

    def get_teams(self):
        return [self.team_1, self.team_2]

    def get_score_string(self):
        return "{} - {}".format(self.team_1_score, self.team_2_score)

    def get_opponent(self, team):
        if self.team_1.id == team.id:
            return self.team_2
        if self.team_2.id == team.id:
            return self.team_1
        raise Exception("Wrong Team")

    def set_ranking_complete(self, team):
        if self.team_1.id == team.id:
            self.team_1_assessed = True
        if self.team_2.id == team.id:
            self.team_2_assessed = True
        self.save()

class SpiritScore(BaseModel):
    team = peewee.ForeignKeyField(Team)
    match = peewee.ForeignKeyField(Match)
    rules = peewee.IntegerField(default=0)
    fouls = peewee.IntegerField(default=0)
    fair = peewee.IntegerField(default=0)
    positive = peewee.IntegerField(default=0)
    our_spirit = peewee.IntegerField(default=0)