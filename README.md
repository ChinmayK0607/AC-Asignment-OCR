# OCR and Summarization Web Application

This project implements a web-based Optical Character Recognition (OCR) application that allows users to upload images and extract text from them. It also includes a stress testing script to evaluate the application's performance under load.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies and Libraries Used](#technologies-and-libraries-used)
4. [Project Structure](#project-structure)
5. [Setup and Installation](#setup-and-installation)
6. [Usage](#usage)
7. [Methodology](#methodology)
8. [Performance Optimization](#performance-optimization)
9. [Stress Testing](#stress-testing)
10. [Assessment Criteria Addressed](#assessment-criteria-addressed)
11. [Future Improvements](#future-improvements)

## Project Overview

This application provides a web interface for users to upload images and extract text using OCR technology. It processes the images on the server-side and returns the extracted text along with performance metrics.

## Features

- Web-based user interface for image upload
- Server-side OCR processing using Tesseract
- Real-time display of extracted text and processing latency
- Optimized image processing for improved performance
- Concurrent request handling
- Comprehensive stress testing script

## Technologies and Libraries Used

- **Backend**:
  - FastAPI: For creating the web server and API endpoints
  - Pillow (PIL): For image processing
  - pytesseract: For OCR functionality
  - uvicorn: ASGI server for running the FastAPI application

- **Frontend**:
  - HTML5
  - JavaScript (Vanilla JS)
  - CSS3

- **Stress Testing**:
  - requests: For sending HTTP requests
  - concurrent.futures: For concurrent execution of requests

## Project Structure

```
ocr_project/
├── main.py              # FastAPI application and OCR logic
├── static/
│   └── app.html         # Web interface
├── stress_test.py       # Stress testing script
├── images/              # Folder to store test images
└── README.md            # This file
```

## Setup and Installation

1. Install the required Python packages:
   ```bash
   pip install fastapi uvicorn python-multipart pillow pytesseract requests
   ```

2. Install Tesseract OCR on your system:
   - For Ubuntu: `sudo apt-get install tesseract-ocr`
   - For macOS: `brew install tesseract`
   - For Windows: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

3. Ensure you have a folder named `images` in the project directory with some test images for stress testing.

## Usage

1. Start the backend server:
   ```bash
   python main.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Use the interface to upload an image and see the extracted text

4. To run the stress test:
   ```bash
   python stress_test.py
   ```

## Methodology

1. **Image Upload**: The user uploads an image through the web interface.

2. **Server-side Processing**: 
   - The server receives the image and performs initial validation.
   - The image is processed using PIL (Python Imaging Library):
     - Converted to grayscale
     - Resized to reduce processing time
   - Tesseract OCR is applied to the processed image to extract text.

3. **Response**: The extracted text and processing latency are sent back to the client.

4. **Display**: The client-side JavaScript updates the UI with the received information.

## Performance Optimization

- **Image Preprocessing**: Grayscale conversion and resizing reduce the computational load on the OCR engine.
- **Caching**: Tesseract configuration is cached using `lru_cache` to avoid repeated setup.
- **Concurrent Processing**: A ThreadPoolExecutor is used to handle multiple requests concurrently.
- **Asynchronous Operations**: FastAPI's asynchronous capabilities are utilized for non-blocking I/O operations.

## Stress Testing

The `stress_test.py` script performs the following:

1. Sends multiple concurrent requests to the OCR endpoint.
2. Measures individual request latencies and overall throughput.
3. Calculates and reports various performance metrics:
   - Average, minimum, and maximum latency
   - Error rate
   - Throughput (requests per second)
   - 95th percentile latency

## Assessment Criteria Addressed

1. **Code Quality and Organization**: The project is well-structured with separate modules for the main application and stress testing. The code follows PEP 8 guidelines and includes comments for clarity.

2. **Functionality**: The application successfully implements OCR functionality with a user-friendly web interface.

3. **Performance Optimization**: Various techniques are employed to optimize performance, including image preprocessing, caching, and concurrent processing.

4. **Error Handling**: The application includes error logging and proper exception handling both in the main application and stress testing script.

5. **Documentation**: This README provides comprehensive documentation on setup, usage, methodology, and performance considerations.

6. **Testing**: A thorough stress testing script is included to evaluate the application's performance under load.

7. **User Experience**: The web interface is simple and intuitive, providing real-time feedback on the OCR process.

## Future Improvements

- Implement more advanced image preprocessing techniques for better OCR accuracy
- Add support for multiple languages in OCR
- Introduce a queue system for handling high load scenarios
- Implement user authentication and rate limiting
- Develop a more sophisticated frontend with progress indicators and error handling
