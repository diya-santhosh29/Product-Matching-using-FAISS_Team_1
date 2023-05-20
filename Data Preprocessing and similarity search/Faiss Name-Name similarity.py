import pandas as pd
import string
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def preprocess_text_column(df, column_name):
    # Extract the desired column from the DataFrame
    extracted_column = df[column_name].str.lower().str.replace('[{}]'.format(string.punctuation), '')
    extracted_column = extracted_column.str.strip().str.replace('\s+', ' ')
    # Append preprocessed column back to DataFrame
    df[column_name] = extracted_column

def text_to_vector(text):
    # Load the pre-trained Sentence Transformer model
    model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
    # Convert the text into a vector representation
    vector = model.encode(text)
    return vector

def query_fun(column_number):
    # Extract the query from the Amazon data based on the provided column number
    query = amazon_data.iloc[column_number, :]
    return query

def faiss_function(vector):
    # Create the FAISS index and add the vector
    vector_dimension = vector.shape[1]
    index = faiss.IndexFlatL2(vector_dimension)
    faiss.normalize_L2(vector)
    index.add(vector)
    return index

def query_vectorisation(column_index):
    # Vectorize the search text in Flipkart data for a specific column index
    search_text = flipkart_data.iloc[column_number, column_index]
    search_vector = text_to_vector(search_text)
    _vector = np.array([search_vector])
    faiss.normalize_L2(_vector)
    return _vector

# Load the Flipkart and Amazon data
flipkart_data = pd.read_excel("https://github.com/diya-santhosh29/Product-Matching-using-FAISS_Team_1/blob/main/SmartWatch_Flpikart_5.xlsx?raw=true")
amazon_data = pd.read_excel("https://github.com/diya-santhosh29/Product-Matching-using-FAISS_Team_1/blob/main/smart_watches_amazon.xlsx?raw=true")
amazon_data = amazon_data.iloc[:, 0:8]

# Preprocess the text columns in Flipkart and Amazon data
preprocess_text_column(flipkart_data, "Product Name")
preprocess_text_column(amazon_data, "Name")

# Vectorize the title in Flipkart data
name_vector = text_to_vector(flipkart_data["Product Name"])

# Perform FAISS indexing on the name vector
index = faiss_function(name_vector)
# Get the column number from the user
column_number = int(input("Enter the index"))

# Create a DataFrame for the query
a_query = pd.DataFrame(query_fun(column_number)).T

# Extract the brand of the query
brand_of_query = a_query.iloc[0, 2]

# Extract details of smartwatches belonging to the brand of the query
flipkart_data_same_brand = flipkart_data[flipkart_data["Brand"] == brand_of_query]

# Perform vectorization and FAISS indexing of the query
query_vector = query_vectorisation(2)

# Search for similar products and calculate similarity
distances, ann = index.search(query_vector, k=index.ntotal)
similarity = 1 / (1 + distances)

# Create a DataFrame for the search results
results = pd.DataFrame({'Similarity': similarity[0], 'distances': distances[0], 'vector position': ann[0]})
products_same_brand = pd.merge(results, flipkart_data_same_brand, left_on="vector position", right_index=True)

# Filter similar products based on conditions
condition1 = products_same_brand["Similarity"] > 0.75
condition2 = products_same_brand["Strap Color"] == a_query.iloc[0, 5]
similar_products = products_same_brand[condition1 & condition2]

# Create the final concatenated DataFrame
column1 = a_query["link"].reset_index(drop=True)
column2 = a_query["Name"].reset_index(drop=True)
column3 = similar_products['Product Link'].reset_index(drop=True)
column4 = similar_products['Product Name'].reset_index(drop=True)




results = pd.DataFrame({'Query Product Link': column1, 'Query Product Name': column2,
                             'Similar Product Name': column3, 'Similar Products': column4})

# Replace NaN values with empty strings
results.fillna('', inplace=True)

# Save the result to a CSV file
results.to_csv('match_results{}.csv'.format(column_number), index=False)
