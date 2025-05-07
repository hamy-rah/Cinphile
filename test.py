import openai
client = openai.OpenAI(api_key="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")

response = client.models.list()
print(response)

