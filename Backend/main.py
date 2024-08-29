import os
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image
import pytesseract
import io
import asyncio
from functools import lru_cache
import concurrent.futures
import time
import logging
from groq import Groq

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Define the directory for static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Create a ThreadPoolExecutor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)

# Groq API configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")
groq_client = Groq(api_key=GROQ_API_KEY)

class SummarizeRequest(BaseModel):
    texts: list[str]

@lru_cache(maxsize=128)
def get_tesseract_config():
    """Cache the Tesseract configuration."""
    return r'--oem 3 --psm 6'

def process_image(image_bytes: bytes) -> str:
    """Process the image and extract text using OCR."""
    try:
        start_time = time.time()
        image = Image.open(io.BytesIO(image_bytes))
        logger.info(f"Image opened in {time.time() - start_time:.4f} seconds")

        start_time = time.time()
        image = image.convert('L')
        logger.info(f"Image converted to grayscale in {time.time() - start_time:.4f} seconds")
        
        start_time = time.time()
        custom_config = get_tesseract_config()
        text = pytesseract.image_to_string(image, config=custom_config)
        logger.info(f"OCR processing done in {time.time() - start_time:.4f} seconds")
        
        return text
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise e

async def summarize_text(text: str) -> str:
    """Summarize the given text using Groq."""
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Please provide a concise summary of the following text:\n\n{text}",
                }
            ],
            model="llama3-8b-8192",
            max_tokens=150,
            temperature=0.5,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error summarizing text: {str(e)}")
        raise e

@app.get("/")
async def serve_index():
    return FileResponse("Frontend/app.html")

@app.post("/ocr")
async def ocr_and_summarize(file: UploadFile = File(...)):
    start_time = time.time()
    
    if not file.filename.lower().endswith(('png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif')):
        logger.warning("Invalid file type uploaded")
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image file.")
    
    image_bytes = await file.read()

    try:
        logger.info(f"Received image file '{file.filename}' of size {len(image_bytes)} bytes")
        
        loop = asyncio.get_running_loop()
        text = await loop.run_in_executor(executor, process_image, image_bytes)
        
        summary = await summarize_text(text)
        
        latency = time.time() - start_time
        logger.info(f"Total request processing time: {latency:.4f} seconds")
        
        return JSONResponse(content={"text": text, "summary": summary, "latency": latency})
    except Exception as e:
        logger.error(f"Error during OCR processing or summarization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize_batch")
async def summarize_batch(request: SummarizeRequest):
    try:
        summaries = await asyncio.gather(*[summarize_text(text) for text in request.texts])
        return JSONResponse(content={"summaries": summaries})
    except Exception as e:
        logger.error(f"Error during batch summarization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, workers=4)
