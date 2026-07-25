from database import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))

    photo = db.Column(db.String(200))
    video = db.Column(db.String(200))


    def __repr__(self):
        return f"<User {self.name}>"