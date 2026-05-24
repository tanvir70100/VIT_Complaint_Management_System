from django import forms
from django.contrib.auth.models import User
from .models import Complaint, ComplaintComment


class ComplaintForm(forms.ModelForm):
    accused = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label="Accused Person"
    )

    class Meta:
        model = Complaint
        fields = ['title', 'description', 'accused', 'evidence']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complaint title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the complaint clearly'
            }),
            'evidence': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        if current_user:
            self.fields['accused'].queryset = User.objects.exclude(id=current_user.id)

        self.fields['accused'].widget.attrs.update({'class': 'form-select'})


class CommentForm(forms.ModelForm):
    class Meta:
        model = ComplaintComment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment'
            }),
        }


class VerdictForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status', 'verdict']

        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'verdict': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write reviewer verdict'
            }),
        }

class ComplaintEditForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'evidence']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complaint title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the complaint clearly'
            }),
            'evidence': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }