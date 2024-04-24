from django import forms

from django_filters_stoex.models import FilterStore

"""
In the template, put this form in it's own form element ( see example below )
"""


class FilterstoreRetrieveForm(forms.Form):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        app_name = kwargs.pop("app_name", None)
        model_name = kwargs.pop("model_name", None)

        super().__init__(*args, **kwargs)

        if request is not None:
            if app_name is None:
                app_name = request.resolver_match.app_name
            self.fields["from_store"].queryset = FilterStore.objects.filter(
                user=request.user, app_name=app_name, model_name=model_name
            ) | FilterStore.objects.filter(
                app_name=app_name, model_name=model_name, all_users=True
            )

    from_store = forms.ModelChoiceField(
        FilterStore.objects.all(), label="Retrieve Saved Filter"
    )
    delete_filterstore = forms.BooleanField(
        label="Delete", initial=False, required=False, help_text="Delete chosen filter"
    )


"""
In the template, put this form within the form element of the filterset form
"""


class FilterstoreSaveForm(forms.Form):

    filterstore_name = forms.CharField(
        label="Save Filter As",
        initial="",
        required=False,
        help_text="The name to save this filter as. Will overytype a filter of the same name",
    )
