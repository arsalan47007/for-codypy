from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from checkins.models import MoodEntry
from checkins.forms import MoodEntryForm

def home(requests):
    # return HttpResponse("Welcome to my website")
    return render(requests, "checkins/home.html")


@login_required
def get_form(requests):
    if requests.method == 'POST':
        my_form = MoodEntryForm(requests.POST)
        if my_form.is_valid():
            entry = my_form.save(commit=False)
            entry.user = requests.user 
            entry_2 = entry.save()

            return HttpResponse("add success!")
    else:
        my_form = MoodEntryForm()

    return render(
        requests,
        "checkins/entry_form.html",
        {"form": my_form}
    )


@login_required
def report(requests):
    # entry = MoodEntry.objects.all()
    print(requests.user, requests.user.is_staff)
    entry = MoodEntry.objects.filter(user=requests.user)

    return render(
        requests,
        "checkins/report.html",
        # selected_date, low_only, avg_score
        {"entries": entry, "count": entry.count()}
    )
