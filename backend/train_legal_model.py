import torch
from datasets import Dataset
from transformers import T5ForConditionalGeneration, T5Tokenizer, Trainer, TrainingArguments
from legal_dataset import LEGAL_DATA

def train_model():
    print("Starting the model training process...")


    dataset = Dataset.from_list(LEGAL_DATA)


    model_name = "t5-small"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    def tokenize_data(examples):
        inputs = tokenizer(examples["input"], padding="max_length", truncation=True, max_length=128)
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(examples["target"], padding="max_length", truncation=True, max_length=128)
        
        inputs["labels"] = labels["input_ids"]
        return inputs

    tokenized_dataset = dataset.map(tokenize_data, batched=True)
    
    print("Dataset has been tokenized.")


    training_args = TrainingArguments(
        output_dir="./legal_grammar_model_output",
        num_train_epochs=10,
        per_device_train_batch_size=2,
        save_strategy="epoch",
        logging_dir='./logs',
        learning_rate=3e-4,
        weight_decay=0.01,
    )


    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )


    print("Fine-tuning the model...")
    trainer.train()
    print("Training complete.")


    model.save_pretrained("./legal_grammar_model")
    tokenizer.save_pretrained("./legal_grammar_model")
    print("Model saved successfully to './legal_grammar_model'")

if __name__ == "__main__":
    train_model()
