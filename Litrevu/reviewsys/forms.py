from django import forms

from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.label = field_name.capitalize()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ("ticket", "user")
        widgets = {
            "rating": forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)])
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        excluded_field = "rating"

        for field_name, field in self.fields.items():
            if field_name is not excluded_field:
                field.widget.attrs["class"] = "form-control"
                field.label = field_name.capitalize()
            else:
                field.widget.attrs["class"] = "form-check d-flex"
                field.label = field_name.capitalize()
