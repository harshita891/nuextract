import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class NuExtractModel:
    def __init__(self, model_name="numind/NuExtract-1.5"):
        try:
            self.device = torch.device("cuda")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)
            self.model.eval()
        except Exception as e:
            raise RuntimeError(f"Model initialization failed: {e}")

    def extract(self, text, json_template):
        try:
            prompt = f"Extract information in JSON format:\nText: {text}\nTemplate: {json_template}\nOutput: "
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

            with torch.no_grad():
                output = self.model.generate(**inputs, max_new_tokens=512)

            extracted_text = self.tokenizer.decode(output[0], skip_special_tokens=True)

            extracted_json = json.loads(extracted_text.split("Output: ")[-1])
        except json.JSONDecodeError:
            extracted_json = {"error": "Failed to parse model output"}
        except Exception as e:
            extracted_json = {"error": f"Extraction failed: {e}"}

        return {"text": text, "extracted_info": extracted_json}
