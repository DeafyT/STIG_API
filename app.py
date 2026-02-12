from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from Controller import logic, intelligence
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Go to /help to print paths for API"}

@app.post("/stig_lookup/{stig}")
async def stig_lookup(stig: str, data: dict):
    if data["list"] == "none":
        file = logic.find_stig(stig)
        return {"message": file}
    else:
        stig_data = logic.find_stig(stig, data["list"])
        stig_data = logic.beautify_stig(stig_data)
        return {"message": stig_data}

@app.post("/keyword_search")
async def keyword_search(data: dict):
    words = data["keywords"]
    stig_list = data["stig"]
    stigs = logic.keyword_search(words, stig_list)
    return {"message": f"STIGs listed with keywords: {stigs}"}

@app.post("/available_STIG_lists")
async def stig_lists(data: dict):
    if data["list"] == "none":
        stig_list = None
    else:
        stig_list = data["list"]
    stigs = logic.list_files(stig_list)
    final_stig = logic.beautify_file(stigs)
    return {"message": final_stig}

@app.post("/load_STIG_ids")
async def stig_ids(data: dict):
    ids_list = logic.list_ids(data["list"])
    return {"message": ids_list}

@app.post("/question/{stig}")
async def stig_question(data: dict, stig: str):
    question = data["question"]
    stig_data = logic.find_stig(stig)
    return EventSourceResponse(intelligence.ask_ai(stig_data, question))

@app.post("/output_analysis/{stig}")
async def output_analysis(data: dict, stig: str):
    output = data["results"]
    stig_data = logic.find_stig(stig)
    return EventSourceResponse(intelligence.ai_analysis(stig_data, output))

@app.get("/help")
async def helper():
    return [
        "/ :: Haven't decided yet",
        "/stig_lookup/{STIG ID} :GET: Looks up the STIG ID provided and returns all of the STIG data",
        "/question/{STIG ID} :POST: Send a question to the AI with json {\"question\": \"question here\"}",
        "/keyword_search :POST: Send a list of words to the API with json {\"keywords\": [\"word\", \"word2\"], \"stig\": \"stig id\"}",
        "/available_STIG_lists :POST: Provides list of STIGs with json {\"list\": \"none\"} will return all lists",
        "/output_analysis/{STIG ID} :POST: Send your STIG output to the AI for analysis on whether or not you meet requirements {\"results\": \"results here\"}",
        "/help :: Prints this menu"
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)