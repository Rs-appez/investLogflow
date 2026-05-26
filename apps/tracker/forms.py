from django.forms import ModelForm, NumberInput, DateInput

from apps.tracker.models import Investment


class InvestmentForm(ModelForm):
    class Meta:
        model = Investment
        fields = ["amount_invested", "quantity", "date_invested"]
        labels = {
            "amount_invested": "Price per Share",
            "quantity": "Quantity",
            "date_invested": "Date Invested",
        }
        widgets = {
            "amount_invested": NumberInput(
                attrs={"class": "input input-bordered w-full [appearance:textfield]"}
            ),
            "quantity": NumberInput(
                attrs={"class": "input input-bordered w-full [appearance:textfield]"}
            ),
            "date_invested": DateInput(
                attrs={"class": "input input-bordered w-full", "type": "date"},
                format="%Y-%m-%d",
            ),
        }
        input_formats = {"date_invested": ["%Y-%m-%d"]}
