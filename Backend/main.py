import asyncio
import concurrent.futures
import io
import logging
import time
from functools import lru_cache

import pytesseract
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create a ThreadPoolExecutor
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

@lru_cache(maxsize=128)
def get_tesseract_config():
    """Cache the Tesseract configuration."""
    return r'--oem 3 --psm 3'

def preprocess_image(image: Image.Image) -> Image.Image:
    """Preprocess the image for better OCR results."""
    image = image.convert('L')  # Convert to grayscale
    return image.resize((image.width // 2, image.height // 2))  # Resize

def process_image(image_bytes: bytes) -> str:
    """Process the image and extract text using OCR."""
    try:
        with Image.open(io.BytesIO(image_bytes)) as image:
            logger.info(f"Image opened, size: {image.size}")
            
            image = preprocess_image(image)
            logger.info("Image preprocessed")
            
            custom_config = get_tesseract_config()
            text = pytesseract.image_to_string(image, config=custom_config)
            logger.info("OCR processing completed")
        
        return text
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise

@app.get("/")
async def serve_index():
    """Serve the main HTML page."""
    return FileResponse("static/app.html")

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    """Endpoint for OCR processing."""
    start_time = time.time()
    
    if not file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
        logger.warning("Invalid file type uploaded")
        raise HTTPException(status_code=400, detail="Invalid file type. Only image files are allowed.")
    
    image_bytes = await file.read()

    try:
        logger.info(f"Received image file '{file.filename}' of size {len(image_bytes)} bytes")
        
        loop = asyncio.get_running_loop()
        text = await loop.run_in_executor(executor, process_image, image_bytes)
        
        latency = time.time() - start_time
        logger.info(f"Total request processing time: {latency:.4f} seconds")
        
        return JSONResponse(content={"text": text, "latency": latency})
    except Exception as e:
        logger.error(f"Error during OCR processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, workers=4)
