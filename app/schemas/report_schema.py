from marshmallow import Schema, fields, validate

class ReportSchema(Schema):
    user_id = fields.Str(required=True)
    diet_plan = fields.Dict(required=False)
    skincare_routine = fields.Dict(required=False)
    beauty_assessment = fields.Dict(required=False)
    images = fields.List(fields.Str(), required=False)
    version = fields.Int(required=False)
    status = fields.Str(validate=validate.OneOf(["Draft", "Published", "Archived"]), dump_default="Draft")
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)