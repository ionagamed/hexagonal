from sqlalchemy import text

from hexagonal import app, db


class LogEntry(db.Model):
    __tablename__ = 'log_entries'

    id = db.Column(db.Integer, primary_key=True)

    who = db.Column(db.String(256))

    what = db.Column(db.String(256))

    obj = db.Column(db.String(256))

    when = db.Column(db.DateTime(), default=text('NOW()'))

    def __repr__(self):
        return ' '.join([self.who, self.what, self.obj])


def log(who, what, obj):
    db.session.commit()
    entry = LogEntry(
        who=who,
        what=what,
        obj=obj
    )
    db.session.add(entry)
    db.session.commit()
