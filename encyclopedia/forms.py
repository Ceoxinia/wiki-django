from django import forms

# Form used in sidebar to search through entry titles
class SearchForm(forms.Form):
    query = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search Wiki', 
            'style': 'width:100%'}))


# Form used to create a new entry/page
class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Enter title', 'id': 'new-entry-title'}))
    data = forms.CharField(label="text", widget=forms.Textarea(attrs={
        'id': 'new-entry', 'style':'width: 100%; height:500px','placeholder':'Enter text using Github MarkDown syntax'}))


# Form used to edit a entry/page
class EditPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        'id': 'edit-entry-title'}))
    data = forms.CharField(label="", widget=forms.Textarea(attrs={
        'id': 'edit-entry','style':'width: 100%; height:500px'}))