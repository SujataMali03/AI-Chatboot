import ollama

print("Connecting to Ollama...")

try:
    response = ollama.chat(
        model="llama3:latest",
        messages=[
            {
                "role": "user",
                "content": "What is machine learning? Explain in two sentences."
            }
        ]
    )

    print("\nResponse received!")
    print(response)

except Exception as e:
    print("\nERROR:")
    print(type(e).__name__)
    print(e)