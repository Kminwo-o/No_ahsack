from django import forms

class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='영화 검색')
