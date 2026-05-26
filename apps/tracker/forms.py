from django.forms import ModelForm, NumberInput, DateInput, Select, TextInput, Textarea

from apps.tracker.models import Investment, Portfolio
from apps.users.models import Organization


class InvestmentForm(ModelForm):
    class Meta:
        model = Investment
        fields = ["amount_invested", "quantity", "portfolio", "date_invested"]
        labels = {
            "amount_invested": "Price per Share",
            "quantity": "Quantity",
            "portfolio": "Portfolio",
            "date_invested": "Date Invested",
        }
        widgets = {
            "amount_invested": NumberInput(
                attrs={"class": "input input-bordered w-full [appearance:textfield]"}
            ),
            "quantity": NumberInput(
                attrs={"class": "input input-bordered w-full [appearance:textfield]"}
            ),
            "portfolio": Select(attrs={"class": "input input-bordered w-full"}),
            "date_invested": DateInput(
                attrs={"class": "input input-bordered w-full", "type": "date"},
                format="%Y-%m-%d",
            ),
        }
        input_formats = {"date_invested": ["%Y-%m-%d"]}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["portfolio"].queryset = Portfolio.objects.filter(  # pyright: ignore[reportAttributeAccessIssue]
                organization__members__in=[user]
            )


class PortfolioForm(ModelForm):
    class Meta:
        model = Portfolio
        fields = ["name", "description", "organization"]
        labels = {
            "name": "Portfolio Name",
            "organization": "Organization",
            "description": "Description",
        }
        widgets = {
            "name": TextInput(attrs={"class": "input input-bordered w-full"}),
            "organization": Select(attrs={"class": "input input-bordered w-full"}),
            "description": Textarea(
                attrs={"class": "textarea textarea-bordered w-full"}
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["organization"].queryset = Organization.objects.filter(  # pyright: ignore[reportAttributeAccessIssue]
                members__in=[user]
            )
