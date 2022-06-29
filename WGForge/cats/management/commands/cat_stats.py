from django.core.management.base import BaseCommand
from django.db.models import Count, Avg
from prettytable import PrettyTable
from WGForge.cats.models import CatsStat, Cats


class Command(BaseCommand):
    help = "Show and save cat length statistics"

    def handle(self, *args, **kwargs):
        result = {}
        cats = Cats.objects.all()
        result["tail_length_mean"] = self.count_mean_value(cats, "tail_length")
        result["tail_length_median"] = self.count_median_value(
            cats, "tail_length"
        )
        result["tail_length_mode"] = self.count_moda_value(cats, "tail_length")
        result["whiskers_length_mean"] = self.count_mean_value(
            cats, "whiskers_length"
        )
        result["whiskers_length_median"] = self.count_median_value(
            cats, "whiskers_length"
        )
        result["whiskers_length_mode"] = self.count_moda_value(
            cats, "whiskers_length"
        )
        self.save_result(result)
        self.show_result(result)

    def count_mean_value(self, qs, item):
        return qs.aggregate(Avg(item))[f"{item}__avg"]

    def count_median_value(self, qs, item):
        _count = qs.count()
        values = qs.values_list(item, flat=True).order_by(item)
        if _count % 2 == 1:
            result = values[int(round(_count / 2))]
        else:
            result = sum(values[_count / 2 - 1 : _count / 2 + 1]) / 2.0  # noqa
        return result

    def count_moda_value(self, qs, item):
        max_count_item = (
            qs.values(item).annotate(dcount=Count(item)).order_by("-dcount")
        )[0]["dcount"]
        item_values_list = list(
            qs.values(item)
            .annotate(dcount=Count(item))
            .filter(dcount=max_count_item)
            .values(item)
            .order_by(item)
        )
        result_list = [str(el[item]) for el in item_values_list]
        result = f"{{{', '.join(result_list)}}}"  # format like {11,12}
        return result

    def save_result(self, item):
        CatsStat.objects.all().delete()
        c = CatsStat(**item)
        c.save()

    def show_result(self, item):
        cat_color_stat_table = PrettyTable()
        cat_color_stat_table.field_names = [
            "tail_length_mean",
            "tail_length_median",
            "tail_length_mode",
            "whiskers_length_mean",
            "whiskers_length_median",
            "whiskers_length_mode",
        ]
        cat_color_stat_table.add_row(
            [
                item["tail_length_mean"],
                item["tail_length_median"],
                item["tail_length_mode"],
                item["whiskers_length_mean"],
                item["whiskers_length_median"],
                item["whiskers_length_mode"],
            ]
        )
        print(cat_color_stat_table)
