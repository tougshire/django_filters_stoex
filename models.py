from django.db import models
from django.conf import settings


class FilterStore(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        "name", max_length=200, help_text="The name of this stored filter object"
    )
    app_name = models.CharField(
        "app",
        max_length=20,
    )
    model_name = models.CharField(
        "model",
        max_length=20,
    )
    data = models.TextField("data")

    last_used = models.DateTimeField("last used", auto_now=True)

    def get_name(self):
        return self.name if self.name else "-"

    def __str__(self):

        return "{}:{}".format(self.get_name(), self.last_used.strftime("%Y-%m-%d"))

    class Meta:
        ordering = ("-last_used",)
