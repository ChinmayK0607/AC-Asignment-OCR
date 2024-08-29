# OCR and Summarization Web Application

This project implements a web-based Optical Character Recognition (OCR) application that allows users to upload images, extract text from them, and obtain a summary of the extracted text using AI.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies and Libraries Used](#technologies-and-libraries-used)
4. [Project Structure](#project-structure)
5. [Setup and Installation](#setup-and-installation)
6. [Usage](#usage)
7. [Architecture and Workflow](#architecture-and-workflow)
8. [Performance Optimization](#performance-optimization)
9. [Error Handling and Logging](#error-handling-and-logging)
10. [Stress Testing](#stress-testing)
11. [Future Improvements](#future-improvements)

## Project Overview

This application provides a web interface for users to upload images, extract text using OCR technology, and obtain an AI-generated summary of the extracted text. It processes the images on the server-side and returns the extracted text, summary, and performance metrics.

## Features

- Web-based user interface for image upload
- Server-side OCR processing using Tesseract
- Text summarization using Groq AI
- Real-time display of extracted text, summary, and processing latency
- Optimized image processing for improved OCR accuracy
- Concurrent request handling
- Error handling and user feedback
- Stress testing capabilities

## Technologies and Libraries Used

- **Backend**:
  - FastAPI: For creating the web server and API endpoints
  - Pillow (PIL): For image processing
  - pytesseract: For OCR functionality
  - Groq: For text summarization
  - uvicorn: ASGI server for running the FastAPI application

- **Frontend**:
  - HTML5
  - JavaScript (Vanilla JS)
  - CSS3

- **Testing**:
  - requests: For sending HTTP requests in stress testing
  - concurrent.futures: For concurrent execution of requests

## Project Structure

```
ocr_project/
├── main.py              # FastAPI application, OCR logic, and summarization
├── static/
│   └── app.html         # Web interface
├── stress_test.py       # Stress testing script
├── images/              # Folder to store test images for stress testing
└── README.md            # Project documentation
```

## Setup and Installation

1. Install the required Python packages:
   ```bash
   pip install fastapi uvicorn python-multipart pillow pytesseract groq requests
   ```

2. Install Tesseract OCR on your system:
   - For Ubuntu: `sudo apt-get install tesseract-ocr`
   - For macOS: `brew install tesseract`
   - For Windows: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

3. Set up your Groq API key:
   - Sign up for a Groq account and obtain your API key
   - Set the `GROQ_API_KEY` variable in `main.py` with your API key

4. Prepare test images:
   - Create an `images` folder in the project directory
   - Add some test images (PNG, JPG, JPEG) to this folder for stress testing

## Usage

1. Start the backend server:
   ```bash
   python main.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Use the interface to upload an image and see the extracted text and summary

4. To run the stress test:
   ```bash
   python stress_test.py
   ```

## Architecture and Workflow

1. **Frontend**:
   - User uploads an image through the web interface
   - JavaScript handles the file upload and sends it to the backend
   - Displays loading indicators, results, and error messages

2. **Backend**:
   - FastAPI server receives the uploaded image
   - Image is processed using PIL and converted to grayscale
   - Tesseract OCR extracts text from the processed image
   - Extracted text is sent to Groq AI for summarization
   - Results (extracted text, summary, and latency) are sent back to the frontend

3. **OCR Processing**:
   - Uses pytesseract with optimized configuration
   - Converts image to grayscale for better OCR accuracy

4. **Summarization**:
   - Utilizes Groq AI to generate a concise summary of the extracted text

## Performance Optimization

- **Concurrent Processing**: ThreadPoolExecutor is used to handle multiple requests concurrently
- **Caching**: Tesseract configuration is cached using `lru_cache` to avoid repeated setup
- **Asynchronous Operations**: FastAPI's asynchronous capabilities are utilized for non-blocking I/O operations
- **Image Preprocessing**: Grayscale conversion improves OCR accuracy without resizing

## Error Handling and Logging

- Comprehensive error handling in both frontend and backend
- Detailed logging of operations and errors for easier debugging and monitoring
- User-friendly error messages displayed in the web interface

## Stress Testing

The `stress_test.py` script performs the following:

- Sends multiple concurrent requests to the OCR endpoint
- Measures individual request latencies and overall throughput
- Calculates and reports various performance metrics:
  - Average, minimum, and maximum latency
  - Error rate
  - Throughput (requests per second)
  - 95th percentile latency

To run the stress test, ensure you have images in the `images` folder and run:
```bash
python stress_test.py
```

