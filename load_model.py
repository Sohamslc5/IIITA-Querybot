import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
os.environ['CURL_CA_BUNDLE'] = ''
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from peft import PeftConfig, PeftModel

peft_model_name = "model"
model_name = "NousResearch/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(peft_model_name)

model = AutoModelForCausalLM.from_pretrained(model_name)
model = PeftModel.from_pretrained(model, peft_model_name)

def generate_response(input_text):
    inputs = tokenizer(input_text, return_tensors="pt")
    inputs_length = len(inputs["input_ids"][0])
    outputs = model.generate(**inputs, max_new_tokens=1024, temperature=0.0001)
    response = tokenizer.decode(outputs[0][inputs_length:], skip_special_tokens=True)
    return response
