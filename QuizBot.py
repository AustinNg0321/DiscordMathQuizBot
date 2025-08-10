# MathQuizBot is a discord bot that generates simple math quizzes for users
#
# Functionalities:
# -> Viewing and modifying settings, including the number of questions, the greatest number possibly included
# in the questions, the allowed operations, and whether negative numbers/results are allowed.
# -> Generating a random quiz based on the settings (only the user can write the quiz).
# -> Viewing scores, quiz reports, and statistics
# -> Asking ChatGPT to explain a certain question
#
# Documentations:
# -> https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#
# -> https://discordpy.readthedocs.io/en/latest/api.html
# -> https://www.w3schools.com/python/default.asp

import os
import asyncio
import openai
from dotenv import load_dotenv
import discord
from discord.ext import commands
from numpy import random

# Getting and setting the keys/tokens from .env
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_KEY

# Initializing the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


"""
Question class: 

Stores information of a simple expression with 2 numbers and a +, -, *, or / operator, e.g. 1 + 1
The result of the expression can be found upon calling get_result, e.g. returns 2 if the question is 1 + 1
"""
class Question:
    def __init__(self, num1, num2, operator):
        self._num1 = num1
        self._num2 = num2

        # Allow only +, -, *, / operators
        if operator not in Settings.allowed_operations:
            raise Exception("Operator not supported! The only operations supported are + " +
                            "(addition), - (subtraction), * (multiplication), and / (division)!")
        else:
            self._operator = operator

    def __str__(self):
        return f"{self._num1} {self._operator} {self._num2} = ? "

    # Returns the result of the question based on the operator
    def get_result(self):
        match self._operator:
            case "+":
                return self._num1 + self._num2
            case "-":
                return self._num1 - self._num2
            case "*":
                return self._num1 * self._num2
            case "/":
                return self._num1 / self._num2
            case _:
                return None


"""
Settings class:

Contains the settings of a Quiz (a series of Questions) wrapped in a class: including the number of questions,
the greatest number possibly included in the questions, the allowed operations, and whether negative numbers/results
are allowed.

Each of the above property can be viewed and modified.
"""
class Settings:
    # Allow only +, -, *, / operators.
    allowed_operations = ["+", "-", "*", "/"]

    # Default settings
    def __init__(self):
        self._num_questions = 10
        self._max_num = 10
        self._operations = ["+", "-", "*", "/"]
        self._allow_negative = False  # no negative numbers/results included

    def __str__(self):
        return f"Number of questions: {self._num_questions}\nMaximum number: {self._max_num}\nOperations included: {self._operations}\nAllow negatives: {self._allow_negative}\n"

    def get_num_questions(self):
        return self._num_questions

    def get_max_num(self):
        return self._max_num

    def get_operations(self):
        return self._operations

    def get_negative(self):
        return self._allow_negative

    def set_num_questions(self, num_questions):
        if num_questions > 0:
            self._num_questions = num_questions
        else:
            raise Exception("The quiz must have at least 1 question!")

    def set_max_num(self, max_num):
        if max_num > 0:
            self._max_num = max_num
        else:
            raise Exception("The maximum number must be positive!")

    # Filter out all illegal operators and update the allowed operations if provided with
    # at least 1 of +, -, *, / operators
    def set_operations(self, operations):
        legal_operations = []
        for operator in operations:
            if operator in Settings.allowed_operations and operator not in legal_operations:
                legal_operations.append(operator)
        if len(legal_operations) == 0:
            raise Exception("Please enter one or more allowed operators (+, -, *, /)!")
        else:
            self._operations = legal_operations

    def set_negative(self, allow_negative):
        self._allow_negative = allow_negative


