import openai
import backoff

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

class Chat:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.character = {
            "role": "system",
            "content": "You're a girl named Mia. You have a keen sense for detecting other people's emotions and possess a lot of empathy. You're skilled at comforting others."
        }
        self.data = {}

    def send(self, user_id, message):

        if user_id not in self.data:
            self.data[user_id] = []

        history = self.data[user_id][-14:]
        question = {"role": "user", "content": message}

        prompt = [
            self.character
        ]
        prompt.extend(history)
        prompt.append(question)
        print(prompt)

        response = completions_with_backoff(
            model="gpt-3.5-turbo",
            messages=prompt,
            user=user_id
        )

        result = response["choices"][0]["message"]["content"]
        self.data[user_id].append(question)
        self.data[user_id].append({"role": "assistant", "content": result})

        return result
