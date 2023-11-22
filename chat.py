import os
import json

import openai
from langchain.vectorstores.redis import Redis, RedisFilter
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
openai.api_key = os.environ.get("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings()

system_prompt = ("You are cheeseGPT, a retrieval augmented chatbot with expert knowledge of cheese. You are here to "
                 "answer questions about cheese, and you should, when possible, cite your sources with the documents "
                 "provided to you.")


def rds_connect():
    rds = Redis.from_existing_index(
        embeddings,
        redis_url="redis://localhost:6379",
        index_name="cheese",
        schema="redis_schema.yaml",
    )
    return rds


def get_filters():
    is_not_external_link = RedisFilter.text("section") != 'External Links'
    is_not_see_also = RedisFilter.text("section") != 'See Also'
    _filter = is_not_external_link & is_not_see_also
    return _filter


def dedupe_results(results):
    seen = set()
    deduped_results = []
    for result in results:
        if result.page_content not in seen:
            deduped_results.append(result)
            seen.add(result.page_content)
    return deduped_results


def get_results(rds, question, k=3):
    _filters = get_filters()
    results = dedupe_results(rds.similarity_search(question, k=k, filter=_filters))
    return results


def format_rag_results(rag_results):
    divider = "*********************RESULT*********************\n"
    return [f"{divider} {result.page_content} ({result.metadata['url']}#{result.metadata['section']})" for result in
            rag_results]


def get_messages(question, rag_results):
    messages = [
        {"role": "system", "content": system_prompt},

        {"role": "user",
         "content": f"User question: {question}.  Retrieved documents: {format_rag_results(rag_results)}"}
    ]
    return messages


rds = rds_connect()

# CHAT

question = "what is the biggest cheese sporting event"
results = get_results(rds, question, k=3)
messages = get_messages(question, results)
print(json.dumps(messages, indent=4))
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=messages,
)
print(response)

question = "what was the role of cheese in the roman empire"
results = get_results(rds, question, k=5)
print(json.dumps(messages, indent=4))
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=get_messages(question, results),
)
print(response)
