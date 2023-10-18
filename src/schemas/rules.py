from .base import BaseSchema


class RuleSchema(BaseSchema):
    text: str


EditRuleSchema = RuleSchema
