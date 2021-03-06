from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import JsonResponse
from .forms import QuizForm
from django.contrib import auth, messages
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import AnswerSheet, Answer
from quiz.models import Quiz, Question
import socket
import random
socket.getaddrinfo('localhost', 8000)


@login_required(login_url='/login')
def admin_dash(request):
    if request.user.is_admin():
        item = Quiz.objects.all().order_by('quiz_name')
        paginator = Paginator(item, 5)  # Show 1o quizzes per page
        page = request.GET.get('page', 1)
        try:
            item = paginator.get_page(page)
        except PageNotAnInteger:
            item = paginator.get_page(1)
        except EmptyPage:
            item = paginator.get_page(paginator.num_pages)
        context = {'title': 'Admin', 'quiz_object': item}

    else:
        context = {'title': "Error", 'messages': ['Not an admin', 'Do not even Try']}

    return render(request, 'admin_index.html', context=context)


def finish(request):
    return redirect('admin_dashboard')


def add_questions(request, quizid):

    user = request.user
    if user.is_admin():

        quiz = Quiz.objects.get(quiz_id=quizid)

        if request.method == 'POST':

            q_type = strip_tags(request.POST.get('type'))
            ques = Question()
            ques.quiz = quiz
            ques.type = strip_tags(request.POST.get('type'))
            ques.marks = strip_tags(request.POST.get('marks'))
            ques.level = strip_tags(request.POST.get('level'))
            ques.time_limit = strip_tags(request.POST.get('time_limit'))
            ques.question = strip_tags(request.POST.get('question'))
            ques.negative = strip_tags(request.POST.get('negative'))

            # if Image is uploaded
            img = request.FILES.get('image')
            if img:

                ques.image = img
            else:
                print("\n\n\n\nNo File was uploaded\n\n\n\n")

            # if Code is added
            code = request.POST.get('code')
            if code:
                ques.code = code

            # if Question is subjective
            if q_type == 's':
                ques.subjective_answer = strip_tags(request.POST.get('subjective_answer'))

            # Question is objective
            else:
                ques.option_A = strip_tags(request.POST.get('option_a'))
                ques.option_B = strip_tags(request.POST.get('option_b'))
                ques.option_C = strip_tags(request.POST.get('option_c'))
                ques.option_D = strip_tags(request.POST.get('option_d'))
                ques.correct = strip_tags(request.POST.get('correct'))

            ques.save()
            return JsonResponse({'kudos': "kudos"})

        # GET the page
        else:
            return render(request, 'add_questions.html', {'title': 'Add Questions', 'quiz_data': quiz})
    # User Does not has sufficient permissions
    else:

        messages.info(request, 'You do not have the permissions required to edit this quiz')
        return redirect('home')


# This function creates a unique ID for new quiz
def create_quiz_id(size):
    uid = get_random_string(length=size)

    # check if Quiz already exists if not, return id
    try:
        notebook = Quiz.objects.get(quiz_id=uid)
    except:
        notebook = None

    if not notebook:
        return uid
    else:
        create_quiz_id(size)  # If uid already exists recreate uid


@login_required(login_url='login/')
def create_quiz(request):

    user = request.user
    if user.is_admin():

        if request.method == 'POST':
            # form is submitted
            quiz_form = QuizForm(request.POST, request.user)

            if quiz_form.is_valid:
                # Create new instance of quiz
                item = Quiz()

                # Create random id and password
                item.quiz_id = create_quiz_id(size=random.randint(5, 10))
                item.quiz_password = get_random_string(length=random.randint(8, 12))

                # Fill other details of the Quiz Object
                item.quiz_name = strip_tags(request.POST['quiz_name'])
                item.description = strip_tags(request.POST['description'])
                item.instructions = strip_tags(request.POST['instructions'])
                item.duration = strip_tags(request.POST['duration'])
                item.quiz_time = request.POST['quiz_time']
                item.quizmaster = request.user
                item.tags = strip_tags(request.POST['tags'])

                # Save the Quiz object and mail the credentials
                item.save()
                send_mail(
                    'New Quiz Created:'+item.quiz_name,
                    'Here are the credentials\n'+'Quiz_id='+item.quiz_id+'\nQuiz_password='+item.quiz_password,
                    'binary.compatible@gmail.com',
                    [user.email],
                    fail_silently=True,
                )
                return redirect('add_questions/'+item.quiz_id)
            # errors are raised
            else:
                messages.error(request, 'Please correct the error below.')
                return render(request, 'create_quiz.html', {'title': 'Create Quiz', 'quiz_form': quiz_form})

        else:
            # get request. We have to return the form so that user can fill it.
            create_quiz_form = QuizForm()
            return render(request, 'create_quiz.html', {'title': 'Create Quiz', 'quiz_form': create_quiz_form})
    else:
        messages.info(request, 'You do not have the permissions required create a quiz')
        return redirect('home')


