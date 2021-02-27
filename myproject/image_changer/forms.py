from django import forms

class LoadImageForm(forms.Form):

	image_url = forms.URLField(required=False)
	image_file = forms.FileField(required=False)

class ChangeSizeForm(forms.Form):

	x = forms.IntegerField(required=False)
	y = forms.IntegerField(required=False)