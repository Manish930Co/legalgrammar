from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load the fine-tuned model and tokenizer from the local directory
MODEL_PATH = "./legal_grammar_model"
tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)

def correct_legal_text(text: str) -> str:
    """
    Takes a string of legal text and corrects it using the fine-tuned model.
    """
    # Prepare the input text with the required prefix
    input_text = f"fix grammar: {text}"
    
    # Tokenize the input
    inputs = tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True)
    
    # Generate the output from the model
    outputs = model.generate(
        inputs.input_ids, 
        max_length=128, 
        num_beams=4, 
        early_stopping=True
    )
    
    # Decode the generated tokens back to a string
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return corrected_text
