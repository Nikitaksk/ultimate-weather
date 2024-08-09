from django import forms


class reportIssueForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100, widget=forms.TextInput(
                              attrs={'class': "input", "placeholder": "Enter your name"}))
    email = forms.EmailField(label="Your email", max_length=100, widget=forms.TextInput(
                              attrs={'class': "input", "placeholder": "Enter your email"}),)
    issue_type = forms.ChoiceField(widget=forms.Select(attrs={'class': ''}), choices={'bug' : 'Bug', 'perfomance' : 'Perfomance issue','request' : 'Feature Request', 'other' : 'Other'})
    issue_desc = forms.CharField(label="Your issue", max_length=100, widget=forms.Textarea(attrs={'class': "textarea has-fixed-size", 'placeholder': 'Describe the issue in detail'}))

