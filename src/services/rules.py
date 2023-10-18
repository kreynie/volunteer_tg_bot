from src.schemas.rules import RuleSchema, EditRuleSchema
from src.utils.unitofwork import IUnitOfWork


class RulesService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
        self.__rules_list: list[RuleSchema] = list()

    async def add_rule(self, rule_text) -> int:
        async with self.uow:
            rule_id = await self.uow.rules.add_one({"text": rule_text})
            await self.uow.commit()
            return rule_id

    async def edit_rule(self, rule: EditRuleSchema) -> int:
        rule_data = rule.model_dump(exclude={"id"})
        async with self.uow:
            rule_id = await self.uow.rules.edit_one(filter_by_id=rule.id, data=rule_data)
            await self.uow.commit()
            return rule_id

    async def get_rules(self) -> list[RuleSchema]:
        async with self.uow:
            rules = await self.uow.rules.find_all()
            return rules
