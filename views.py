import csv
from django.core.exceptions import ImproperlyConfigured, MultipleObjectsReturned
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.urls import reverse
from django.views.generic import View
from django.views.generic.list import (
    MultipleObjectMixin,
    MultipleObjectTemplateResponseMixin,
)

from django_filters.constants import ALL_FIELDS
from django_filters.filterset import filterset_factory
from django_filters.views import FilterMixin

from .forms import CSVOptionForm, FilterstoreRetrieveForm, FilterstoreSaveForm
from .models import FilterStore
from urllib.parse import urlencode
from django.template import loader


class FilterStoexMixin(FilterMixin):
    """
    A mixin that provides a way to show and handle a FilterSet in a request.


    """

    filterset_class = None
    filterset_fields = ALL_FIELDS
    strict = True

    def get_filterset(self, filterset_class, from_store=None):
        """
        Returns an instance of the filterset to be used in this view.
        """
        kwargs = self.get_filterset_kwargs(filterset_class, from_store)
        return filterset_class(**kwargs)

    def get_filterset_kwargs(self, filterset_class, from_store=None):
        """
        Returns the keyword arguments for instantiating the filterset.
        """
        data = None
        if from_store is not None:
            try:
                filterstore = FilterStore.objects.get(pk=from_store)
                data = QueryDict(filterstore.data)
            except Exception as e:
                raise e
        elif self.request.POST:
            data = self.request.POST
        else:
            try:
                filterstore = FilterStore.objects.filter(user=self.request.user).first()
                data = QueryDict(filterstore.data)
            except Exception as e:
                data = None

        kwargs = {
            "data": data,
            "request": self.request,
        }
        try:
            kwargs.update(
                {
                    "queryset": self.get_queryset(),
                }
            )
        except ImproperlyConfigured:
            # ignore the error here if the filterset has a model defined
            # to acquire a queryset from
            if filterset_class._meta.model is None:
                msg = (
                    "'%s' does not define a 'model' and the view '%s' does "
                    "not return a valid queryset from 'get_queryset'.  You "
                    "must fix one of them."
                )
                args = (filterset_class.__name__, self.__class__.__name__)
                raise ImproperlyConfigured(msg % args)
        return kwargs

    def get_strict(self):
        return self.strict


class BaseFilterView(FilterStoexMixin, MultipleObjectMixin, View):
    def get(self, request, *args, **kwargs):

        if request.GET.get("from_store"):
            return HttpResponseRedirect(
                reverse(self.filterstore_urlname, args=request.GET.get("from_store"))
            )

        filterset_class = self.get_filterset_class()

        from_store = kwargs.get("from_store")
        if from_store:
            self.filterset = self.get_filterset(filterset_class, from_store)
            self.object_list = self.filterset.qs

        else:
            self.filterset = self.get_filterset(filterset_class)
            self.object_list = self.filterset.queryset.none()

        context = self.get_context_data(
            filter=self.filterset, object_list=self.object_list
        )

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        filterset_class = self.get_filterset_class()
        self.filterset = self.get_filterset(filterset_class)

        if (
            not self.filterset.is_bound
            or self.filterset.is_valid()
            or not self.get_strict()
        ):
            self.object_list = self.filterset.qs
        else:
            self.object_list = self.filterset.queryset.none()

        context = self.get_context_data(
            filter=self.filterset, object_list=self.object_list
        )

        if self.request.user.is_authenticated:
            self.save_filterset(request)

        if request.POST.get("csv"):
            return self.render_csv()

        return self.render_to_response(context)

    def save_filterset(self, request):

        filterstore_save_form = FilterstoreSaveForm(request.POST)

        if request.user.is_authenticated and filterstore_save_form.is_valid():
            filterstore_name = (
                filterstore_save_form["filterstore_name"].value()
                if filterstore_save_form["filterstore_name"].value() is not None
                else ""
            )

            try:
                filterstore, created = FilterStore.objects.get_or_create(
                    user=self.request.user,
                    model_name=self.filterset.queryset.model.__name__.lower(),
                    app_name=self.filterset.queryset.model._meta.app_label,
                    name=filterstore_name,
                )
            except MultipleObjectsReturned:
                filterstore = FilterStore.objects.filter(
                    user=self.request.user,
                    model_name=self.filterset.queryset.model.__name__.lower(),
                    app_name=self.filterset.queryset.model._meta.app_label,
                    name=filterstore_name,
                ).latest("last_used")

            data_string = ""

            for filter in self.filterset.filters:
                for value in request.POST.getlist(filter):
                    data_string = data_string + urlencode({filter: value}) + "&"

            filterstore.data = data_string

            filterstore.save()

    def render_csv(self):
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="people.csv"'},
        )
        writer = csv.writer(response)
        data = []
        if hasattr(self.filterset.Meta, "csv_fields"):
            for object in self.object_list:
                row = []
                for field in self.filterset.Meta.csv_fields:
                    try:
                        row.append(getattr(object, field))
                    except Exception as e:
                        pass
                writer.writerow(row)
        else:
            for object in self.object_list:
                row = [object]
                writer.writerow(row)
        return response


class FilterView(MultipleObjectTemplateResponseMixin, BaseFilterView):
    """
    Render some list of objects with filter, set by `self.model` or
    `self.queryset`.
    `self.queryset` can actually be any iterable of items, not just a queryset.
    """

    template_name_suffix = "_filter"

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        # this is a fallback but it's better to define an instance of FilterstoreRetrieveForm
        # in get_context_manager of the calling view and passing keywords request, app_name, and model_name
        # example:
        # context_data["filterstore_retrieve"] = FilterstoreRetrieveForm(
        #     request=self.request, app_name="your_app_name", model_name="your_model_name"
        # )
        context_data["filterstore_retrieve"] = FilterstoreRetrieveForm(
            request=self.request
        )
        context_data["filterstore_save"] = FilterstoreSaveForm()
        context_data["as_csv"] = CSVOptionForm()

        return context_data
