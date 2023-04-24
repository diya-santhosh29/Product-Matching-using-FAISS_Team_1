#!/usr/bin/env python
# coding: utf-8

# Here, we are attempting to determine the similarity between products available on Amazon and Flipkart based solely on their product names.
# Taking the product name from Amazon and comparing it for similarity with the products available on Flipkart.
# Importing flipkart data

import pandas as pd
flipkart_data=pd.read_excel("https://github.com/diya-santhosh29/Product-Matching-using-FAISS_Team_1/blob/main/SmartWatch_Flpikart_5.xlsx?raw=true")
flipkart_data.head(10)


#Vectorization of flipkart data
from sentence_transformers import SentenceTransformer
text = flipkart_data["Product Name"]
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


#importing the Amazon data
Amazon_data=pd.read_excel("https://github.com/diya-santhosh29/Product-Matching-using-FAISS_Team_1/blob/main/smart_watches_amazon.xlsx?raw=true")
Amazon_data.head(10)


#Selecting a specific product's information from the "Name" column and using it as a query for the similarity search.
query=Amazon_data.iloc[2,0]



#converting the selected query product details into vector
import numpy as np
query=Amazon_data.iloc[0,0]
search_text = query
search_vector = encoder.encode(search_text)
_vector = np.array([search_vector])
faiss.normalize_L2(_vector)


#We are searching for the Amazon query in the Flipkart data by using the FAISS index created for the Flipkart products. 
#We will retrieve the closest matching products based on the distance between the query and the Flipkart products' names.

k = 10
distances, ann = index.search(_vector, k=k)

#similarity is calculated
similarity=1/(1+distances)

#We will then store these metrics in a pandas DataFrame for further analysis and visualization
#The ann is the approximate nearest neighbour corresponding to that distance, meaning that ann 0 is the vector at position 0 in the index. Similarly, ann 3 is the vector at position 3 in the index — based on the order of text vectors from step 1.
results = pd.DataFrame({'Similarity' : similarity[0],'Distances': distances[0], 'vector position': ann[0]})


# Function to convert file path into clickable form.
import os as o
def fun(path):
    
    # returns the final component of a url
    f_url = o.path.basename(path)
      
    # convert the url into link
    return '<a href="{}">{}</a>'.format(path, f_url)



#combining the formed dataframe with our flipkart data 
Output=pd.merge(results,flipkart_data,left_on="Vector position",right_index=True)

# applying function "fun" on column "Product Link".
Output = Output.style.format({'Product Link' : fun})
Output






