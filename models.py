class Houses(db.Model):
    id = db.column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    mascot = db.Column(db.String(255), nullable=False)
    founder = db.Column(db.String(255), nullable=False)
    head = db.Column(db.String(255), nullable=False)


class Professors(db.Model):
    id = db.column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    founder = db.Column(db.String(255), nullable=False)
    house_id = Column(db.Integer, db.ForeignKey('houses.id'))

