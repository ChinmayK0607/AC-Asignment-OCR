import os
import time
import requests
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
API_URL = "http://localhost:8000/ocr"
IMAGES_FOLDER = "images"
NUM_REQUESTS = 100
MAX_WORKERS = 10

def get_image_files(folder):
    """Retrieve image files from the specified folder."""
    return [os.path.join(folder, f) for f in os.listdir(folder) 
            if f.lower().endswith(('png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif')) and os.path.isfile(os.path.join(folder, f))]

def send_request(image_path):
    """Send a POST request to the API with the provided image."""
    with open(image_path, 'rb') as img_file:
        files = {'file': (os.path.basename(image_path), img_file)}
        try:
            start_time = time.time()
            response = requests.post(API_URL, files=files)
            latency = time.time() - start_time
            response.raise_for_status()
            data = response.json()
            return latency, data['latency'], len(data['text']), len(data['summary']), None
        except requests.RequestException as e:
            return None, None, None, None, str(e)

def run_stress_test():
    """Run the stress test and calculate performance metrics."""
    image_files = get_image_files(IMAGES_FOLDER)
    if not image_files:
        print("No images found in the folder.")
        return
    
    total_latencies = []
    server_latencies = []
    text_lengths = []
    summary_lengths = []
    errors = 0
    total_time_start = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(send_request, img) for img in image_files * (NUM_REQUESTS // len(image_files) + 1)][:NUM_REQUESTS]
        for future in as_completed(futures):
            total_latency, server_latency, text_length, summary_length, error = future.result()
            if total_latency:
                total_latencies.append(total_latency)
                server_latencies.append(server_latency)
                text_lengths.append(text_length)
                summary_lengths.append(summary_length)
                print(f"OK - Total time: {total_latency:.4f}s, Server time: {server_latency:.4f}s, Text: {text_length} chars, Summary: {summary_length} chars")
            if error:
                errors += 1
                print(f"Error occurred: {error}")

    total_time = time.time() - total_time_start
    total_requests = len(total_latencies) + errors
    print_metrics(total_requests, total_time, total_latencies, server_latencies, text_lengths, summary_lengths, errors)

def print_metrics(total_requests, total_time, total_latencies, server_latencies, text_lengths, summary_lengths, errors):
    """Print the calculated performance metrics."""
    avg_total_latency = statistics.mean(total_latencies) if total_latencies else float('inf')
    avg_server_latency = statistics.mean(server_latencies) if server_latencies else float('inf')
    avg_text_length = statistics.mean(text_lengths) if text_lengths else 0
    avg_summary_length = statistics.mean(summary_lengths) if summary_lengths else 0
    error_rate = (errors / total_requests) * 100 if total_requests > 0 else 0
    throughput = total_requests / total_time if total_time > 0 else 0

    print(f"\nTest Results:")
    print(f"Total requests made: {total_requests}")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Average total latency: {avg_total_latency:.4f} seconds")
    print(f"Average server latency: {avg_server_latency:.4f} seconds")
    print(f"Average extracted text length: {avg_text_length:.2f} characters")
    print(f"Average summary length: {avg_summary_length:.2f} characters")
    print(f"Error rate: {error_rate:.2f}%")
    print(f"Throughput: {throughput:.2f} requests/second")

    if total_latencies:
        print(f"Min total latency: {min(total_latencies):.4f} seconds")
        print(f"Max total latency: {max(total_latencies):.4f} seconds")
        print(f"Median total latency: {statistics.median(total_latencies):.4f} seconds")
        print(f"95th percentile total latency: {statistics.quantiles(total_latencies, n=20)[-1]:.4f} seconds")

    if server_latencies:
        print(f"Min server latency: {min(server_latencies):.4f} seconds")
        print(f"Max server latency: {max(server_latencies):.4f} seconds")
        print(f"Median server latency: {statistics.median(server_latencies):.4f} seconds")
        print(f"95th percentile server latency: {statistics.quantiles(server_latencies, n=20)[-1]:.4f} seconds")

if __name__ == "__main__":
    run_stress_test()
