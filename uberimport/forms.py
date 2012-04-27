from django import forms

class UploadCSVForm(forms.Form):
	RESOURCE_CHOICES = (
	 	('item', 'Item'),
		('expense', 'Expenses'),
		('client', 'Clients'),
	)
	subdomain = forms.CharField(max_length=50)
	token = forms.CharField(max_length=50)
	resource = forms.ChoiceField(choices=RESOURCE_CHOICES)
	file  = forms.FileField()