# Multimodal AI Assistant

## Overview

This project is a multimodal AI assistant that can understand both text and image inputs. It analyzes visual content, maintains conversation context, handles ambiguity, provides evidence-based responses, and validates its answers.

## Technologies Used

- Python
- Streamlit
- Ollama
- Qwen3-VL 4B
- Llama 3
- Pillow

## AI Models

### Vision Model
Qwen3-VL 4B is used to analyze uploaded images and generate a draft response.

### Validation Model
Llama 3 is used as a separate validation layer to check the response for unsupported assumptions, logical errors, and unreliable information.

## How It Works

1. User uploads an image.
2. User asks a question.
3. Qwen3-VL 4B analyzes the image.
4. The model generates a draft answer.
5. Llama 3 validates the draft answer.
6. The validated response is displayed to the user.
7. Conversation history is maintained for follow-up questions.

## Key Features

- Image understanding
- Text-based interaction
- Contextual reasoning
- Ambiguity handling
- Evidence-based responses
- Response validation
- Intelligent decision-making
- Conversation history

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt