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

