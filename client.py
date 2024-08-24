from openai import OpenAI
#pip install openai
client = OpenAI(
    api_key="YOU_API_KEY_HERE"
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Just like Alexa and google cloud."},
        {
            "role": "user",
            "content": "What is freelancing?"
        }
    ]
)

print(completion.choices[0].message.content)