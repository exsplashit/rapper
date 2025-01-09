from dynaconf import settings
import openai
from transformers import pipeline


class Generator:
    def __init__(self):
        self.use_openai = settings.llm.use_openai
        self.model_name = settings.llm.model_name
        if not self.use_openai:
            self.generator = pipeline("text-generation", model=self.model_name)

    def generate(self, prompt):
        if self.use_openai:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "system", "content": prompt}],
            )
            return response.choices[0].message["content"]
        else:
            return self.generator(prompt, max_length=200, num_return_sequences=1)[0][
                "generated_text"
            ]
