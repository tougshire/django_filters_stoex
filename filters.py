from django_filters import Filter
from django_filters.constants import EMPTY_VALUES
from django.db.models import Q


class CrossFieldSearchFilter(Filter):
    def __init__(
        self,
        field_name=None,
        lookup_expr=None,
        *,
        label=None,
        method=None,
        distinct=False,
        exclude=False,
        **kwargs
    ):
        super().__init__(
            field_name,
            lookup_expr,
            label=label,
            method=method,
            distinct=distinct,
            exclude=exclude,
            **kwargs
        )
        self.field_names = field_name.split(",")

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        Qcombined = None
        for field_name in self.field_names:
            lookup = "%s__%s" % (field_name, self.lookup_expr)
            Qcombined = (
                Q(**{lookup: value})
                if Qcombined is None
                else Qcombined | Q(**{lookup: value})
            )

        qs = self.get_method(qs)(Qcombined)
        if self.distinct:
            qs = qs.distinct()
        return qs
