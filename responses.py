from transformers import pipeline, Conversation

# Initialize the model pipeline for text generation
generator = pipeline("conversational", model="microsoft/DialoGPT-medium")

def get_response(user_input: str) -> str:
    # Use the transformer model to generate a response
    conversation = Conversation(user_input)
    response = generator(conversation, max_length=100, num_return_sequences=1, pad_token_id=50256)
    return response.generated_responses[0]


