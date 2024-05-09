import json
import random
import ai

use_ai = True

def new_conversation(instructions=''):
    conversation = [ { "role": "system", "content": f"You are a Walensio, the quizzmaster in a music quiz show. {instructions}"}]
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
        prompt = (f"Create a question about {artist} and provide 4 possible answers."
                  "Format your reponse as JSON like this:"
                  "{\"question\": \"Who are the members of bla bla?\", "
                  " \"answers\": [\"First option\", \"Second option\", \"Third option\", \"Fourth option\"]}")
        jquestion = ai.ask(prompt, self.conversation, expect_json=True)
        question = json.loads(jquestion)
        random.shuffle(question["answers"])
        self.answers = question["answers"]
        self.question_number += 1
        return question

    def check_answer(self, answer):
        prompt = (f"Given the answer {answer}, "
                            "determine if the answer is correct. "
                            "Format your reponse as JSON like this:"
                            "{\"correct\": true, \"message\": \"The answer is correct\" "
                            " \"trivia\": \"Album 1 was the first album to reach a top 10 position\" }")
        
        jfeedback = ai.ask(prompt, self.conversation, expect_json=True)
        feedback = json.loads(jfeedback)

        if feedback["correct"]:
            self.correct_answers += 1
        
        return feedback