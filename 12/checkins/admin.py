from django.contrib import admin
from django.utils.html import format_html
from checkins.models import MoodEntry


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    """
    تنظیمات نمایش مدل MoodEntry در پنل ادمین
    """
    
    # ============================================
    # فیلدهای نمایش در لیست
    # ============================================
    list_display = [
        'id',
        'user_display',
        'score_display_with_emoji',
        'score',  # ✅ این رو اضافه کردم چون در list_editable هست
        'tag',
        'created_at_display',
        'is_positive_badge',
        'status_badge',
    ]
    
    # ============================================
    # فیلدهای قابل ویرایش در لیست
    # ============================================
    list_editable = [
        'tag',
        'score',  # ✅ اینجا score هست و الآن در list_display هم هست
    ]
    
    # ============================================
    # فیلدهای قابل جستجو
    # ============================================
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'tag',
        'reason',
    ]
    
    # ============================================
    # فیلترهای کناری
    # ============================================
    list_filter = [
        'score',
        'tag',
        ('created_at', admin.DateFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
    ]
    
    # ============================================
    # تنظیمات نمایش
    # ============================================
    list_per_page = 25
    list_max_show_all = 100
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    # ============================================
    # فیلدهای فقط خواندنی
    # ============================================
    readonly_fields = [
        'created_at',
        'updated_at',
        'user_display',
        'score_display_with_emoji',
        'score_emoji_only',
        'is_positive_badge',
        'status_badge',
    ]
    
    # ============================================
    # گروه‌بندی فیلدها در فرم
    # ============================================
    fieldsets = (
        ('📝 اطلاعات اصلی', {
            'fields': (
                'user',
                'score',
                'tag',
                'reason',
            ),
            'description': 'اطلاعات مربوط به ثبت حال کاربر',
        }),
        ('📊 وضعیت', {
            'fields': (
                'score_display_with_emoji',
                'is_positive_badge',
                'status_badge',
            ),
            'classes': ('collapse',),
            'description': 'نمایش وضعیت حال',
        }),
        ('⏱️ زمان', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )
    
    # ============================================
    # اکشن‌های سفارشی
    # ============================================
    actions = [
        'make_positive',
        'make_negative',
        'delete_selected',
    ]
    
    def make_positive(self, request, queryset):
        """
        تغییر امتیاز به مثبت (۴ و ۵)
        """
        updated = queryset.update(score=4)
        self.message_user(request, f'{updated} ثبت حال به مثبت تغییر کرد.')
    make_positive.short_description = '👍 تغییر به حال مثبت (۴)'
    
    def make_negative(self, request, queryset):
        """
        تغییر امتیاز به منفی (۲)
        """
        updated = queryset.update(score=2)
        self.message_user(request, f'{updated} ثبت حال به منفی تغییر کرد.')
    make_negative.short_description = '👎 تغییر به حال منفی (۲)'
    
    # ============================================
    # متدهای نمایش سفارشی
    # ============================================
    
    @admin.display(description='کاربر', ordering='user__username')
    def user_display(self, obj):
        """
        نمایش نام کامل کاربر
        """
        if obj.user.first_name and obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.username
    
    @admin.display(description='حال', ordering='score')
    def score_display_with_emoji(self, obj):
        """
        نمایش امتیاز با ایموجی
        """
        emojis = {
            1: '😢',
            2: '😕',
            3: '😐',
            4: '🙂',
            5: '😊',
        }
        return f"{emojis.get(obj.score, '')} {obj.get_score_display()}"
    
    @admin.display(description='ایموجی')
    def score_emoji_only(self, obj):
        """
        فقط ایموجی
        """
        emojis = {
            1: '😢',
            2: '😕',
            3: '😐',
            4: '🙂',
            5: '😊',
        }
        return emojis.get(obj.score, '')
    
    @admin.display(description='تاریخ ثبت', ordering='created_at')
    def created_at_display(self, obj):
        """
        نمایش تاریخ به صورت خوانا
        """
        return obj.created_at.strftime('%Y/%m/%d - %H:%M')
    
    @admin.display(description='وضعیت', boolean=True)
    def is_positive_badge(self, obj):
        """
        وضعیت مثبت یا منفی بودن
        """
        return obj.score >= 4
    
    @admin.display(description='وضعیت کلی')
    def status_badge(self, obj):
        """
        نمایش وضعیت کلی با رنگ‌بندی
        """
        if obj.score >= 4:
            color = '#10B981'  # سبز
            status = '✅ عالی'
        elif obj.score >= 3:
            color = '#F59E0B'  # زرد
            status = '⚡ معمولی'
        else:
            color = '#EF4444'  # قرمز
            status = '❌ نیاز به توجه'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 12px; border-radius: 12px; font-size: 12px;">{}</span>',
            color, status
        )
    
    # ============================================
    # تنظیمات ذخیره‌سازی
    # ============================================
    
    def save_model(self, request, obj, form, change):
        """
        هنگام ذخیره در ادمین
        """
        if not change:  # اگر جدید است
            if not obj.user_id:
                obj.user = request.user
        super().save_model(request, obj, form, change)