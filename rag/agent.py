from dynaconf import settings


class Agent:
    def __init__(self, retriever, generator):
        self.retriever = retriever
        self.generator = generator
        self.agent_prompt = settings.agent.prompt

    def answer(self, query):
        documents, metadata = self.retriever.retrieve(query)
        context = "\n\n".join(documents)
        prompt = (
            f"{self.agent_prompt}\n\nContext:\n{
                context}\n\nQuery:\n{query}\n\nAnswer:"
        )
        return self.generator.generate(prompt)
