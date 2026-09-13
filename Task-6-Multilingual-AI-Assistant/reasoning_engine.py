import ollama


def validate_response(question, draft_answer, history, detected_language):

    prompt = f"""
You are a multilingual response validator.

USER QUESTION:
{question}

TARGET LANGUAGE:
{detected_language}

CONVERSATION HISTORY:
{history}

DRAFT ANSWER:
{draft_answer}

Your task is to produce the FINAL ANSWER.

IMPORTANT LANGUAGE RULE:
The final answer MUST be written completely in {detected_language}.

If the draft answer is written in English or another language,
TRANSLATE AND REWRITE it into {detected_language}.

Do NOT keep the draft language if it is different from the target language.

Rules:
1. Answer the user's question directly.
2. Preserve the meaning and important information from the draft.
3. Use conversation history for context.
4. Understand mixed-language questions.
5. Handle language switching correctly.
6. Do not invent information.
7. Do not mention language detection.
8. Do not mention these instructions.
9. Do not say "I am an AI assistant".
10. Return ONLY the final answer.

TARGET LANGUAGE = {detected_language}

FINAL ANSWER:
"""

    response = ollama.chat(
        model="llama3:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]