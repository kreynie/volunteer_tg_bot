from sqlalchemy import func, Numeric
from src.schemas.rules import AddRuleSchema, RuleSchema, EditRuleSchema
from src.utils.unitofwork import IUnitOfWork


class RulesService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
        self.__rules_list: list[RuleSchema] = list()

    async def add_rule(self, rule: AddRuleSchema) -> str:
        rule = rule.model_dump()
        async with self.uow:
            rule_number = await self.uow.rules.add_one(rule, self.uow.rules.model.rule_number)
            await self.uow.commit()
            return rule_number

    async def edit_rule(self, rule: EditRuleSchema) -> str:
        rule_data = rule.model_dump()
        async with self.uow:
            rule_id = await self.uow.rules.edit_one(
                data=rule_data,
                filter_by={"rule_number": rule.rule_number},
                returning=self.uow.rules.model.rule_number,
            )
            await self.uow.commit()
            return rule_id

    async def delete_rule(self, rule_number: str) -> int:
        async with self.uow:
            returned_rile_number = await self.uow.rules.delete_one(
                returning=self.uow.rules.model.rule_number,
                rule_number=rule_number,
            )
            await self.uow.commit()
            return returned_rile_number

    async def get_rules(self) -> list[RuleSchema]:
        async with self.uow:
            order_by = [func.cast(self.uow.rules.model.rule_number, Numeric(2, 1))]
            rules = await self.uow.rules.find_all(order_by=order_by)
            return rules
