from django import forms
from checkins.models import MoodEntry


class MoodEntryForm(forms.ModelForm):
    """
    فرم ثبت حال کاربر
    """
    
    class Meta:
        model = MoodEntry
        fields = ["score", "reason", "tag"]
        
        # ویجت‌ها برای نمایش بهتر در صفحه
        widgets = {
            'score': forms.RadioSelect(choices=MoodEntry.SCORE_CHOICES),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'اگر دوست داری، بیشتر توضیح بده...',
                'style': 'resize: vertical;',
            }),
            'tag': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثلاً: خوشحال، خسته، پرانرژی، ناراحت',
                'maxlength': 50,
            }),
        }
        
        # برچسب‌های فارسی برای فیلدها
        labels = {
            'score': '🥰 حالت امروز چطوره؟',
            'reason': '💬 توضیحات (اختیاری)',
            'tag': '🏷️ برچسب احساسی (اختیاری)',
        }
        
        # راهنمای فیلدها
        help_texts = {
            'score': 'یکی از گزینه‌ها رو انتخاب کن',
            'tag': 'با یک کلمه حالت رو توصیف کن (حداکثر ۵۰ کاراکتر)',
            'reason': 'هر چیزی که دوست داری به اشتراک بذار',
        }
        
        # پیام‌های خطا
        error_messages = {
            'score': {
                'required': 'لطفاً حالت امروز خود را انتخاب کنید.',
            },
        }
    
    def __init__(self, *args, **kwargs):
        """
        تنظیمات اضافی هنگام ساخت فرم
        """
        super().__init__(*args, **kwargs)
        
        # اضافه کردن کلاس CSS به همه فیلدها
        for field_name, field in self.fields.items():
            if field_name != 'score':  # برای RadioSelect نیازی نیست
                if hasattr(field.widget, 'attrs'):
                    field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'
        
        # تنظیمات خاص برای فیلد score
        self.fields['score'].widget.attrs['class'] = 'mood-radio'
    
    def clean_tag(self):
        """
        اعتبارسنجی برچسب
        """
        tag = self.cleaned_data.get('tag', '').strip()
        if tag and len(tag) > 50:
            raise forms.ValidationError('برچسب نمی‌تواند بیشتر از ۵۰ کاراکتر باشد.')
        return tag
    
    def clean_reason(self):
        """
        اعتبارسنجی توضیحات
        """
        reason = self.cleaned_data.get('reason', '').strip()
        if reason and len(reason) > 1000:
            raise forms.ValidationError('توضیحات نمی‌تواند بیشتر از ۱۰۰۰ کاراکتر باشد.')
        return reason
    
    def clean(self):
        """
        اعتبارسنجی کلی فرم
        """
        cleaned_data = super().clean()
        score = cleaned_data.get('score')
        
        # اگر امتیاز پایین است و توضیحی نوشته نشده، اخطار بده
        if score and score <= 2:
            reason = cleaned_data.get('reason', '')
            if not reason or len(reason.strip()) < 3:
                self.add_error('reason', 'اگر حالت خوب نیست، می‌تونی توضیح بدی تا بتونیم کمکت کنیم 💚')
        
        return cleaned_data