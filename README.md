# AI-ML-Final-project
mental health chatbot
This project is a conversational AI chatbot designed to offer supportive and empathetic responses to users facing mental health challenges. It uses Hugging Face's DialoGPT model, fine-tuned on an empathy-focused dataset to provide context-aware and emotionally intelligent replies.

## Features
Conversational chatbot with chat history support for context

Fine-tuned on the EmpatheticDialogues dataset for empathetic responses

Offensive language filtering to maintain respectful communication

Custom backend using Flask API

Interactive frontend using Streamlit

Modular design for easy expansion and deployment

Technology Stack
Python

Hugging Face Transformers and Datasets

PyTorch

DialoGPT-medium (fine-tuned)

Flask (REST API backend)

Streamlit (Web UI)

## Folder Structure
bash
Copy
Edit
├── app/
│   ├── chatbot.py          # Chat logic using fine-tuned model
│   ├── routes.py           # Flask route for message handling
├── frontend/
│   └── streamlit_app.py    # Streamlit interface
├── fine-tune.py            # Fine-tuning script for DialoGPT
├── dialoGPT_empathetic/    # Directory with saved fine-tuned model
├── main.py                 # Flask app entry point
└── requirements.txt
## How to Run
Clone the repository and install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Start the Flask backend:

bash
Copy
Edit
python main.py
In a new terminal, launch the Streamlit frontend:

bash
Copy
Edit
streamlit run frontend/streamlit_app.py
Fine-Tuning Overview
The chatbot uses a fine-tuned version of microsoft/DialoGPT-medium, trained on the empathetic_dialogues dataset. The model was trained using Hugging Face's Trainer API with custom preprocessing and tokenization settings to handle conversation turns effectively.

## Future Enhancements
Add journaling and mood-tracking functionality

Deploy on platforms like Render or Hugging Face Spaces

Enable multilingual support

Implement escalation to a human therapist for critical queries

