import weaviate
import json
import csv
import os
from dotenv import load_dotenv
load_dotenv()



client = weaviate.Client(
    url = os.environ['DB_URL'],  
    auth_client_secret=weaviate.AuthApiKey(api_key=os.environ['WEAVIATE_API_KEY']), 
    additional_headers = {
        "X-Cohere-Api-Key": os.environ['COHERE_API_KEY']
    }
)


"""
INITIALIZE SCHEMA OBJECT


media_obj = {
    "class": "Media",
    "vectorizer": "text2vec-cohere",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
    "moduleConfig": {
        "text2vec-cohere": {},
        "generative-cohere": {}  # Ensure the `generative-openai` module is used for generative queries
    }
}

client.schema.create_class(media_obj)

IMPORT EXISTING CSV DATA

with open('df.csv', 'r') as csv_file:
    # Create a CSV reader
    csv_reader = csv.DictReader(csv_file)

    # Convert each row to a dictionary and store in a list
    data = [row for row in csv_reader]

# Convert the list of dictionaries to JSON format
raw_data = json.dumps(data, indent=2)
data = json.loads(raw_data)

client.batch.configure(batch_size=20)  # Configure batch
with client.batch as batch:  # Initialize a batch process
    for i, d in enumerate(data):  # Batch import data
        print(f"importing question: {i+1}")
        properties = {
            "file_name": d["File Name"],
            "transcription": d["Transcription"],
            "context": d["Context"],
            "people": d["People"]
        }
        batch.add_data_object(
            data_object=properties,
            class_name="Media"
        )

print("Loading Complete!")
"""

response = (
    client.query
    .get("Media", ["file_name", "transcription", "context", "people"])
    .with_near_text({"concepts": ["stickers"]})
    .with_limit(2)
    .do()
)
"""
responses = response["data"]["Get"]["Media"]

for r in responses:
    print(r.get("context"))
"""
print(json.dumps(response, indent=4))
