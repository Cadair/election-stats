from app import db

# Please set your GP base.
class Constituency(db.Model):
    __tablename__ = "Constituency"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120)) # Name of the place
    numvotes = db.Column(db.Integer) # Total registered since last full election
    children = db.relationship("Results")

    def __init__(self, name):
        self.name = name


class Results(db.Model):
    __tablename__ = "Results"
    id = db.Column(db.Integer, primary_key=True)
    constituency_id = db.Column(db.Integer, db.ForeignKey('Constituency.id'))
    turnout = db.Column(db.Float(precision=3)) # Percentage turnout
    year = db.Column(db.Date) # Date of this election
    children = db.relationship("Candidates")


class Candidates(db.Model):
    __tablename__ = "Candidates"
    id = db.Column(db.Integer, primary_key=True)
    results_id = db.Column(db.Integer, db.ForeignKey('Results.id'))
    share = db.Column(db.Float(precision=3)) # Share of vote.
    MPname = db.Column(db.String(120)) # Name
    MPparty = db.Column(db.Integer, db.ForeignKey('Party.id')) # Party
    child = db.relationship("Party")
    numvotes = db.Column(db.Integer) # Total numver of votes for this person

    
class Party(db.Model): # To be expanded on later I feel.
    __tablename__ = "Party"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
