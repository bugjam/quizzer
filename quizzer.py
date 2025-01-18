import json
import random
import model
import ai

use_ai = True

def new_conversation(instructions=''):
    conversation = [ ("system", f"You are a Walensio, the quizzmaster in a music quiz show. {instructions}") ]
    return conversation

def welcome_message():
    if use_ai:
        prompt = "Create a witty and welcoming opening line for the Quizzer show. Start with the phrase 'Hello and welcome to Quizzer. I am your host, Walensio.'"
        return ai.ask(prompt, new_conversation())
    else:
        return "Hello and welcome to Quizzer. I am your host, Walensio. Get ready to test your musical knowledge and wit as we embark on a melodious journey filled with trivia and tunes! Let's see who will hit all the right notes and emerge as today's ultimate music maven. Welcome, music enthusiasts!"
    
class ArtistsQuiz:
    def __init__(self, artists):
        self.artists = list(artists)
        self.conversation = new_conversation('You will adapt the difficulty of questions depending on the performance of the contestant.')
        self.question_number = 0
        self.correct_answers = 0

    def ask_question(self):
        #self.conversation = new_conversation()
        artist = random.choice(self.artists)
        prompt = f"Ask a new question about {artist} and provide 4 possible answers."
        question = ai.ask(prompt, self.conversation, output_type=model.QuizQuestion)
        random.shuffle(question.answers)
        self.question = question
        self.question_number += 1
        return question

    def check_answer(self, answer):
        c = self.question.answers[answer].is_correct
        if c:
            self.correct_answers += 1
        return c
    
    def correct_answer(self):
        return [a.is_correct for a in self.question.answers].index(True)