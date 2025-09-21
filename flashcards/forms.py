from django import forms
from .models import Flashcard, FlashcardItem


class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['title', 'description', 'subject']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})


class FlashcardItemForm(forms.ModelForm):
    class Meta:
        model = FlashcardItem
        fields = ['front_text', 'back_text', 'order']
        widgets = {
            'front_text': forms.Textarea(attrs={'rows': 3}),
            'back_text': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['front_text'].widget.attrs.update({'class': 'form-control'})
        self.fields['back_text'].widget.attrs.update({'class': 'form-control'})
        self.fields['order'].widget.attrs.update({'class': 'form-control'})


class FlashcardSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search flashcards...'
    }))
    subject = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Filter by subject...'
    }))
