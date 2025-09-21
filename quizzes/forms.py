from django import forms
from .models import Quiz, QuizQuestion


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'subject']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})


class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ['question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'explanation']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3}),
            'explanation': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget.attrs.update({'class': 'form-control'})
        self.fields['option_a'].widget.attrs.update({'class': 'form-control'})
        self.fields['option_b'].widget.attrs.update({'class': 'form-control'})
        self.fields['option_c'].widget.attrs.update({'class': 'form-control'})
        self.fields['option_d'].widget.attrs.update({'class': 'form-control'})
        self.fields['correct_answer'].widget.attrs.update({'class': 'form-select'})
        self.fields['explanation'].widget.attrs.update({'class': 'form-control'})


class QuizSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search quizzes...'
    }))
    subject = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Filter by subject...'
    }))
