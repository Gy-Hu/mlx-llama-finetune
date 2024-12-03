import json
import random
from typing import List, Dict
import os

def convert_conversation(conv_data: Dict) -> Dict:
    """Convert a single conversation to the desired format"""
    messages = [
        {
            "role": "system",
            "content": conv_data["system"]
        }
    ]
    
    # Add conversation pairs
    for conv in conv_data["conversations"]:
        role = "user" if conv["from"] == "human" else "assistant"
        messages.append({
            "role": role,
            "content": conv["value"]
        })
    
    return {"messages": messages}

def process_file(input_file: str, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1):
    """Process the input file and split into train/val/test sets"""
    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert all conversations
    converted_data = []
    for conv_data in data:
        if "conversations" in conv_data:  # Skip any malformed entries
            converted = convert_conversation(conv_data)
            converted_data.append(converted)
    
    # Shuffle data
    random.shuffle(converted_data)
    
    # Calculate split indices
    total = len(converted_data)
    train_size = int(total * train_ratio)
    val_size = int(total * val_ratio)
    
    # Split data
    train_data = converted_data[:train_size]
    val_data = converted_data[train_size:train_size + val_size]
    test_data = converted_data[train_size + val_size:]
    
    # Create output directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Write to files - modified to write one conversation per line
    def write_jsonl(data, filename):
        with open(f"data/{filename}", 'w', encoding='utf-8') as f:
            for item in data:
                json_str = json.dumps(item, ensure_ascii=False)
                f.write(json_str + '\n')
    
    write_jsonl(train_data, "train.jsonl")
    write_jsonl(val_data, "val.jsonl")
    write_jsonl(test_data, "test.jsonl")
    
    # Print statistics
    print(f"Total conversations: {total}")
    print(f"Train set size: {len(train_data)}")
    print(f"Validation set size: {len(val_data)}")
    print(f"Test set size: {len(test_data)}")

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    
    # Process the file
    process_file("raw_data/love_words_collections_system.json")