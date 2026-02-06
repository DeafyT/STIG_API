from fastapi import FastAPI
from Controller import logic

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Go to /help to print paths for API"}

@app.get("/stig_lookup/{stig}")
async def stig_lookup(stig: str):
    if stig[0].lower() != "v":
        stig = f"V-{stig}"
    return {"message": f"You want to look up {stig}?"}

@app.post("/question/{stig}")
async def stig_question(data: dict, stig: str):
    question = data["question"]
    return {"message": f"Here is your question for {stig}: {question}"}

@app.post("/keyword_search")
async def keyword_search(data: dict):
    words = data["keywords"]
    stig_list = data["stig"]
    return {"message": f"Here are the words: {words}"}

@app.post("/available_STIG_lists")
async def stig_lists(data: dict):
    stig_list = None
    if data is not None:
        stig_list = data["stig"]
    return {"message": "Will print off all STIG lists available or STIG lists with keyword in name"}

@app.post("/output_analysis")
async def output_analysis(data: dict):
    output = data["results"]
    return {"message": f"Here is your STIG output you provided : {output}"}

@app.get("/help")
async def helper():
    return [
        "/ :: Haven't decided yet",
        "/stig_lookup/{STIG ID} :: Looks up the STIG ID provided and returns all of the STIG data",
        "/question/{STIG ID} :: Send a question to the AI with json {\"question\": \"question here\"}",
        "/keyword_search :: Send a list of words to the API with json {\"keywords\": [\"word\", \"word2\"]}",
        "/available_STIG_lists :: Will provide a list of all available STIG lists",
        "/output_analysis :: Send your STIG output to the AI for analysis on whether or not you meet requirements",
        "/help :: Prints this menu"
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)