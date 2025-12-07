from django.shortcuts import render, redirect, get_object_or_404
from .models import JobApplication
from .forms import JobApplicationForm
import csv
from django.http import HttpResponse

def home(request):
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '')
    status_filter = request.GET.get('status', '')

    apps = JobApplication.objects.all()

    # 1) SEARCH
    if search:
        apps = apps.filter(company__icontains=search) | apps.filter(role__icontains=search)

    # 2) FILTER BY STATUS
    if status_filter:
        apps = apps.filter(status=status_filter)

    # 3) SORTING
    if sort == 'company':
        apps = apps.order_by('company')
    elif sort == 'role':
        apps = apps.order_by('role')
    elif sort == 'date':
        apps = apps.order_by('applied_date')
    elif sort == 'status':
        apps = apps.order_by('status')

    # 4) DASHBOARD STATS
    total = JobApplication.objects.count()
    applied = JobApplication.objects.filter(status='Applied').count()
    interview = JobApplication.objects.filter(status='Interview Scheduled').count()
    rejected = JobApplication.objects.filter(status='Rejected').count()
    selected = JobApplication.objects.filter(status='Selected').count()

    return render(request, 'applications/home.html', {
        'apps': apps,
        'total': total,
        'applied': applied,
        'interview': interview,
        'rejected': rejected,
        'selected': selected,
    })


def add(request):
    form = JobApplicationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'applications/add.html', {'form': form})


def edit(request, id):
    app = get_object_or_404(JobApplication, id=id)
    form = JobApplicationForm(request.POST or None, instance=app)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'applications/edit.html', {'form': form})


def delete(request, id):
    app = get_object_or_404(JobApplication, id=id)
    app.delete()
    return redirect('home')


# EXPORT CSV
def export_csv(request):
    apps = JobApplication.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="job_applications.csv"'

    writer = csv.writer(response)
    writer.writerow(['Company', 'Role', 'Status', 'Applied Date'])

    for a in apps:
        writer.writerow([a.company, a.role, a.status, a.applied_date])

    return response
