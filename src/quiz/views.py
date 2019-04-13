from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question
from admin_panel.models import AnswerSheet, Answer
from django.utils.html import strip_tags
from datetime import datetime, date
from django.utils.timezone import datetime, timedelta
import random
import pytz
utc = pytz.UTC



# Create your views here.



@login_required(login_url='/login')
def quiz_auth(request, quizid):
    item = Quiz.objects.get(quiz_id=quizid)
    item.duration = item.duration
    users = item.users_appeared.filter(pk=request.user.pk)
    start_time = item.quiz_time
    today = datetime.now()
    print(today.tzinfo)
    print(start_time)
    print(today)
    temp = datetime.combine(date.min, today.time()) - datetime.combine(date.min, item.quiz_time.time())
    if temp < timedelta(minutes=5):
        print("hola")
        margin = 1
    else:
        margin = 0

    if(today >start_time and margin ):

        if users.exists():
            messages.info(request, 'You already appeared in this Quiz')
            return redirect('dashboard')
        else:
            if item.quiz_password == request.POST['password']:
                request.session['username'] = quizid
                # if request.user.profile.role == 'client':
                #     item.users_appeared.add(request.user)

                return redirect('test/' + str(quizid))
            else:

                # return render(request, 'start', {'error': 'Invalid Credentials!'})
                messages.info(request, 'Invalid Credentials')
                return redirect('dashboard')
    else:
        messages.info(request, "You can't start now!")
        return redirect('dashboard')


def create_answer_table(quiz_object, question_objects, user_object):
    for question_object in question_objects:
        list_sheet = get_object_or_404(AnswerSheet, contestant=user_object, quiz=quiz_object)
        ans = Answer()
        ans.sheet = list_sheet
        ans.question = question_object
        ans.save()
    return


# Function for conducting quiz
@login_required(login_url='/login')
def conduct_quiz(request, quizid):
    # this checks is for preventing user to open quiz through URL
    if request.session['username'] == quizid:

        aspirant = request.user
        item = get_object_or_404(Quiz, quiz_id=quizid)
        data = list(Question.objects.filter(quiz=item))
        random.shuffle(data)

        list_sheet = get_object_or_404(AnswerSheet, contestant=aspirant, quiz=item)

        # Question Submission
        if request.method == 'POST':
            if list_sheet.is_valid and not list_sheet.is_attempted:
                question_object = get_object_or_404(Question, id=request.POST.get('question_id'))
                answer_object = get_object_or_404(Answer, question=question_object, sheet=list_sheet)

                if not answer_object.is_attempted:
                    # Update values
                    if question_object.is_subjective:
                        answer_object.subjective_answer = strip_tags(request.POST.get('subjective_answer'))
                    elif question_object.is_single:
                        answer_object.response_A = request.POST.get('single_answer')

                    # Multi correct
                    else:
                        check_list = request.POST.getlist('multi_answer[]')
                        print(check_list[0])
                        length = len(check_list)
                        if length == 1:
                            answer_object.response_A = check_list[0]
                        elif length == 2:
                            answer_object.response_A = check_list[0]
                            answer_object.response_B = check_list[1]
                        elif length == 3:
                            answer_object.response_A = check_list[0]
                            answer_object.response_B = check_list[1]
                            answer_object.response_C = check_list[2]
                        elif length == 4:
                            answer_object.response_A = check_list[0]
                            answer_object.response_B = check_list[1]
                            answer_object.response_C = check_list[2]
                            answer_object.response_D = check_list[3]

                    answer_object.response_time = request.POST.get('response_time')
                    answer_object.is_attempted = True
                    answer_object.save()

                else:
                    context = {'title': 'Error', 'messages': 'You have already attempted this question'}
                    return JsonResponse(context)

            else:
                messages.info(request, 'You have already attempted this quiz')
                return redirect('dashboard')

        querys = []
        for question in data:
            querys.append(question)

        else:
            try:
                answers = get_list_or_404(Answer, sheet=list_sheet)
            except:
                create_answer_table(item, data, aspirant)

        return render(request, 'conduct_quiz.html', {'title': 'Best of Luck', 'quiz_object': item, 'quiz_data': querys,
                                                     'user': aspirant})
    else:
        return redirect('dashboard')


@login_required(login_url='/login')
def instructions(request, quizid):

    try:
        item = Quiz.objects.get(quiz_id=quizid)
        user = request.user
        instruct = item.instructions
        instruct_list = instruct.split(";")

        today = datetime.now()
        temp = datetime.combine(date.min, today.time()) - datetime.combine(date.min, item.quiz_time.time())
        print(item.quiz_time)
        print(today)
        # if(today>item.quiz_time):
        #      print(0)
        if temp < timedelta(minutes=5):
            print("hola")
            margin = 1
        else:
            margin = 0

        return render(request, 'instructions.html',
                      {'quiz_object': item, 'user': user, 'instruct_list': instruct_list, 'today': today,
                       'margin': margin})
    except Quiz.DoesNotExist:
        messages.info(request, 'Quiz does not exists!')
        return redirect('dashboard')


