from django.core.management.base import BaseCommand
from django.db.models import Count
from prettytable import PrettyTable
from WGForge.cats.models import CatColorsInfo, Cats


class Command(BaseCommand):
    help = "Show and save cat colors statistic"

    def handle(self, *args, **kwargs):
        self.cats_with_color = (
            Cats.objects.values("color")
            .annotate(dcount=Count("color"))
            .order_by("color")
        )
        self.show_result()
        self.save_result()

    def show_result(self):
        cat_color_stat_table = PrettyTable()
        cat_color_stat_table.field_names = [
            "color",
            "count",
        ]
        for cat_with_color in self.cats_with_color:
            cat_color_stat_table.add_row(
                [cat_with_color["color"], cat_with_color["dcount"]]
            )
        print(cat_color_stat_table)

    def save_result(self):
        CatColorsInfo.objects.all().delete()
        for cat_with_color in self.cats_with_color:
            CatColorsInfo.objects.create(
                color=cat_with_color["color"], count=cat_with_color["dcount"]
            )
