from app import db


class Base(db.Model):
    __abstract__ = True

    def to_dict(self):
        rv = dict()
        for c in self.__table__.columns:
            rv[c.name] = getattr(self, c.name)
        return rv

    @classmethod
    def generate_dummy(cls, **kwargs):
        d = cls(**kwargs)
        db.session.add(d)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception


class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(20), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def __repr__(self):
        return '<Post {}>'.format(self.title)


class Comment(Base):
    __tablename__ = 'comments'
    __table_args__ = (db.UniqueConstraint('user_id', 'text', name='unique_idx_user_id_text'), )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    text = db.Column(db.String(160))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def __repr__(self):
        return '<Comment {}>'.format(self.text)
