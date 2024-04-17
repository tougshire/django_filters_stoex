from django_filters import FilterSet


class StoexFilterSet(FilterSet):

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        if not self.is_bound:
            for filter in self.filters.values():
                if "initial" in filter.extra:
                    self.queryset = filter.filter(
                        self.queryset, filter.extra["initial"]
                    )
