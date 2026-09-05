from django import forms

from checkins.models import MoodEntry


class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ["score", "reason", "tag"]
