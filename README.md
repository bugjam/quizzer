# Quizzer

Quizzer is an AI-based music quiz. It uses OpenAI's API to generate questions, and Spotify's API to explore the player's musical preferences.

Python library dependencies are listed in `requirements.txt`.

API keys for OpenAI, Spotify and LangChain should be defined as environment variables or in `.env`:
```
OPENAI_API_KEY=...
SPOTIPY_CLIENT_ID=...
SPOTIPY_CLIENT_SECRET=...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://eu.api.smith.langchain.com"
LANGCHAIN_API_KEY=...
LANGCHAIN_PROJECT="quizzer"
```

## History

* v1.0 - First playable version with integration to Spotify and OpenAI
* v1.1 - Introduced LangChain to prepare for more "agentic" flows

## Ideas for the future
* Speech output
* Provide artist biography and discography as context instead of relying on the model's training knowledge
* Trigger Spotify playback of relevant music
* Use few-shot learning to create more variation in the questions
* Better adaptation of level of difficulty