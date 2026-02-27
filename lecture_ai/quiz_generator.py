from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

_tokenizer = None
_model = None

def generate_quiz_and_flashcards(text: str) -> str:
    """
    Generate simple Q&A pairs (Flashcards) from the summarized text.
    """
    global _tokenizer, _model
    
    try:
        if _tokenizer is None:
            _tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
            _model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
            
        prompt = f"Generate 3 simple question and answer pairs based on the following text:\\n\\nText: {text}\\n\\nQ&A:"
        
        inputs = _tokenizer(prompt, return_tensors="pt", max_length=2000, truncation=True)
        outputs = _model.generate(inputs["input_ids"], max_length=200, num_return_sequences=1)
        qa_output = _tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        formatted_output = "### Auto-Generated Flashcards\\n\\n" + qa_output
        return formatted_output
        
    except Exception as e:
        return f"Could not generate flashcards. Error: {str(e)}"
