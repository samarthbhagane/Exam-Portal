from django.shortcuts import render, redirect
from django.db.models import Q 
from django.views.decorators.cache import never_cache
from .models import Question, Candidate
from django.contrib.auth.hashers import make_password, check_password


# 🔐 Custom Login
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            candidate = Candidate.objects.get(email=email)

            if not check_password(password, candidate.password):
                return render(request, 'login.html', {
                    "error": "Invalid email or password"
                })

            request.session['candidate'] = {
                'id': candidate.id,
                'name': candidate.name,
                'email': candidate.email,
                'phone': candidate.phone,
                'is_admin': candidate.is_admin
            }

            if candidate.is_admin:
                return redirect('results')
            return redirect('dashboard')

        except Candidate.DoesNotExist:
            return render(request, 'login.html', {
                "error": "Invalid email or password"
            })

    return render(request, 'login.html')


# Dashboard
@never_cache
def dashboard(request):
    if not request.session.get('candidate'):
        return redirect('login')
    if request.session['candidate'].get('is_admin'):
        return redirect('results')

    return render(request, 'dashboard.html', {
        'candidate': request.session.get('candidate')
    })


# Start Exam
@never_cache
def start_exam(request):
    if not request.session.get('candidate'):
        return redirect('login')
    if request.session['candidate'].get('is_admin'):
        return redirect('results')

    request.session['exam_started'] = True
    return redirect('exam')


# Exam Page
@never_cache
def exam_view(request):
    if not request.session.get('exam_started'):
        return redirect('dashboard')
    if request.session.get('candidate', {}).get('is_admin'):
        return redirect('results')

    questions = Question.objects.all()
    return render(request, 'exam.html', {
        'questions': questions,
        'candidate': request.session.get('candidate')
    })


# Submit
@never_cache
def submit_exam(request):
    if not request.session.get('candidate'):
        return redirect('login')
    if request.session['candidate'].get('is_admin'):
        return redirect('results')
    if request.method != "POST":
        return redirect('exam')

    request.session['exam_started'] = False

    questions = Question.objects.all()
    score = 0

    for q in questions:
        if request.POST.get(str(q.id)) == q.correct_answer:
            score += 1

    if score >= 16:
        result = "Excellent"
    elif score >= 11:
        result = "Good"
    elif score >= 6:
        result = "Average"
    else:
        result = "Not Suitable"

    candidate_data = request.session.get('candidate')
    candidate, _ = Candidate.objects.update_or_create(
        email=candidate_data.get('email'),
        defaults={
            'name': candidate_data.get('name'),
            'phone': candidate_data.get('phone'),
            'mcq_score': score,
            'result': result,
        }
    )

    response = render(request, 'exam_submit.html', {
        'candidate': candidate_data,
        'score': score,
        'result': result
    })

    request.session.flush()
    return response

def signup_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        candidate_obj, created = Candidate.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'phone': phone,
                'password': make_password(password),
            }
        )

        if not created:
            return render(request, 'signup.html', {
                'error': "Email already exists. Please login."
            })

        return redirect('login')

    return render(request, 'signup.html')

def result_view(request):
    if not request.session.get('candidate'):
        return redirect('login')
    if not request.session['candidate'].get('is_admin'):
        return redirect('dashboard')

    # Get search parameters
    search_query = request.GET.get('q', '').strip()
    result_filter = request.GET.get('result', '').strip()

    # Start with base queryset
    results = Candidate.objects.filter(is_admin=False)

    # Apply search query across multiple fields
    if search_query:
        results = results.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    # Apply result filter
    if result_filter:
        results = results.filter(result=result_filter)

    results = results.order_by('-created_at')

    return render(request, 'result.html', {
        'results': results,
        'request': request  # Pass request to template for form values
    })
