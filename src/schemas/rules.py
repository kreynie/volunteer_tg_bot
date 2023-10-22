from pydantic import BaseModel
from .base import BaseSchema


class AddRuleSchema(BaseModel):
    rule_number: str
    text: str


class RuleSchema(BaseSchema, AddRuleSchema):
    rule_number: str
    text: str


EditRuleSchema = AddRuleSchema
