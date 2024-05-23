import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, PeftModel
from trl import SFTTrainer
from datasets import load_dataset

model_name = "NousResearch/Llama-2-7b-chat-hf"

dataset = load_dataset("sohamslc5/dataset", split = "train")

token = "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"

bnb_config = BitsAndBytesConfig(
    load_in_4bit = True,
    bnb_4bit_quant_type = "nf4",
    bnb_4bit_compute_dtype = torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    use_safetensors = True,
    use_auth_token=True,
    quantization_config = bnb_config,
    trust_remote_code = True,
    device_map = 'auto'
)

model.config.use_cache = False
model.config.pretraining_tp = 1

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_state = 'right'

peft_config = LoraConfig(
    lora_alpha = 16,
    r = 64,
    lora_dropout = 0.1,
    bias = "none",
    task_type = "CAUSAL_LM"
)

training_arguments = TrainingArguments(
    output_dir = "./checkpoint_dir",
    num_train_epochs = 2,
    per_device_train_batch_size = 2,
    gradient_accumulation_steps = 1,
    optim = "adamw_torch",
    logging_steps = 30,
    learning_rate = 2e-5,
    lr_scheduler_type = "cosine",
    max_steps = -1,
    warmup_ratio = 0.3,
    weight_decay = 0.001,
    evaluation_strategy = "steps",
    eval_steps = 0.2,
    save_safetensors = True,
    per_device_eval_batch_size = 2,
)


trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    peft_config = peft_config,
    dataset_text_field = 'text',
    max_seq_length = 4096,
    args = training_arguments,
    train_dataset = dataset,
    eval_dataset = dataset,
)

trained = trainer.train()
new_model="model"
trainer.model.save_pretrained(new_model)
print("Model Saved Locally")

tokenizer.save_pretrained(new_model)
print("Tokenizer Saved Locally")

print("Execution done")



























