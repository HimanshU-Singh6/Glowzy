from marshmallow import Schema, fields, validate

class SubscriptionSchema(Schema):
    user_id = fields.Str(required=True)
    status = fields.Str(validate=validate.OneOf(["active", "inactive", "canceled", "trial"]), required=True)
    plan = fields.Str(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=False)
    payment_method = fields.Str(required=True)
    transaction_history = fields.List(fields.Dict(), required=False)
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)