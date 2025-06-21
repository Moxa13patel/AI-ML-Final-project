from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# ✅ Load fine-tuned model (use checkpoint if necessary)
model_path = "moxa-ai-13/fine_tuned_dialoGPT"  # or "./fine_tuned_dialoGPT/checkpoint-9408" if needed

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)

# ✅ Add special tokens (must match training)
special_tokens_dict = {"additional_special_tokens": ["<|user|>", "<|bot|>"]}
tokenizer.add_special_tokens(special_tokens_dict)

# Load model
model = AutoModelForCausalLM.from_pretrained(model_path)
model.resize_token_embeddings(len(tokenizer))  # adjust embedding size for new tokens

# Store chat history (optional for context)
chat_history_ids = None
OFFENSIVE_KEYWORDS = ["hate", "stupid", "kill", "idiot", "die", "hang"]

def contains_offensive_language(text):
    text = text.lower()
    return any(word in text for word in OFFENSIVE_KEYWORDS)

def generate_response(user_input, prev_chat_history=None):
    if contains_offensive_language(user_input):
        return "Let's keep things respectful. Please avoid offensive language.", prev_chat_history

    # Prepare prompt
    prompt = f"<|user|> {user_input} <|bot|>"
    new_input_ids = tokenizer.encode(prompt, return_tensors='pt')

    # Combine with previous history if any
    bot_input_ids = (
        torch.cat([prev_chat_history, new_input_ids], dim=-1)
        if prev_chat_history is not None else new_input_ids
    )

    # Generate response
    output_ids = model.generate(
        bot_input_ids,
        max_new_tokens=80,  # This controls *response length only*, not total
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=40,
        top_p=0.95,
        temperature=0.7,
        eos_token_id=tokenizer.eos_token_id
    )

    # Decode only new part
    generated_tokens = output_ids[:, bot_input_ids.shape[-1]:]
    bot_reply = tokenizer.decode(generated_tokens[0], skip_special_tokens=True).strip()

    # Fallback for blank or gibberish
    if not bot_reply.strip() or any(char.isdigit() for char in bot_reply[:10]):
        bot_reply = "I'm here for you. Want to share more about how you're feeling?"

    return bot_reply, output_ids



