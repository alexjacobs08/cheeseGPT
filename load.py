import json

from langchain.vectorstores.redis import Redis
from langchain.embeddings import OpenAIEmbeddings

# Load texts and metadata
texts = json.load(open('texts.json'))
metadata = json.load(open('metadata.json'))

# Generate embeddings and load into Redis
embeddings = OpenAIEmbeddings()
rds = Redis.from_texts(
    texts,
    embeddings,
    metadatas=metadata,
    redis_url="redis://localhost:6379",
    index_name="cheese",
)
