from django.db import models
from django.conf import settings


class FilterStore(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    all_users = models.BooleanField(
        "all users",
        default=False,
        help_text="If this search should appear in every user's list of saved searches",
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

    stick_to = models.IntegerField(
        "stick to",
        choices=[(0, "Neither"), (1, "Top"), (-1, "Bottom")],
        default=0,
        help_text="Whether to stick to the top or bottom, or none",
    )
    last_used = models.DateTimeField("last used", auto_now=True)

    def get_name(self):
        return self.name if self.name else "-"

    def __str__(self):

        return "{}:{}".format(self.get_name(), self.last_used.strftime("%Y-%m-%d"))

    class Meta:
        ordering = (
            "-stick_to",
            "-last_used",
        )
