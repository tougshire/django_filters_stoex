from django.test import TestCase
from django.db import models

from tougshire_filsor.functions import get_filter_fields
from .models import FilsorTestModelA, FilsorTestModelB

{
    "id": {
        "lookups": [
            ("exact", "is"),
            ("iexact", "is(i)"),
            ("gt", "is greater than"),
            ("gte", "is greater than or equal to"),
            ("lt", "is less than"),
            ("lte", "is less than or equal to"),
            ("in", "is in"),
            ("contains", "contains"),
            ("icontains", "contains(i)"),
            ("startswith", "starts with"),
            ("istartswith", "starts with(i)"),
            ("endswith", "ends with"),
            ("iendswith", "ends with(i)"),
            ("range", "is in range"),
            ("isnull", "is null"),
            ("regex", "matches regex"),
            ("iregex", "matches regex(i)"),
        ]
    },
    "name": {
        "lookups": [
            ("exact", "is"),
            ("iexact", "is(i)"),
            ("gt", "is greater than"),
            ("gte", "is greater than or equal to"),
            ("lt", "is less than"),
            ("lte", "is less than or equal to"),
            ("in", "is in"),
            ("contains", "contains"),
            ("icontains", "contains(i)"),
            ("startswith", "starts with"),
            ("istartswith", "starts with(i)"),
            ("endswith", "ends with"),
            ("iendswith", "ends with(i)"),
            ("range", "is in range"),
            ("isnull", "is null"),
            ("regex", "matches regex"),
            ("iregex", "matches regex(i)"),
        ]
    },
}


class FilsorFuncTestCase(TestCase):
    def setUp(self):
        self.a_first = FilsorTestModelA.objects.create(name="model_a_first")
        self.a_second = FilsorTestModelA.objects.create(name="model_a_second")

        self.b_first = FilsorTestModelB.objects.create(
            name="model_b_first", model_a=FilsorTestModelA.objects.first()
        )

        self.char_lookup = {
            "lookups": [
                ("exact", "is"),
                ("iexact", "is(i)"),
                ("gt", "is greater than"),
                ("gte", "is greater than or equal to"),
                ("lt", "is less than"),
                ("lte", "is less than or equal to"),
                ("in", "is in"),
                ("contains", "contains"),
                ("icontains", "contains(i)"),
                ("startswith", "starts with"),
                ("istartswith", "starts with(i)"),
                ("endswith", "ends with"),
                ("iendswith", "ends with(i)"),
                ("range", "is in range"),
                ("isnull", "is null"),
                ("regex", "matches regex"),
                ("iregex", "matches regex(i)"),
            ]
        }

    def test_testmodel_has_name(self):
        fields = get_filter_fields("tougshire_filsor.FilsorTestModelA")
        self.assertListEqual(["id", "name"], list(fields.keys()))

    def test_testmodel_name_has_char_lookups(self):
        fields = get_filter_fields("tougshire_filsor.FilsorTestModelA")
        self.assertDictEqual(fields["name"], self.char_lookup)

    def test_testmodel_foreignkey_has_choices(self):
        print("*************************")
        print(dir(self.b_first._meta.get_field("model_a")))
        print("******************************")
        print(self.b_first._meta.get_field("model_a").related_model)
