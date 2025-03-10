from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    role = fields.Str(validate=validate.OneOf(["user", "admin"]), default="user")
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone_number = fields.Str(required=False)
    password_hash = fields.Str(required=True)
    profile_picture = fields.Str(required=False)
    bio = fields.Dict(required=False)
    pictures = fields.List(fields.Str(), required=False)
    is_verified = fields.Bool(default=False)
    subscription_status = fields.Str(validate=validate.OneOf(["active", "inactive", "cancelled", "trial"]), default="inactive")
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)