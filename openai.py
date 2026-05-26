
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Explain Kubernetes in 3 simple bullet points."}
    ]
)

print(response.choices[0].message.content)