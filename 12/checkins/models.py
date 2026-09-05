from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class MoodEntry(models.Model):
    """
    مدل ثبت حال و احساسات کاربران
    """
    
    # ============================================
    # انتخاب‌های از پیش تعیین شده برای حال
    # ============================================
    SCORE_CHOICES = [
        (1, '😢 بد'),
        (2, '😕 نه‌چندان'),
        (3, '😐 معمولی'),
        (4, '🙂 خوب'),
        (5, '😊 عالی'),
    ]
    
    # ============================================
    # فیلدهای مدل
    # ============================================
    
    # کاربری که ثبت حال انجام داده
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='mood_entries',  # برای دسترسی راحت: user.mood_entries.all()
        verbose_name='کاربر'
    )
    
    # امتیاز حال (۱ تا ۵)
    score = models.IntegerField(
        choices=SCORE_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='حال',
        help_text='وضعیت احساسی خود را انتخاب کنید'
    )
    
    # برچسب احساسی (اختیاری)
    tag = models.CharField(
        max_length=50,
        blank=True,  # می‌تواند خالی باشد
        null=True,   # می‌تواند null باشد
        verbose_name='برچسب',
        help_text='مثلاً: خوشحال، خسته، پرانرژی، ناراحت'
    )
    
    # توضیحات تکمیلی (اختیاری)
    reason = models.TextField(
        blank=True,
        null=True,
        verbose_name='توضیحات',
        help_text='اگر دوست دارید بیشتر توضیح دهید'
    )
    
    # تاریخ ثبت (به صورت خودکار)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت'
    )
    
    # تاریخ آخرین ویرایش (به صورت خودکار)
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='آخرین ویرایش'
    )
    
    # ============================================
    # متدهای کمکی
    # ============================================
    
    def __str__(self):
        """
        نمایش نام کاربر و تاریخ ثبت در ادمین
        """
        return f"{self.user.username} - {self.get_score_display()} - {self.created_at.strftime('%Y/%m/%d %H:%M')}"
    
    def get_score_display_with_emoji(self):
        """
        دریافت نمایش امتیاز با ایموجی
        مثلاً: "😊 عالی"
        """
        emojis = {
            1: '😢',
            2: '😕',
            3: '😐',
            4: '🙂',
            5: '😊',
        }
        return f"{emojis.get(self.score, '')} {self.get_score_display()}"
    
    def get_score_emoji(self):
        """
        فقط ایموجی مربوط به امتیاز
        """
        emojis = {
            1: '😢',
            2: '😕',
            3: '😐',
            4: '🙂',
            5: '😊',
        }
        return emojis.get(self.score, '')
    
    def is_positive(self):
        """
        آیا حال مثبت است؟ (امتیاز ۴ یا ۵)
        """
        return self.score >= 4
    
    def is_negative(self):
        """
        آیا حال منفی است؟ (امتیاز ۱ یا ۲)
        """
        return self.score <= 2
    
    def is_neutral(self):
        """
        آیا حال معمولی است؟ (امتیاز ۳)
        """
        return self.score == 3
    
    def get_mood_status(self):
        """
        دریافت وضعیت کلی حال
        """
        if self.is_positive():
            return 'positive'
        elif self.is_negative():
            return 'negative'
        else:
            return 'neutral'
    
    # ============================================
    # متاداده‌های مدل
    # ============================================
    
    class Meta:
        ordering = ['-created_at']  # مرتب‌سازی بر اساس جدیدترین
        verbose_name = 'ثبت حال'
        verbose_name_plural = 'ثبت‌های حال'
        indexes = [
            models.Index(fields=['user', 'created_at']),  # ایندکس برای جستجوی سریع‌تر
            models.Index(fields=['score']),
        ]