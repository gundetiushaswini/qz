from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Question, UserScore, FAQ
from .forms import RegistrationForm, QuestionForm, ContactForm

# Home View
@login_required
def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})

# Register View
def register(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('name')

        # Validate data
        if not username or not password or not full_name:
            messages.error(request, 'Please fill in all fields.')
            return redirect('register')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect('register')

        # Create the user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.first_name = full_name  # Save full name as first name
            user.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')  # Redirect to the login page
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('register')

    return render(request, 'register.html')

# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Quiz View
@login_required
def quiz(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    questions = category.questions.all()
    return render(request, 'quiz.html', {'category': category, 'questions': questions})

# Results View
@login_required
def results(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    questions = category.questions.all()
    score = 0

    if request.method == 'POST':
        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option == question.correct_answer:
                score += 1

        # Save or update the user's score
        user_score, created = UserScore.objects.get_or_create(
            user=request.user,
            category=category,
            defaults={'score': score}
        )
        if not created:
            user_score.score = score
            user_score.save()

        return render(request, 'results.html', {'category': category, 'score': score, 'total': questions.count()})

    messages.error(request, 'You have not submitted this quiz yet.')
    return redirect('home')

# Leaderboard View
@login_required
def leaderboard(request):
    scores = UserScore.objects.all().order_by('-score')[:10]
    return render(request, 'leaderboard.html', {'scores': scores})

# Contact View
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send an email (optional)
        send_mail(
            f'Contact Form Submission from {name}',
            message,
            email,
            [settings.EMAIL_HOST_USER],

        )

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')

# About View
def about(request):
    return render(request, 'about.html')

# Landing View
def landing(request):
    return render(request, 'landing.html')

# FAQ View
def faq_view(request):
    faqs = FAQ.objects.all()  # Assuming you have an FAQ model
    return render(request, 'faq.html', {'faqs': faqs})

# Terms and Conditions View
def terms_conditions(request):
    return render(request, 'terms_conditions.html')

# Privacy Policy View
def privacy_policy(request):
    return render(request, 'privacy_policy.html')