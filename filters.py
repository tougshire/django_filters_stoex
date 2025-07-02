from django_filters import Filter, DateRangeFilter, OrderingFilter
from django_filters.filters import _truncate
from django_filters.constants import EMPTY_VALUES
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


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
        self.field_names = [name.strip() for name in field_name.split(",")]

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


class ChainableOrderingFilter(OrderingFilter):

    def filter(self, qs, value):
        initial_ordering = qs.query.order_by
        qs = super().filter(qs, value)

        return super().filter(qs, value).order_by(*initial_ordering, *qs.query.order_by)

class ExpandedDateRangeFilter(DateRangeFilter):
    choices = DateRangeFilter.choices + [
        ("aftertoday", _("After Today")),
        ("beforetoday", _("Before Today")),
        ("todayorafter", _("Today or After")),
        ("todayorbefore", _("Today or Before")),

    ]

    filters = DateRangeFilter.filters
    filters.update({
        "aftertoday": lambda qs, name: qs.filter(
            **{
                "%s__gt" % name: _truncate(now()),
            }
        ),
        "todayorafter": lambda qs, name: qs.filter(
            **{
                "%s__gte" % name: _truncate(now()),
            }
        ),
        "beforetoday": lambda qs, name: qs.filter(
            **{
                "%s__lt" % name: _truncate(now()),
            }
        ),
        "todayorbefore": lambda qs, name: qs.filter(
            **{
                "%s__lte" % name: _truncate(now()),
            }
        ),
    })

