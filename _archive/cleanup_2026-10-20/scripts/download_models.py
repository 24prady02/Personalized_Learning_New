"""
Script to download pre-trained models
"""

from transformers import AutoModel, AutoTokenizer


def download_models():
    """Download required pre-trained models"""
    
    print("Downloading CodeBERT...")
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base")
    print("✓ CodeBERT downloaded")
    
    print("Downloading BERT...")
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModel.from_pretrained("bert-base-uncased")
    print("✓ BERT downloaded")
    
    print("All models downloaded successfully!")


if __name__ == "__main__":
    download_models()

















