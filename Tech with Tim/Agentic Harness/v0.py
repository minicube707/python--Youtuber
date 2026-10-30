import sys

sys.stdout.reconfigure(encoding='utf-8') #Only for Windows

from openai import OpenAI

client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
MODEL = "qwen3:1.7b"


def chat(user_message: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful personal assistant."},
            {"role": "user", "content": user_message},
        ]
    )
    
    # print(f"\nresponse={response.model_dump_json(indent=2)}")
    return response.choices[0].message.content or ""


if __name__ == "__main__":

    print(f"v0 assistant {MODEL} - ctr+c to quit")

    try:
        while True:
            question = input("\nyou: ")
            print("\nassistant: ", chat(question))

    except (EOFError, KeyboardInterrupt):
        print("\nbye!")
