import torch
from transformers import T5ForConditionalGeneration,T5Tokenizer

class parainfer:

    def __init__(self):
        torch.manual_seed(1)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        print("Loading T5 model")
        self.model = T5ForConditionalGeneration.from_pretrained('./paraphrase/quora_paws_model')
        self.tokenizer = T5Tokenizer.from_pretrained('t5-base')
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
        print("T5 ready")

    def generate(self, sentence):
        sourcetext =  "paraphrase: " + sentence + " </s>"

        max_len = 256

        encoding = self.tokenizer.encode_plus(sourcetext, padding=True, return_tensors="pt")
        input_ids, attention_masks = encoding["input_ids"].to(self.device), encoding["attention_mask"].to(self.device)

        output = self.model.generate(
            input_ids=input_ids, attention_mask=attention_masks,
            do_sample=True,
            max_length=max_len,
            top_k=120,
            top_p=0.98,
            early_stopping=True,
            num_return_sequences=20
        )
        
        final_outputs = []
        for item in output:
            sent = self.tokenizer.decode(item, skip_special_tokens=True, clean_up_tokenization_spaces=True)
            if sent.lower() != sentence.lower() and sent not in final_outputs:
                final_outputs.append(sent)

        return final_outputs
