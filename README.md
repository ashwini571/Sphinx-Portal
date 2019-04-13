# Sphinx-Portal

## Features

#### 1. Accounts
1. Registration System(Login/Signup).
2. Change Password
3. Forgot password
4. Edit Profile/ Upload Photos
5. Profile for each user containing - :
    * Upcoming Quizzes that the user has registered for
    * Already Attempted Quizzes and their results and graphical **anal**ysis 
6. Separate dashboard for admin and student.  
7.  A student can only have single session on the website.  

#### 2. Quiz Creation And Question adding

1. Student can register for upcoming Quizzes.

2. Quiz Creation
    * Quiz Id and Password automatically generated and sent to the creator via email (Doesn't works behind a Proxy)
    * Specific date and time for Quizzes.
        * Each Quiz can only be attempted at that specified date and time
    * Duration Field for Quizzes
        * Each Quiz can have its separate Duration
    * About and Instructions Field for Quiz. Here additional info for each quiz will be added.
    
2. An Interface for adding Questions

3. A single form can be used to do the following-:
    * Subjective Questions can be added.
    * Objective Question Single-Correct , as well as objective Questions Multi-correct can be added
        * Four options are available
        * Correct Answer field stores one of correct options A, B, C, D or many separated by semicolon A;B
    * Separate field for adding code in Questions. It will show up as `<code>`
    * Images can be added with the Question
    * Link Field for adding extra content or references
    
4. Each Question has it's own time limit

#### 3. Quiz Conduction

1. Cannot take Quiz without password.
2. Quiz will only start at it's own time
3. Questions come one by one without an option to go back.
4. Question Submission without reload.
5. Questions are shuffled up for each user.
6. Timer for Quiz
7. Timer for each Question

#### 4. Quiz Grading

5. Objective Questions are automatically graded on submission of Quiz
6. Separate place in admin panel for grading subjective Questions of the answersheet
6. Leaderboard for each of the Quizzes.


## Technology Stack
* **FRONTEND** : HTML5 , CSS, BOOTSTRAP 4, JavaScript, jQuery ,AJAX
* **BACKEND** : Django

Note - All the additional python lobraries can be installed using requirements.txt


## Installations
* Clone the [Repository](https://github.com/ashwini571/Sphinx-Portal.git)
* Make Sure You have **Python3** installed.
* Do the following - :
    1. `pip install requirements.txt`
    2. `python manage.py makemigrations`
    3. `python manage.py migrate`
    4. `python manage.py runserver`
    5. visit 127.0.0.1:8000
    6. Use `python manage.py collectstatic` to **Collect Static files during the first run as their copy in project root is being ignored**


## Project Info
#### Apps
1. Accounts - For managing signup and authentication of both the admins and the users
2. quiz - For conducting quizzes
3. admin_panel - For creating quizzes and grading them

### Models
| S. No	| Model 	    | App  	  | Description                     |
|-------|---------------|---------|---------------------------------|
|   1.	| User 		    | Account |  AbstractBaseUser               |
|   2.	| Quiz  	    |   Quiz  |  The Quiz model generalised for all kinds of quizzes.   |
|   3.	| Questions  	|   Quiz  |  Each Question will be connected to its Quiz and Each question is generalised to contain all kinds of questions. Subjective as well as objective.|
|   4.  | Answersheet   | Admin Panel | An answersheet for each contestant for every quiz. The Sheet will be created when user registers for the quiz. It will store the marks obtained, time elapsed etc. |
|   5.  | Answer        | Admin Panel | This model will be used to store answers to the questions as well as time elapsed in each questions |


## Contributors
| S. No	| Name 	    | Registration Number|
|-------|-----------|--------------------|
|   1.	| [Ashwini Ojha](https://github.com/ashwini571) 		    |  20175008       |
|   2.	| [Rohit Raj Anand](https://github.com/rht6226) 		    |  20175139       |
|   3.	| [Sheetal Singh](https://github.com/Sheetal-98) 		    |  20175015       |

