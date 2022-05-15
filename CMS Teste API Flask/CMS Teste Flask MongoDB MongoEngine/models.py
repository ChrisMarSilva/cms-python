import mongoengine as me


class User(me.Document):
    name = me.StringField(required=True)
    email = me.StringField()
    password = me.StringField()

    def to_json(self):
        return {'id': self.pk, 'name': self.name, 'email': self.email, 'password': self.password}


class UserLog(me.Document):
    user = me.ReferenceField(User)
    type = me.StringField()
    date = me.DateTimeField()

    def to_json(self):
        return {'user': self.user.pk, 'type': self.type, 'date': self.date}

