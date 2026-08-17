import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def create_vector_db():
    """
    Create the vector database.
    Currently this function is kept for compatibility
    with main.py.
    """
    return True


def get_qa_chain():
    """
    Returns a customer-service question answering function.
    """

    def chain(question):
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=f"""
You are a professional customer service chatbot.

Answer the customer's question politely and clearly.

Customer-service information:

- Customers can check order status using their order ID.
- Products can be returned within 7 days if unused and in original condition.
- Refunds are processed after the returned product is received and inspected.
- Orders can be cancelled before they are shipped.
- Standard delivery usually takes 3 to 5 business days.
- Payment methods include credit cards, debit cards, UPI and net banking.
- Damaged products should be reported to customer support.
- Customer support helps with orders, payments, delivery, returns,
  refunds and cancellations.

Customer question:
{question}

Give a helpful answer.
"""
        )

        return response.text

    return chain