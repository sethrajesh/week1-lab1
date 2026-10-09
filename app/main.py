import logging
import traceback
from fastapi import FastAPI, HTTPException
from .models import HealthResponse, TextRequest, TextResponse
from .services import process_task
from .llm_client import get_provider_info

app = FastAPI(
    title="API workbench API",
    description="A multi-task LLM-powered text prcessing service",
    version="1.0.0",
    )

@app.get("/health", response_model=HealthResponse)
def health_check():
    info=get_provider_info()
    return HealthResponse(status="healthy", **info)

@app.post("/summarize") 
def summarize(req: TextRequest):
    # 2. Return a raw dictionary instead of the Pydantic object
    try:
        response_obj = _handle_task("summarize", req.text)
        return response_obj.model_dump() # or .dict() if using Pydantic v1
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Caught endpoint error: {str(e)}")

@app.post("/rewrite", response_model=TextResponse)
def rewrite(req: TextRequest):
    return _handle_task("explain", req.text)

@app.post("/keypoints", response_model=TextResponse)
def keypoints(req: TextRequest):
    return _handle_task("keypoints", req.text)

@app.post("/explain", response_model=TextResponse)
def keypoints(req: TextRequest):
    return _handle_task("explain", req.text)

@app.get("/")
def read_root():
    return {"message": "Welcome to BITS Course Lab 1 API!"}

def _handle_task(task: str, text: str) -> TextResponse:
    try:
        result = process_task(task, text)
        info = get_provider_info()
        return TextResponse(
            task= result["task"],
            result= result["content"],
            model= info["model"],
            tokens_used=result["tokens_used"],
            )
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except EnvironmentError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # This forces the exact error message and line number into your terminal logs
        logging.error("Unhandled error in _handle_task:")
        traceback.print_exc()

        raise HTTPException(
            status_code=500, 
            detail=f"Unhandled application error ({type(e).__name__}): {str(e)}"
        )