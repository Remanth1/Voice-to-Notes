from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

_tokenizer = None
_model = None

def summarize_text(text: str) -> str:
    """
    Summarize a long transcript using Hugging Face's BART model.
    """
    global _tokenizer, _model
    
    # Load model once and cache it
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        _model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
    
    max_chunk_size = 1000
    chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    
    summaries = []
    for chunk in chunks:
        if len(chunk) < 50:
            continue
            
        try:
            inputs = _tokenizer(chunk, max_length=1024, return_tensors="pt", truncation=True)
            summary_ids = _model.generate(inputs["input_ids"], max_length=150, min_length=30, do_sample=False)
            summary_text = _tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(summary_text)
        except Exception:
            summaries.append(chunk)

    final_summary = " ".join(summaries)
    return final_summary if final_summary else "No summary could be generated."
