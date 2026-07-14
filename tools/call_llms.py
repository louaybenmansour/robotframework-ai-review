"""
Appelle les LLM configures (Gemini / Claude / ChatGPT) sur tout le dataset
(bad/medium/good) avec chaque version de prompt disponible.

Structure attendue:
    dataset/bad/*.robot
    dataset/medium/*.robot
    dataset/good/*.robot
    prompts/prompt_v*.md

Resultats sauvegardes dans:
    results/<llm>/<prompt_version>/<categorie>__<nom_script>.md

Usage:
    python3 tools/call_llms.py
"""

import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

DATASET_DIR = pathlib.Path("dataset")
CATEGORIES = ["bad", "medium", "good"]
PROMPTS_DIR = pathlib.Path("prompts")
RESULTS_DIR = pathlib.Path("results")

GEMINI_MODEL = "gemini-2.5-flash"
CLAUDE_MODEL = "claude-sonnet-4-6"
OPENAI_MODEL = "gpt-4o"


def is_configured(value):
    if not value:
        return False
    placeholders = ["your_", "_here", "xxxx"]
    return not any(p in value.lower() for p in placeholders)


ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")

USE_CLAUDE = is_configured(ANTHROPIC_KEY)
USE_CHATGPT = is_configured(OPENAI_KEY)
USE_GEMINI = is_configured(GOOGLE_KEY)

anthropic_client = None
openai_client = None

if USE_CLAUDE:
    import anthropic
    anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

if USE_CHATGPT:
    import openai
    openai_client = openai.OpenAI(api_key=OPENAI_KEY)

if USE_GEMINI:
    import google.generativeai as genai
    genai.configure(api_key=GOOGLE_KEY)


def read_file(path):
    return path.read_text(encoding="utf-8")


def call_claude(prompt, code):
    message = anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1500,
        messages=[{"role": "user", "content": f"{prompt}\n\n```robot\n{code}\n```"}],
    )
    return message.content[0].text


def call_chatgpt(prompt, code):
    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": f"{prompt}\n\n```robot\n{code}\n```"}],
    )
    return response.choices[0].message.content


def call_gemini(prompt, code):
    import google.generativeai as genai
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(f"{prompt}\n\n```robot\n{code}\n```")
    return response.text


def find_robot_scripts():
    """Retourne une liste de (categorie, chemin) pour chaque script .robot du dataset."""
    scripts = []
    for category in CATEGORIES:
        category_dir = DATASET_DIR / category
        if not category_dir.exists():
            continue
        for robot_file in sorted(category_dir.glob("*.robot")):
            scripts.append((category, robot_file))
    return scripts


def main():
    prompt_files = sorted(PROMPTS_DIR.glob("prompt_v*.md"))
    scripts = find_robot_scripts()

    if not prompt_files:
        print("Aucun fichier prompt_v*.md trouve dans prompts/")
        return
    if not scripts:
        print("Aucun script .robot trouve dans dataset/bad, dataset/medium ou dataset/good")
        return

    print("LLM actifs :")
    print(f"  Claude  : {'OUI' if USE_CLAUDE else 'non'}")
    print(f"  ChatGPT : {'OUI' if USE_CHATGPT else 'non'}")
    print(f"  Gemini  : {'OUI' if USE_GEMINI else 'non'}")
    print(f"\n{len(prompt_files)} version(s) de prompt x {len(scripts)} script(s) a traiter\n")

    if not (USE_CLAUDE or USE_CHATGPT or USE_GEMINI):
        print("Aucune cle API valide. Remplis au moins GOOGLE_API_KEY dans .env")
        return

    for prompt_path in prompt_files:
        prompt_version = prompt_path.stem
        prompt_text = read_file(prompt_path)

        for category, script_path in scripts:
            script_name = script_path.stem
            code = read_file(script_path)
            output_name = f"{category}__{script_name}.md"
            print(f"=== {prompt_version} | {category}/{script_name} ===")

            if USE_CLAUDE:
                out_dir = RESULTS_DIR / "claude" / prompt_version
                out_dir.mkdir(parents=True, exist_ok=True)
                try:
                    result = call_claude(prompt_text, code)
                    (out_dir / output_name).write_text(result, encoding="utf-8")
                    print("  Claude : OK")
                except Exception as e:
                    print(f"  Claude : ERREUR - {e}")

            if USE_CHATGPT:
                out_dir = RESULTS_DIR / "chatgpt" / prompt_version
                out_dir.mkdir(parents=True, exist_ok=True)
                try:
                    result = call_chatgpt(prompt_text, code)
                    (out_dir / output_name).write_text(result, encoding="utf-8")
                    print("  ChatGPT : OK")
                except Exception as e:
                    print(f"  ChatGPT : ERREUR - {e}")

            if USE_GEMINI:
                out_dir = RESULTS_DIR / "gemini" / prompt_version
                out_dir.mkdir(parents=True, exist_ok=True)
                try:
                    result = call_gemini(prompt_text, code)
                    (out_dir / output_name).write_text(result, encoding="utf-8")
                    print("  Gemini : OK")
                except Exception as e:
                    print(f"  Gemini : ERREUR - {e}")

    print("\nTermine. Resultats dans results/<llm>/<prompt_version>/")


if __name__ == "__main__":
    main()
