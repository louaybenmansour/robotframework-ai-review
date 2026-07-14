import os
from dotenv import load_dotenv
import anthropic
import openai
import google.generativeai as genai

load_dotenv()

anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def call_claude(prompt, code):
    message = anthropic_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{"role": "user", "content": f"{prompt}\n\n```robot\n{code}\n```"}]
    )
    return message.content[0].text

def call_chatgpt(prompt, code):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"{prompt}\n\n```robot\n{code}\n```"}]
    )
    return response.choices[0].message.content

def call_gemini(prompt, code):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(f"{prompt}\n\n```robot\n{code}\n```")
    return response.text

def read_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_script(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    prompt = read_prompt("prompts/prompt_v1.md")
    code = read_script("scripts-analyses/anonymises/login_test_01.robot")

    print("=== CLAUDE ===")
    print(call_claude(prompt, code))

    print("\n=== CHATGPT ===")
    print(call_chatgpt(prompt, code))

    print("\n=== GEMINI ===")
    print(call_gemini(prompt, code))