# Function to edit quiz credentials
@login_required(login_url='login/')
@transaction.atomic()
def edit_quiz(request, quizid):
    user = request.user
    quiz_instance = Quiz.objects.get(quiz_id=quizid)

    if user.is_admin():
        if request.method == 'POST':

            quiz_form = QuizForm(request.POST, instance=quiz_instance)
            if quiz_form.is_valid():
                quiz_form.save()
                messages.success(request, 'Your Quiz was successfully updated!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            quiz_form = QuizForm(instance=quiz_instance)

        return render(request, 'edit_quiz.html', {
            'title': "{} - Edit".format(quiz_instance.quiz_name),
            'quiz_form': quiz_form,
            'quiz': quiz_instance
        })

    else:
        return render(request, 'edit_quiz.html', {
            'title': "Error",
            'messages': ["Permissions Denied", "Privilege Not Available!"]
        })


# Function to manage AnswerSheet list
@login_required(login_url='/login')
def grader(request, quizid):
    user = request.user
    quiz_instance = Quiz.objects.get(quiz_id=quizid)

    if user.is_admin():
        try:
            sheet_instances = get_list_or_404(AnswerSheet, quiz=quiz_instance, is_attempted=True, is_valid=True,
                                              is_graded=False)
            context = {
                'title': "{} - Grade".format(quiz_instance.quiz_name),
                'sheets': sheet_instances,
                'quiz': quiz_instance
            }
        except:
            context = {
                'title': "{} - Grade".format(quiz_instance.quiz_name),
                'quiz': quiz_instance,
                'messages': ['No sheets to grade for this Quiz', 'All Done']
            }

        return render(request, 'grader.html', context=context)

    else:
        return render(request, 'grader.html', {
            'title': "Error",
            'messages': ["Permissions Denied", "Privilege Not Available!"]
        })


# Function to grade Subjective Questions
@login_required(login_url='/login')
def sheet_grader(request, sheet_id):
    if request.user.is_admin():
        sheet = get_object_or_404(AnswerSheet, id=sheet_id)
        try:
            answer_list = get_list_or_404(Answer, sheet=sheet, is_graded=False)
            context = {'title': 'Grade', 'sheet_object': sheet, 'answers': answer_list, }

        except:
            context = {'title': 'Grade', 'sheet_object': sheet, 'messages': ['All the answers have already been graded',
                                                                             'Click Finish Grading']}

        if request.method == "POST":
            answer_id = request.POST.get('ans_id')
            marks = request.POST.get('marks_given')

            answer_object = Answer.objects.get(id=answer_id)
            answer_object.marks_awarded = marks
            answer_object.is_graded = True
            answer_object.save()

        return render(request, 'grade_sheet.html', context=context)


@login_required(login_url='/login')
def finish_grading(request, sheet_id):
    if request.user.is_admin():

        try:
            sheet = get_object_or_404(AnswerSheet, id=sheet_id)
        except:
            sheet = None

        if sheet is not None:
            question_list = get_list_or_404(Question, quiz=sheet.quiz)
            answer_list = get_list_or_404(Answer, sheet=sheet)
            total_marks = 0
            marks_obtained = total_subjective = total_objective_positive = total_objective_negative = 0
            for question in question_list:
                total_marks = total_marks + question.marks
            for answer in answer_list:
                marks_obtained = marks_obtained + answer.marks_awarded
                if answer.question.is_subjective:
                    total_subjective = total_subjective + answer.marks_awarded
                else:
                    total_objective_positive = total_objective_positive + (answer.marks_awarded if answer.marks_awarded >= 0 else 0)
                    total_objective_negative = total_objective_negative + (answer.marks_awarded if answer.marks_awarded < 0 else 0)
            print(total_objective_positive)
            print(total_objective_negative)
            print(total_subjective)
            sheet.total_marks_available = total_marks
            sheet.total_marks_obtained = marks_obtained
            sheet.total_subjective_marks = total_subjective
            sheet.total_objective_positive = total_objective_positive
            sheet.total_objective_negative = total_objective_negative
            sheet.is_graded = True
            sheet.save()

        messages.info(request, 'Quiz Graded Successfully')
        return redirect('grader', quizid=sheet.quiz.quiz_id)

    else:
        messages.info(request, 'Permission Denied')
        return redirect('dashboard')


# Function for LeaderBoard of each Quiz
def quiz_leader_board(request, quiz_id):
    quiz_object = get_object_or_404(Quiz, quiz_id=quiz_id)
    sheet_list = get_list_or_404(AnswerSheet.objects.order_by('-total_marks_obtained'), quiz=quiz_object, is_graded=True)
    context = {'title': 'LeaderBoards', 'quiz': quiz_object, 'leader_data': sheet_list}
    return render(request, 'quiz_leader_board.html', context=context)


# Function for Showing all quiz
def leader_board(request):
    quiz_list = get_list_or_404(Quiz.objects.order_by('-quiz_time'), is_active=True)
    context = {'title': 'LeaderBoards', 'leader_data': quiz_list}
    return render(request, 'LeaderBoard.html', context=context)