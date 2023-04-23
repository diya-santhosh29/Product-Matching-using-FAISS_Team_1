#!/usr/bin/env python
# coding: utf-8

# Here, we are attempting to determine the similarity between products available on Amazon and Flipkart based on their complete details, including the product name, brand, price, color, model, and so on



# importing flipkart data 
import pandas as pd
flipkart_data=pd.read_csv(r"C:\Users\Arishma\Downloads\SmartWatch_Flpikart_5 (2).csv")
flipkart_data.head(10)


# We do not need the product link column for vectorization. 
# Other columns are concatenated into a single string format for vectorization.
cols_to_group = ['Brand', 'Product Name', 'Discounted Price', 'Original Price', 'Product Rating', 'Strap Color', 'Model', 'Size']
# Creating a  new column by concatenating  the data from the selected columns
flipkart_data['Product_whole_details'] = flipkart_data[cols_to_group].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)
# Drop the original column that were used for grouping
flipkart_data.drop(cols_to_group, axis=1, inplace=True)



#Vectorization of flipkart data
from sentence_transformers import SentenceTransformer
text = flipkart_data["Product_whole_details"]
encoder = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
vectors = encoder.encode(text)
vectors.shape




#Creating FAISS indexes for Flipkart data based on Euclidean distance.
#Normalization is done to avoid distance from 0 to infinite
import faiss
vector_dimension = vectors.shape[1]
index = faiss.IndexFlatL2(vector_dimension)
faiss.normalize_L2(vectors)
index.add(vectors)


# Importing amazon data 
Amazon_data=pd.read_csv(r"C:\Users\Arishma\Amazon.csv")
Amazon_data



#Selecting a specific product's information from the "Name" column and using it as a query for the similarity search.
query=Amazon_data.iloc[2,0]
query


#converting the selected query product details into vector
import numpy as np
query=Amazon_data.iloc[0,0]
search_text = query
search_vector = encoder.encode(search_text)
_vector = np.array([search_vector])
faiss.normalize_L2(_vector)



#We are searching for the Amazon query in the Flipkart data by using the FAISS index created for the Flipkart products. 
#We will retrieve the closest matching products based on the distance between the query and the Flipkart products' names.
k = index.ntotal
distances, ann = index.search(_vector, k=k)
#similarity is calcualted 
similarity=1/(1+distances)



#We will then store these metrics in a pandas DataFrame for further analysis and visualization
#The ann is the approximate nearest neighbour corresponding to that distance, meaning that ann 0 is the vector at position 0 in the index. Similarly, ann 3 is the vector at position 3 in the index — based on the order of text vectors from step 1.results = pd.DataFrame({'Similarity' : similarity[0],'distances': distances[0], 'vector position': ann[0]})
results = pd.DataFrame({'Similarity' : similarity[0],'Distances': distances[0], 'vector position': ann[0]})


# Function to convert file path into clickable form.
import os as o
def fun(path):
    
    # returns the final component of a url
    f_url = o.path.basename(path)
      
    # convert the url into link
    return '<a href="{}">{}</a>'.format(path, f_url)


#combining the formed dataframe with our flipkart data 
Output=pd.merge(results,flipkart_data,left_on="vector position",right_index=True)
Output = Output.style.format({'Product Link' : fun})
Output







