from django.db.models import Case, When, Expression, F

class ConditionalExpression(Expression):
    def __init__(self, condition_field, when_true, when_false, output_field):
        super().__init__(output_field=output_field)
        self.condition_field = condition_field
        self.when_true = when_true
        self.when_false = when_false

    def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False):
        condition = F(self.condition_field)
        case = Case(
            When(
                **{self.condition_field: True},
                then=self.when_true
            ),
            default=self.when_false,
            output_field=self.output_field
        )
        return case.resolve_expression(query, allow_joins, reuse, summarize, for_save)