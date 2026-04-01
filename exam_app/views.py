from django.shortcuts import render, redirect
from .models import Question, Candidate

# 🔐 Custom Login
def login_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        candidate_obj, _ = Candidate.objects.update_or_create(
            email=email,
            defaults={
                'name': name,
                'phone': phone,
            }
        )

        # Save in session
        request.session['candidate'] = {
            'id': candidate_obj.id,
            'name': candidate_obj.name,
            'email': candidate_obj.email,
            'phone': candidate_obj.phone,
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