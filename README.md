# OCR and Summarization Web Application

This project implements a web-based Optical Character Recognition (OCR) application that allows users to upload images, extract text from them, and obtain a summary of the extracted text.

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
10. [Future Improvements](#future-improvements)

## Project Overview

This application provides a web interface for users to upload images, extract text using OCR technology, and obtain a summary of the extracted text. It processes the images on the server-side and returns the extracted text, summary, and performance metrics.

## Features

- Web-based user interface for image upload
- Server-side OCR processing using Tesseract
- Text summarization using Groq AI
- Real-time display of extracted text, summary, and processing latency
- Optimized image processing for improved OCR accuracy
- Concurrent request handling
- Error handling and user feedback

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

## Project Structure

```
ocr_project/
├── main.py              # FastAPI application, OCR logic, and summarization
├── static/
│   └── app.html         # Web interface
└── README.md            # Project documentation
```

## Setup and Installation

1. Install the required Python packages:
   ```bash
   pip install fastapi uvicorn python-multipart pillow pytesseract groq
   ```

2. Install Tesseract OCR on your system:
   - For Ubuntu: `sudo apt-get install tesseract-ocr`
   - For macOS: `brew install tesseract`
   - For Windows: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

3. Set up your Groq API key:
   - Sign up for a Groq account and obtain your API key
   - Set the `GROQ_API_KEY` variable in `main.py` with your API key

## Usage

1. Start the backend server:
   ```bash
   python main.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Use the interface to upload an image and see the extracted text and summary

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

4. **