"""
Quiz class:

Contains the questions and settings of a math quiz.
The questions are initially empty and have to be generated with a generate_quiz function.
"""
class Quiz:
    allowed_operations = ["+", "-", "*", "/"]

    def __init__(self, settings):
        self._settings = settings
        self._questions = []

    def __str__(self):
        quiz = f"Math Quiz ({self._settings.get_num_questions()} questions): \n"
        for i in range(len(self._questions)):
            quiz += f"{i + 1}. {self._questions[i]} \n"
        return quiz

    def get_settings(self):
        return self._settings

    def get_questions(self):
        return self._questions

    def update_settings(self, settings):
        self._settings = settings

    # Generates a quiz: a set number of questions with the applied settings
    def generate_quiz(self):
        self._questions.clear()
        num_questions = self._settings.get_num_questions()
        max_num = self._settings.get_max_num()
        operations = self._settings.get_operations()
        allow_negative = self._settings.get_negative()

        for i in range(num_questions):
            # Choosing a random operator out of the included operations
            operator = random.choice(operations)

            # Generated division equations always evaluate to integers, so the second number is generated first
            # and a multiple of the second number is generated for the first number
            if operator == "/":
                num2 = random.randint(1, max_num + 1)
                num1 = random.randint(0, max_num // num2)
                num1 = num1 * num2
                if allow_negative:
                    if random.randint(0, 2):
                        num1 = -1 * num1
                    if random.randint(0, 2):
                        num2 = -1 * num2
            else:
                if allow_negative:
                    num1 = random.randint(-1 * max_num, max_num + 1)
                    num2 = random.randint(-1 * max_num, max_num + 1)
                else:
                    num1 = random.randint(0, max_num + 1)
                    num2 = random.randint(0, max_num + 1)

                    if operator == "-" and num1 < num2:
                        temp = num1
                        num1 = num2
                        num2 = temp

            self._questions.append(Question(num1, num2, operator))


async def main():
    """
    Stores user data
    Since there are no databases connected to this program, everything resets once the bot is re-run
    Format ... user: {settings: ..., quiz: ..., user_answers: [...], score: ...}
    """
    user_sessions = {}

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

    # Sends the error message when a command cannot be run due to an error
    @bot.event
    async def on_command_error(ctx, exception):
        await ctx.send(str(exception))

    # Helper function
    async def add_user_session(user):
        if user not in user_sessions:
            user_settings = Settings()
            user_sessions[user] = {  # auto-insertion
                "settings": user_settings,  # default settings
                "quiz": Quiz(user_settings),  # load settings stored in database!!!
                "user_answers": [],
                "score": 0,
                "num_attempted": 0,
                "num_correct": 0
            }

    # Runs before any command is executed
    # If the user is not found in the data (USER_SESSIONS), initialize user settings and add user into the data
    @bot.before_invoke
    async def func(ctx):
        await add_user_session(ctx.author)

    @bot.command()
    async def view_settings(ctx):
        cur_settings = user_sessions[ctx.author]["settings"]
        await ctx.send(f"{ctx.author}'s settings:\n{cur_settings}")

    @bot.command()
    async def change_num_questions(ctx, num: int):
        cur_settings = user_sessions[ctx.author]["settings"]
        cur_settings.set_num_questions(num)
        await ctx.send(f"Number of questions on {ctx.author}'s quiz changed to {cur_settings.get_num_questions()}.")

    @bot.command()
    async def change_max_num(ctx, num: int):
        cur_settings = user_sessions[ctx.author]["settings"]
        cur_settings.set_max_num(num)
        await ctx.send(f"Maximum number of {ctx.author}'s quiz changed to {cur_settings.get_max_num()}.")

    # Gets the list of operators entered and update the included operators
    # Sends an error message if the method fails
    @bot.command()
    async def set_operations(ctx, *operators):
        cur_settings = user_sessions[ctx.author]["settings"]
        operations = []
        for operator in operators:
            operations.append(operator)

        try:
            cur_settings.set_operations(operations)
            await ctx.send(f"Operations now included in {ctx.author}'s quiz: {cur_settings.get_operations()}.")
        except Exception as e:
            await ctx.send(str(e))

    # Allow negative numbers/results in questions
    @bot.command()
    async def allow_negatives(ctx):
        cur_settings = user_sessions[ctx.author]["settings"]
        cur_settings.set_negative(True)
        await ctx.send(f"Negative numbers are now allowed on {ctx.author}'s quiz.")

    # Disallow negative numbers/results in questions
    @bot.command()
    async def disallow_negatives(ctx):
        cur_settings = user_sessions[ctx.author]["settings"]
        cur_settings.set_negative(False)
        await ctx.send(f"Negative numbers are now not allowed on {ctx.author}'s quiz.")

    # Update user data and generate a quiz based on user settings
    # We currently allow duplicate questions to be generated
    async def generate_quiz(ctx):
        cur_quiz = user_sessions[ctx.author]["quiz"]
        cur_settings = user_sessions[ctx.author]["settings"]
        cur_quiz.update_settings(cur_settings)
        cur_quiz.generate_quiz()
        await ctx.send(f"{ctx.author}'s quiz generated successfully.")

    # Starts writing a quiz
    @bot.command()
    async def start(ctx):
        # check function
        def check_user(msg):
            return msg.author == ctx.author

        # Updating/Resetting certain data before starting a new quiz
        quiz = user_sessions[ctx.author]["quiz"]
        user_answers = user_sessions[ctx.author]["user_answers"]
        questions = quiz.get_questions()
        score = 0
        user_answers.clear()

        await generate_quiz(ctx)
        await ctx.send(f"--- {ctx.author}'s Math Quiz ---")
        for i in range(len(questions)):
            # Printing the questions one by one
            await ctx.send(f"{ctx.author}: {i + 1}. {questions[i]}")

            # Keeps repeating the current question until the user gives a valid answer (an integer)
            answered = False
            while not answered:
                # the check ensures other users can't interfere with quiz-writing
                msg = await bot.wait_for("message", check=check_user)
                try:
                    user_input = int(msg.content)
                    if user_input == questions[i].get_result():
                        score = score + 1
                    await ctx.send(f"{ctx.author} entered {user_input} for question {i + 1}.")
                    answered = True
                    user_answers.append(user_input)
                except Exception as e:
                    await ctx.send(e)

        await ctx.send(
            f"{ctx.author}'s quiz completed. Score: {score} / {len(questions)} ({score * 100 / len(questions)}%).")

        user_sessions[ctx.author]["score"] = score
        user_sessions[ctx.author]["num_correct"] = user_sessions[ctx.author]["num_correct"] + score
        user_sessions[ctx.author]["num_attempted"] = user_sessions[ctx.author]["num_attempted"] + len(questions)

    # Prints a report of the last quiz taken
    @bot.command()
    async def view_report(ctx):
        quiz = user_sessions[ctx.author]["quiz"]
        score = user_sessions[ctx.author]["score"]
        user_answers = user_sessions[ctx.author]["user_answers"]
        questions = quiz.get_questions()

        if len(user_answers) == 0:
            await ctx.send("Please write a quiz before viewing the quiz report!")
        else:
            report = f"--- Quiz Report ---\n{ctx.author} scored {score} / {len(questions)} ({score * 100 / len(questions)}%).\n"
            for i in range(len(questions)):
                report = report + f"{i + 1}. {questions[i]}\n User entered {user_answers[i]}. The correct answer is {questions[i].get_result()}.\n"
            await ctx.send(report)

    @bot.command()
    async def view_stats(ctx):
        num_attempted = user_sessions[ctx.author]["num_attempted"]
        num_correct = user_sessions[ctx.author]["num_correct"]

        if num_attempted == 0:
            await ctx.send(f"{ctx.author} has not written any quizzes yet.")
        else:
            await ctx.send(
                f"{ctx.author}'s stats:\nQuestions attempted: {num_attempted}\nQuestions answered correctly: {num_correct} ({num_correct * 100 / num_attempted}%)")

    @bot.command()
    async def reset_stats(ctx):
        user_sessions[ctx.author]["num_attempted"] = 0
        user_sessions[ctx.author]["num_correct"] = 0
        user_sessions[ctx.author]["user_answers"].clear()
        await ctx.send(f"{ctx.author}'s stats successfully reset.")

    # Gets a response directly from a specific ChatGPT model ("gpt-3.5-turbo")
    # Returns the error message if the method fails
    def get_chatgpt_response(prompt):
        try:
            # add custom instructions: chatbot is not specifically tailored to answer math questions for now ...
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    # Structures a prompt for a specific question on the quiz and ask ChatGPT for a response
    @bot.command()
    async def explain_question(ctx, question_no: int):
        quiz = user_sessions[ctx.author]["quiz"]
        questions = quiz.get_questions()

        if 1 <= question_no <= len(questions):
            await ctx.send("Thinking ...")

            # Structuring the prompt
            cur_equation = str(questions[question_no - 1])
            cur_equation = cur_equation[:-2] + str(questions[question_no - 1].get_result()) + "?"

            # Response from ChatGPT
            response = get_chatgpt_response(f"Can you explain why {cur_equation}")
            await ctx.send(response)
        else:
            await ctx.send("Invalid question number!")

    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
