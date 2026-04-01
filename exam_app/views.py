from django.shortcuts import render, redirect
from .models import Question, Candidate

# 🔐 Custom Login
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            candidate = Candidate.objects.get(email=email, password=password)

            request.session['candidate'] = {
                'id': candidate.id,
                'name': candidate.name,
                'email': candidate.email,
                'phone': candidate.phone,
                'is_admin': candidate.is_admin
            }

            if candidate.is_admin:
                return redirect('admin_dashboard')   
            else:
                return redirect('dashboard')

        except Candidate.DoesNotExist:
            return render(request, 'login.html', {
                "error": "Invalid email or password"
            })

    return render(request, 'login.html')


# Dashboard
def dashboard(request):
    if not request.session.get('candidate'):
        return redirect('login')

    return render(request, 'dashboard.html', {
        'candidate': request.session.get('candidate')
    })


# Start Exam
def start_exam(request):
    if not request.session.get('candidate'):
        return redirect('login')

    request.session['exam_started'] = True
    return redirect('exam')


# Exam Page
def exam_view(request):
    if not request.session.get('exam_started'):
        return redirect('dashboard')

    questions = Question.objects.all()
    return render(request, 'exam.html', {
        'questions': questions,
        'candidate': request.session.get('candidate')
    })


# Submit
def submit_exam(request):
    if not request.session.get('candidate'):
        return redirect('login')

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
    Candidate.objects.filter(email=candidate_data.get('email')).update(
        name=candidate_data.get('name'),
        phone=candidate_data.get('phone'),
        mcq_score=score,
        result=result,
    )

    return render(request, 'exam_submit.html', {
        'candidate': candidate_data,
        'score': score,
        'result': result
    })

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
                'password': password,
            }
        )

        if not created:
            return render(request, 'signup.html', {
                'error': "Email already exists. Please login."
            })

        return redirect('login')

    return render(request, 'signup.html')