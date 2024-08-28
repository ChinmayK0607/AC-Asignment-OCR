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
            if f.lower().endswith(('png', 'jpg', 'jpeg')) and os.path.isfile(os.path.join(folder, f))]

def send_request(image_path):
    """Send a POST request to the API with the provided image."""
    with open(image_path, 'rb') as img_file:
        files = {'file': (os.path.basename(image_path), img_file)}
        try:
            start_time = time.time()
            response = requests.post(API_URL, files=files)
            latency = time.time() - start_time
            response.raise_for_status()
            return latency, None
        except requests.RequestException as e:
            return None, str(e)

def run_stress_test():
    """Run the stress test and calculate performance metrics."""
    image_files = get_image_files(IMAGES_FOLDER)
    if not image_files:
        print("No images found in the folder.")
        return
    
    latencies = []
    errors = 0
    total_time_start = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(send_request, img) for img in image_files * (NUM_REQUESTS // len(image_files) + 1)][:NUM_REQUESTS]
        for future in as_completed(futures):
            latency, error = future.result()
            if latency:
                latencies.append(latency)
                print(f"OK - Time taken: {latency:.4f} seconds")
            if error:
                errors += 1
                print(f"Error occurred: {error}")

    total_time = time.time() - total_time_start

    # Calculate and print metrics
    total_requests = len(latencies) + errors
    print_metrics(total_requests, total_time, latencies, errors)

def print_metrics(total_requests, total_time, latencies, errors):
    """Print the calculated performance metrics."""
    avg_latency = statistics.mean(latencies) if latencies else float('inf')
    error_rate = (errors / total_requests) * 100 if total_requests > 0 else 0
    throughput = total_requests / total_time if total_time > 0 else 0

    print(f"\nTest Results:")
    print(f"Total requests made: {total_requests}")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Average latency: {avg_latency:.4f} seconds")
    print(f"Error rate: {error_rate:.2f}%")
    print(f"Throughput: {throughput:.2f} requests/second")

    if latencies:
        print(f"Min latency: {min(latencies):.4f} seconds")
        print(f"Max latency: {max(latencies):.4f} seconds")
        print(f"Median latency: {statistics.median(latencies):.4f} seconds")
        print(f"95th percentile latency: {statistics.quantiles(latencies, n=20)[-1]:.4f} seconds")

if __name__ == "__main__":
    run_stress_test()
