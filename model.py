from pydantic import BaseModel, Field

class Answer(BaseModel):
    """ Represents an answer to a question """

    answer: str = Field(description="The text of the answer. This is what the user will select if the quiz is executed as multiple-choice.")
    is_correct: bool = Field(description="Indicates whether this answer is the correct one.")

class QuizQuestion(BaseModel):
    """ Represents a question in a quiz """

    question: str = Field(description="This is the text of the question that will be presented to the user.")
    answers: list[Answer] = Field(description="A list of possible answers to the question, one of which should be correct.")
    trivia: str = Field(description="Additional information related to the question or the correct answer, such as a fun fact.")