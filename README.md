Purpose:
=========
The MathQuizBot is a Discord bot created to generate and manage simple math quizzes for users. It allows users to customize the quiz settings, such as the number of questions and types of operations, while providing instant feedback and explanations for their answers. The bot aims to enhance users' math skills in an engaging and interactive manner.


Setup:
======
Users must have a Discord bot token and an OpenAI API key, which are stored in a .env file.  
Required libraries must be installed.  


Commands:
=========
  !start: Begins a new quiz based on user settings.  
  !view_settings: Displays current quiz settings.  
  !change_num_questions <number>: Changes the number of questions.  
  !change_max_num <number>: Sets the maximum number for questions.  
  !set_operations <operators>: Updates allowed operations (+, -, *, /).  
  !allow_negatives: Permits negative numbers in questions.  
  !disallow_negatives: Disallows negative numbers.  
  !view_report: Shows the results of the last quiz.  
  !view_stats: Displays overall statistics.  
  !reset_stats: Resets user statistics.  
  !explain_question <number>: Requests an explanation for a specific question using ChatGPT.  


User Interaction:
=================
Users interact with the bot through commands within Discord, receiving quizzes, feedback, and explanations in real time.


Technologies and Libraries/Frameworks
=====================================
Python: The programming language used to develop the bot.  
Discord.py: A Python library that enables interaction with the Discord API to build bots and manage Discord servers.  
OpenAI API: Used to access ChatGPT for generating explanations for quiz questions.  
dotenv: A library for loading environment variables from a .env file, which holds sensitive information like API keys.  
Numpy: Used for generating random numbers to create quiz questions.  
Asyncio: A Python library for writing asynchronous code, allowing the bot to handle multiple operations concurrently without blocking.  


Main Functions and Routines
=====================================  
main():  
The main asynchronous function that initializes the bot, sets up user sessions, and handles events.  

on_ready():  
An event handler that prints a message to the console when the bot has successfully logged in.  

on_command_error(ctx, exception):  
An event handler that sends an error message to the Discord channel if a command fails to execute.  

add_user_session(user):  
A helper function that initializes a new user session with default settings if the user is not already in the session data.

func(ctx):  
A routine that runs before any command is invoked, ensuring that user sessions are initialized.


Command Functions  
=====================================   
view_settings(ctx):  
Sends the current quiz settings of the user to the Discord channel.  

change_num_questions(ctx, num: int):  
Changes the number of questions in the user's quiz and sends a confirmation message.  

change_max_num(ctx, num: int):  
Updates the maximum number that can be used in questions and sends a confirmation message.  

set_operations(ctx, *operators):  
Updates the allowed mathematical operations for the quiz and sends a confirmation message. Handles errors if illegal operations are provided.  

allow_negatives(ctx):  
Allows negative numbers in quiz questions and sends a confirmation message.  

disallow_negatives(ctx):  
Disallows negative numbers in quiz questions and sends a confirmation message.  

generate_quiz(ctx):  
Generates a quiz based on the user's settings and updates the quiz object.  

start(ctx):  
Begins a new quiz session, prompts the user with questions, and records answers until the quiz is completed. Sends the final score to the user.  

view_report(ctx):  
Generates and sends a report of the user's last quiz, including correct answers and user responses.  

view_stats(ctx):  
Displays overall statistics for the user, including the number of questions attempted and answered correctly.  

reset_stats(ctx):  
Resets the user's quiz statistics and sends a confirmation message.  

get_chatgpt_response(prompt):  
Sends a prompt to the OpenAI API and retrieves a response. Handles errors and returns error messages if needed.  

explain_question(ctx, question_no: int):  
Requests an explanation for a specific quiz question from ChatGPT and sends the response to the user. Verifies the question number's validity before proceeding.  

