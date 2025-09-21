from django import forms
from .models import Resource, Review


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'subject', 'tags', 'file_type', 'file_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.TextInput(attrs={'placeholder': 'e.g., programming, python, tutorial'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['tags'].widget.attrs.update({'class': 'form-control'})
        self.fields['file_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['file_url'].widget.attrs.update({'class': 'form-control'})


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-select'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})


class ResourceSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search resources...'
    }))
    subject = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Filter by subject...'
    }))
    file_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Resource.TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
