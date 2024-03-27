from marshmallow import Schema, fields


class UserSchema(Schema):
    _id = fields.String()
    username = fields.String()
    password = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
