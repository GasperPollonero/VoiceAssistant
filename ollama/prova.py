import ollama
from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='gemma3:1b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky red?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)