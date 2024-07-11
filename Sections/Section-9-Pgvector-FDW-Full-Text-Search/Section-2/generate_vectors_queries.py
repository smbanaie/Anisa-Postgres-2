import json
from gpt4all import GPT4All, Embed4All


try:

    # Initialize Embed4All
    embedder = Embed4All()
    pgvector_desc = embedder.embed("sleep disorders")
    print(pgvector_desc)

except Exception as e:
    print(f"Error: {e}")