@login_required(login_url='/login')
def start_quiz(request):
    if request.method == 'POST':
        quizid = request.POST.get('quizid')
        try:
            quiz_instance = Quiz.objects.get(quiz_id=quizid)
            user = request.user
            # this is to check if the user has registered or not
            list_sheet = AnswerSheet.objects.filter(contestant=user).filter(quiz=quiz_instance)
            if list_sheet.exists():
                return redirect('instructions/'+quizid)
            else:
                messages.info(request, 'You need to register first!')
                return redirect('dashboard')
        except Quiz.DoesNotExist:
            messages.info(request, 'Invalid Quiz-id')
            return redirect('admin_dashboard')
    else:
         return redirect('dashboard')

@login_required(login_url='/login')
def register_quiz(request, quizid):

    try:
        # Get Quiz form DB
        quiz_instance = Quiz.objects.get(quiz_id=quizid)
        user = request.user
        tags = quiz_instance.tags
        tags_list = tags.split(';')
        # this is to check if the user has registered or not
        list_sheet = AnswerSheet.objects.filter(contestant=user).filter(quiz=quiz_instance)

        if list_sheet.exists():
            flag = 0
        else:
            flag = 1
        print(list_sheet)
        if request.method == 'POST':
            try:
                # Check if user is already registered for the quiz
                sheet_instance = AnswerSheet.objects.get(quiz=quiz_instance, contestant=user)
                messages.info(request, 'You have already registered for this quiz')
                return redirect('dashboard')

            except AnswerSheet.DoesNotExist:
                sheet_instance = AnswerSheet()

                sheet_instance.quiz = quiz_instance
                sheet_instance.contestant = user
                sheet_instance.is_valid = True

                sheet_instance.save()
                messages.info(request, 'Best of Luck!! You have been successfully registered.')
                return redirect('dashboard')

        # Get the page
        else:
            context = {'title': 'Register for Quiz', 'quiz': quiz_instance, 'user': user, 'tags': tags_list, 'flag': flag}

        return render(request, 'register_quiz.html', context=context)

    except Quiz.DoesNotExist:
        # No such quiz found in the database
        messages.info(request, 'Quiz does not exists')
        return redirect('dashboard')


# This function returns the correct answer from the database based on the option number saved in database
def switch_objects(question, argument):
    data = {
        'A': question.option_A,
        'B': question.option_B,
        'C': question.option_C,
        'D': question.option_D
    }
    return data.get(argument)


def switch_answers(answer, argument):
    data = {
        'A': answer.response_A,
        'B': answer.response_B,
        'C': answer.response_C,
        'D': answer.response_D
    }
    return data.get(argument)


# Function for ending quiz and Grading Objectives automatically
def end_quiz(request, quizid):
    quiz_object = Quiz.objects.get(quiz_id=quizid)
    user = request.user
    sheet = AnswerSheet.objects.get(quiz=quiz_object, contestant=user)
    quiz_object.users_appeared.add(user)
    answer_list = get_list_or_404(Answer, sheet=sheet)
    subjective_counter = 0

    for answer in answer_list:
        question = Question.objects.get(id=answer.question.id)
        if question.is_subjective:
            subjective_counter = subjective_counter+1
        if question.is_single:
            correct_answer = switch_objects(question, question.correct)
            if answer.response_A is not '':
                answer.marks_awarded = question.marks if correct_answer == answer.response_A else -1*question.negative
                answer.is_graded = True
                answer.save()

        if question.is_multiple:
            correct_options = question.correct.split(';')
            correct_answer = list()
            responses = []
            for option in correct_options:
                correct_answer.append(switch_objects(question, option))
            for arg in ['A', 'B', 'C', 'D']:
                res = switch_answers(answer, arg)
                if res is not '':
                    responses.append(res)

            correct_answer.sort()
            responses.sort()
            if len(responses) != 0:
                answer.marks_awarded = question.marks if correct_answer == responses else -1*question.negative
                answer.is_graded = True
                answer.save()

    sheet.end_time = datetime.now()
    sheet.is_attempted = True
    if subjective_counter == 0:     # Only Multiple choice questions in the quiz
        sheet.is_graded = True
    sheet.save()

    messages.info(request, 'Your Quiz has been Successfully completed')
    return redirect('dashboard')







