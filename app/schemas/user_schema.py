from marshmallow import Schema, fields, validate

class UserRegistrationSchema(Schema):
    role = fields.Str(validate=validate.OneOf(["user", "admin"]), dump_default="user")
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone_number = fields.Str(required=False)
    password = fields.Str(required=True, validate=validate.Length(min=6))  # Plain password
    profile_picture = fields.Str(required=False)
    bio = fields.Dict(required=False)
    pictures = fields.List(fields.Str(), required=False)

class UserSchema(Schema):
    id = fields.Str(attribute="_id")  # Serialize ObjectId as string
    role = fields.Str(validate=validate.OneOf(["user", "admin"]), dump_default="user")
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone_number = fields.Str(required=False)
    country = fields.Str(required=False)
    profile_picture = fields.Str(required=False)
    bio = fields.Dict(required=False)
    pictures = fields.List(fields.Str(), required=False)
    is_verified = fields.Bool(default=False)
    subscription_status = fields.Str(validate=validate.OneOf(["active", "inactive", "cancelled", "trial"]), dump_default="inactive")
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)