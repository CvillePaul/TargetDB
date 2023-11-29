from django import forms

class ImportTargetsForm(forms.Form):
    file = forms.FileField(max_length=10000, allow_empty_file=False, label="File of target IDs")
    require_all = forms.BooleanField(label="Fail if any IDs not found")
