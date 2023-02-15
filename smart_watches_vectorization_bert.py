from transformers import BertModel, BertTokenizer
import pandas as pd
import numpy as np

# Load the pre-trained BERT model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)

# Load the e-commerce dataset
data = pd.read_csv("/home/futures/smart_watches_amazon.csv")

# Vectorize the e-commerce data using BERT
embeddings = []
for text in data['Brand']:
    inputs = tokenizer.encode_plus(text, add_special_tokens=True, return_tensors='pt')
    outputs = bert_model(**inputs)
    embedding = outputs.last_hidden_state[:, 0, :].detach().numpy()
    embeddings.append(embedding)
embeddings = np
