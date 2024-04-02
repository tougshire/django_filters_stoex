from django_filters import FilterSet


class StoexFilterSet(FilterSet):

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset)
        if not self.is_bound:
            for filter in self.filters.values():
                if "initial" in filter.extra:
                    self.queryset = filter.filter(
                        self.queryset, filter.extra["initial"]
                    )
