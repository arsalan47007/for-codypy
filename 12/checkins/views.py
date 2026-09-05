from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta

from .models import MoodEntry
from .forms import MoodEntryForm


def home(request):
    context = {}
    
    if request.user.is_authenticated:
        today_mood = MoodEntry.objects.filter(user=request.user).order_by('-created_at').first()
        total_checks = MoodEntry.objects.filter(user=request.user).count()
        streak = calculate_streak(request.user)
        
        top_tag = MoodEntry.objects.filter(user=request.user)\
            .values('tag')\
            .annotate(count=Count('id'))\
            .order_by('-count')\
            .first()
        
        context.update({
            'today_mood': today_mood.get_score_display() if today_mood else '-',
            'total_checks': total_checks,
            'streak': streak,
            'top_tag': top_tag['tag'] if top_tag and top_tag['tag'] else '-',
        })
    
    return render(request, "checkins/home.html", context)


def about(request):
    return render(request, "checkins/about.html")


@login_required
def check_in(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, '😊 حال شما با موفقیت ثبت شد!')
            return redirect('checkins:report')
        else:
            messages.error(request, '❌ خطا در ثبت اطلاعات. لطفاً دوباره تلاش کنید.')
    else:
        form = MoodEntryForm()
    
    recent_checks = MoodEntry.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    moods = [
        {'value': 5, 'emoji': '😊', 'label': 'عالی'},
        {'value': 4, 'emoji': '🙂', 'label': 'خوب'},
        {'value': 3, 'emoji': '😐', 'label': 'معمولی'},
        {'value': 2, 'emoji': '😕', 'label': 'نه‌چندان'},
        {'value': 1, 'emoji': '😢', 'label': 'بد'},
    ]
    
    return render(request, "checkins/check_in.html", {
        'form': form,
        'recent_checks': recent_checks,
        'moods': moods,
    })


@login_required
def report(request):
    selected_date = request.GET.get('date', '')
    low_only = request.GET.get('low', '') == '1'
    tag_filter = request.GET.get('tag', '')
    
    entries = MoodEntry.objects.filter(user=request.user)
    
    if selected_date:
        try:
            filter_date = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date()
            entries = entries.filter(created_at__date=filter_date)
        except ValueError:
            pass
    
    if tag_filter:
        entries = entries.filter(tag=tag_filter)
    
    if low_only:
        entries = entries.filter(score__lt=3)
    
    entries = entries.order_by('-created_at')
    
    count = entries.count()
    avg_score = entries.aggregate(avg=Avg('score'))['avg']
    streak = calculate_streak(request.user)
    
    top_tag = MoodEntry.objects.filter(user=request.user)\
        .values('tag')\
        .annotate(count=Count('id'))\
        .order_by('-count')\
        .first()
    
    context = {
        'entries': entries,
        'count': count,
        'avg_score': avg_score,
        'selected_date': selected_date,
        'low_only': low_only,
        'streak': streak,
        'top_tag': top_tag['tag'] if top_tag and top_tag['tag'] else '-',
    }
    
    return render(request, "checkins/report.html", context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '🎉 ثبت‌نام با موفقیت انجام شد! خوش آمدید.')
            return redirect('checkins:home')
        else:
            messages.error(request, '❌ خطا در ثبت‌نام. لطفاً اطلاعات را بررسی کنید.')
    else:
        form = UserCreationForm()
    
    return render(request, "checkins/register.html", {'form': form})


def calculate_streak(user):
    entries = MoodEntry.objects.filter(user=user).values_list('created_at', flat=True).order_by('-created_at')
    
    if not entries:
        return 0
    
    today = timezone.now().date()
    streak = 0
    current_date = today
    
    entry_dates = [entry.date() for entry in entries]
    
    if entry_dates and entry_dates[0] < today - timedelta(days=1):
        return 0
    
    for date in entry_dates:
        if date == current_date:
            streak += 1
            current_date -= timedelta(days=1)
        elif date < current_date:
            break
    
    return streak


# ==============================================
# ویوهای قدیمی (برای سازگاری)
# ==============================================

@login_required
def get_form(request):
    if request.method == 'POST':
        my_form = MoodEntryForm(request.POST)
        if my_form.is_valid():
            entry = my_form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, '😊 حال شما با موفقیت ثبت شد!')
            return redirect('checkins:report')
    else:
        my_form = MoodEntryForm()
    
    return render(request, "checkins/entry_form.html", {"form": my_form})