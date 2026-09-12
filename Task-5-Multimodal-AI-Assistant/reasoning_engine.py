import ollama


# -----------------------------------
# Step 1: Validate the Vision Response
# -----------------------------------

def validate_response(question, draft_answer, history):

    history_text = ""

    for msg in history[-6:]:
        history_text += f"{msg['role']}: {msg['content']}\n"

    validator_prompt = f"""
You are a response validation system for a multimodal AI assistant.

Your job is to check whether the draft answer is reliable and appropriate.

User Question:
{question}

Conversation History:
{history_text}

Draft Answer:
{draft_answer}

Check the draft answer using these rules:

1. Does it answer the user's question?
2. Does it avoid unsupported assumptions?
3. Does it distinguish observation from speculation?
4. Does it handle uncertainty correctly?
5. Is the reasoning logical?
6. Does it avoid inventing information?

Return your result in this format:

VALIDATION: PASS or REVISE

REASON:
Give a short explanation of your validation.

FINAL ANSWER:
Give the corrected and reliable answer.
"""

    response = ollama.chat(
        model="llama3:latest",
        messages=[
            {
                "role": "user",
                "content": validator_prompt
            }
        ]
    )

    return response["message"]["content"]