from django.shortcuts import render, redirect
from .models import Question

# 🔐 Custom Login
def login_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        # Save in session
        request.session['candidate'] = {
            'name': name,
            'email': email,
            'phone': phone
        }

        return redirect('dashboard')

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
    return render(request, 'exam.html', {'questions': questions})


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

    return render(request, 'result.html', {
        'candidate': request.session.get('candidate'),
        'score': score,
        'result': result
    })