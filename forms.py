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


"""
In the template, put this form within the form element of the filterset form
"""


class CSVOptionForm(forms.Form):

    as_csv = forms.BooleanField(
        label="CSV",
        initial=False,
        required=False,
        help_text="Download the result as a CSV file",
    )


"""
Example:


  <table>
    <form method="POST">
      {% csrf_token %}
      {{ filter.form.as_table }}          <!-- This is the form as it would be with plan django_fitlers  -->
      {{ as_csv.as_table }}               <!-- This is the CSV option form sharing the form element      -->
      {{ filterstore_save.as_table }}     <!-- This is the Save form sharing the form element            -->
      <tr><td> </td><td><input type="submit" /></td></tr>
    </form>
    <form method="GET" action="{% url 'myapp:my-get-saved-filter-view' %}">
      {{ filterstore_retrieve.as_table }} <!-- This is the retrieve form within its own form element     -->
      <tr><td> </td><td><input type="submit" /></td></tr>
    </form>
  </table>


"""
