import json

from django import forms

from .models import Cats

ORDER_PARAMETR = (("asc", "asc"), ("desc", "desc"))


class CatsSearchForm(forms.Form):

    _model_fields = set(
        (field.name, field.name) for field in Cats._meta.get_fields()
    )

    attribute = forms.ChoiceField(choices=_model_fields, required=False)
    order = forms.ChoiceField(choices=ORDER_PARAMETR, required=False)
    offset = forms.IntegerField(min_value=0, required=False)
    limit = forms.IntegerField(min_value=0, required=False)

    def clean(self):
        cleaned_data = super().clean()
        attribute = cleaned_data.get("attribute")
        order = cleaned_data.get("order")
        if order and not attribute:
            raise forms.ValidationError(
                "Sorting is possible only if there is an attribute"
            )
        return cleaned_data


class CatCreateForm(forms.ModelForm):
    class Meta:
        model = Cats
        fields = ["name", "color", "tail_length", "whiskers_length"]

    def __init__(self, *args, **kwargs):
        try:
            new_data = json.loads(kwargs["data"])
        except json.decoder.JSONDecodeError:
            new_data = {}
        kwargs["data"] = new_data
        super(CatCreateForm, self).__init__(*args, **kwargs)
