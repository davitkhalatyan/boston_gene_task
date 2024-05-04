from fastapi import FastAPI
from find_hla import find_hla, equal_ignore_order
from find_genes import find_genes
from pydantic import BaseModel
import requests
import threading
import uvicorn
import json


class TextInput(BaseModel):
    text: str


def start_server():
    uvicorn.run(app, port=8070)


app = FastAPI()


@app.post("/")
async def recognize_genes_and_hla(txt: TextInput):

    gene_results = find_genes(txt.text)
    hla_results = find_hla(txt.text)

    return {"genes": gene_results["genes"], "hla": hla_results["hla"]}


if __name__ == "__main__":

    server_thread = threading.Thread(target=start_server)
    server_thread.start()

# Sending a test request
    with open('test_texts.json', 'r') as json_file:

        # Load JSON data from the file
        texts = json.load(json_file)

        for text in texts:
            test_text = text["text"]
            response = requests.post("http://localhost:8070", json={"text": test_text})
            print(response.json())

            # Checking if the response matches the expected format
            assert equal_ignore_order(response.json()['genes'], text["genes"]) and \
                   equal_ignore_order(response.json()['hla'], text['hla'])
