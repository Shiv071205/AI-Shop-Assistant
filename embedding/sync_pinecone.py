import os
import time
import mysql.connector 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from pandas import col
from pinecone import Pinecone,ServerlessSpec
from tqdm.auto import tqdm
import pandas as pd

load_dotenv()


#pinecone configuration

api_key=os.getenv("PINECONE_API_KEY")
pc=Pinecone(api_key=api_key)


spec=ServerlessSpec(
    cloud="aws",region="us-east-1"
)


index = "shop-assistant"

if index in [i["name"] for i in pc.list_indexes()]:
    pc.delete_index(index)
    print("Old index deleted.")

existing_indexes = [
    index_info["name"]
    for index_info in pc.list_indexes()
]

#check  if index a;ready exists

if index not in existing_indexes:
    pc.create_index(
        name=index,
        dimension=3072,
        metric='dotproduct',
        spec=spec
    )

while not pc.describe_index(index).status['ready']:
    print(f"Waiting for the index{index} to be ready...")
    time.sleep(5)


#connect to the pinecone index
indexes=pc.Index(index)
time.sleep(1)

#connect to mysql database
db_connection=mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="shopassistant"
)

cursor= db_connection.cursor()

#googgle api key 
os.environ['GOOGLE_API_KEY']=os.getenv("GOOGLE_API_KEY")
embed_Model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

test = embed_Model.embed_query("hello")
print("Embedding size =", len(test))

def fetch_data():
    query="SELECT * FROM products"
    cursor.execute(query)
    data=cursor.fetchall()
    columns=[col[0] for col in cursor.description]
    df=pd.DataFrame(data,columns=columns)
    return df

def sync_with_pinecone(data):
    batch_size=10
    total_batches=(len(data)+batch_size-1)//batch_size

    for i in tqdm(range(0, len(data), batch_size), desc="Processing Batches", unit="batch", total=total_batches):
        i_end=min(i+batch_size,len(data))
        batch=data[i:i+batch_size]
        
        #unique id 
        ids=[str(row['ProductID']) for _,row in batch.iterrows()]
         #combine text fields into a single string for embedding
        texts=[
            f"Product Name: {row['ProductName']}, Product Brand: {row['ProductBrand']}, Gender: {row['Gender']}, Description: {row['Description']}, Price: {row['Price']}"
        
        for _,row in batch.iterrows()
        ]
        #embed text
        embeds=embed_Model.embed_documents(texts)
        time.sleep(35)

        metadata=[{
            "ProductName":row['ProductName'],
            "Description":row['Description'],
            "Price":row['Price'],
            "ProductBrand":row['ProductBrand'],
            "Gender":row['Gender']
        } for _,row in batch.iterrows()]
        print(metadata[0])
        #upsert to pinecone
        with tqdm(total=len(ids), desc="Upserting to Pinecone", unit="vector") as upsert_vector:
                indexes.upsert(vectors=zip(ids,embeds,metadata))
                upsert_vector.update(len(ids))

def main():
    data=fetch_data()
    sync_with_pinecone(data)
    print("Data synchronization with Pinecone completed successfully.")

if __name__=="__main__":
    main()

cursor.close()
db_connection.close()
