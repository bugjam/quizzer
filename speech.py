import openai

def say(prompt):
    with openai.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="echo",
        response_format="aac",
        speed=1.1,
        input=prompt
    ) as response:
        for chunk in response.iter_bytes():
            yield chunk
