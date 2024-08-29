from transformers import AutoModelForCausalLM, AutoTokenizer

def load_moondream_model():
    model_id = "vikhyatk/moondream2"
    revision = "2024-08-26"
    model = AutoModelForCausalLM.from_pretrained(
        model_id, trust_remote_code=True, revision=revision
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    return model, tokenizer

# Initialize the model and tokenizer
moondream_model, moondream_tokenizer = load_moondream_model()
