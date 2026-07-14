from django_filters import (
    Filter, DateRangeFilter, OrderingFilter, BooleanFilter
)
from django_filters.widgets import BooleanWidget
from django_filters.filters import _truncate
from django_filters.constants import EMPTY_VALUES
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class AltBooleanWidget(BooleanWidget):

    def __init__(self, attrs=None):
        choices = (("", _("Any")), ("true", _("Yes")) ,("false", _("No")))
        super(BooleanWidget, self).__init__(attrs, choices)

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

class BlankNullFilter(BooleanFilter):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", AltBooleanWidget)

        super(BooleanFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        lookup_exact = '%s__exact' % (self.field_name)
        lookup_gt = '%s__gt' % (self.field_name)
        lookup_null = '%s__isnull' % (self.field_name)
        if value is True:
            Qcombined = (
                Q(**{lookup_exact: ''}) | Q(**{lookup_null: True})
            )
            return self.get_method(qs)(Qcombined)
        if value is False:
            Qcombined = (
                Q(**{lookup_gt: ''}) & Q(**{lookup_null: False})
            )
            return self.get_method(qs)(Qcombined)
        return qs

class BlankFilter(BooleanFilter):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", AltBooleanWidget)

        super(BooleanFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        lookup_exact = '%s__exact' % (self.field_name)
        lookup_gt = '%s__gt' % (self.field_name)
        if value is True:
            Qfilter = (
                Q(**{lookup_exact: ''})
            )
            return self.get_method(qs)(Qfilter)
        if value is False:
            Qfilter = (
                Q(**{lookup_gt: ''})
            )
            return self.get_method(qs)(Qfilter)
        return qs
class NullFilter(BooleanFilter):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", AltBooleanWidget)

        super(BooleanFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        lookup_null = '%s__isnull' % (self.field_name)
        if value is True:
            Qfilter = (
                Q(**{lookup_null: True})
            )
            return self.get_method(qs)(Qfilter)
        if value is False:
            Qfilter = (
                Q(**{lookup_null: False})
            )
            return self.get_method(qs)(Qfilter)
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

