from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Go to /help to print paths for API"}

@app.get("/stig_lookup/{stig}")
async def stig_lookup(stig: str):
    if stig[0].lower() != "v":
        stig = f"V-{stig}"
    return {"message": f"You want to look up {stig}?"}

@app.post("/question")
async def stig_question(data: dict):
    question = data["question"]
    return {"message": f"Here is your question: {question}"}

@app.post("/keyword_search")
async def keyword_search(data: dict):
    words = data["keywords"]
    return {"message": f"Here are the words: {words}"}

@app.get("/help")
async def helper():
    return [
        "/ :: Haven't decided yet",
        "/stig_lookup/{STIG ID} :: Looks up the STIG ID provided and returns all of the STIG data",
        "/question :: Send a question to the API with json {\"question\": \"question here\"}",
        "/keyword_search :: Send a list of words to the API with json {\"keywords\": [\"word\", \"word2\"]}",
        "/help :: Prints this menu"
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)