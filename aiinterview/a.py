import requests

url = "http://localhost:1337/v1/chat/completions"
headers = {
    "Content-Type": "application/json"
}
data = {
    "model": "llama3.2:1b",
    "messages": [
        {
            "role": "user",
            "content": '''You are a senior Python technical interviewer.

Generate 5 interview questions about Python programming.  
For each question, also generate 1 follow-up question that digs deeper.

Strictly output only a following JSON object:

{
  "questions": [
    {
      "main": "Main question here",
      "follow_up": "Follow-up question here"
    },
    ...
  ]
}
            '''
        }
    ],
    "temperature": 0.8,
    "max_tokens": 4096
}

res = requests.post(url, headers=headers, json=data)
