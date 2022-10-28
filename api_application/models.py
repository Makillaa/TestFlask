from api_application import app, db


with app.app_context():
    class ResultsModel(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        type = db.Column(db.String(64), nullable=False)
        operator = db.Column(db.String(64), nullable=False)
        datetime = db.Column(db.String(64), nullable=False)
        result = db.Column(db.Integer, nullable=False)

        def __init__(self, type, operator, datetime, result):
            self.type = type
            self.operator = operator
            self.datetime = datetime
            self.result = result

        def __repr__(self):
            return f"{self.type}"

    db.create_all()
