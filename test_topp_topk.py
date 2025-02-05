from ollama import Client
import json
import time
import random
from datetime import datetime, UTC

def generate_and_measure(model, prompt, top_p, top_k):
    client = Client(host='http://localhost:11434')
    
    start_time = time.time()
    try:
        response = client.generate(
            model=model,
            prompt=prompt,
            options={
                'top_p': top_p,
                'top_k': top_k
            }
        )
        end_time = time.time()
        processing_time = end_time - start_time
        
        result = {
            "timestamp": datetime.now(UTC).isoformat(),
            "model": model,
            "prompt": prompt,
            "parameters": {
                "top_p": top_p,
                "top_k": top_k
            },
            "processing_time": processing_time,
            "response": response['response']
        }
        
        return result
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_result(result, filename):
    try:
        # Load existing results
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"results": []}
        
        # Append new result
        data["results"].append(result)
        
        # Save updated results
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
    except Exception as e:
        print(f"Error saving results: {e}")

def test_random(filename, num_tests=10):
    model = "llama3.2"
    prompt = "Write a story between 100-120 words about a robot learning to paint"
    
    for i in range(num_tests):
        # Generate random values
        top_p = round(random.uniform(0.1, 1.0), 2)
        top_k = random.randint(10, 100)
        
        result = generate_and_measure(model, prompt, top_p, top_k)
        if result:
            save_result(result, filename)
            print(f"Random Test {i+1}: top_p={top_p:.2f}, top_k={top_k}")
        
        # Add delay to avoid rate limiting
        time.sleep(2)

def test_incremental(filename):
    model = "llama3.2"
    prompt = "Write a story between 100-120 words about a robot learning to paint"
    
    # Test with incremental values
    for top_p in [round(x * 0.1, 1) for x in range(1, 11)]:  # 0.1 to 1.0
        for top_k in [10, 25, 50, 75, 100]:  # Fixed intervals for top_k
            result = generate_and_measure(model, prompt, top_p, top_k)
            if result:
                save_result(result, filename)
                print(f"Tested: top_p={top_p:.1f}, top_k={top_k}")
            
            # Add delay to avoid rate limiting
            time.sleep(2)

def main():
    # Create timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"testtopptopk_{timestamp}.json"
    
    print(f"Starting tests. Results will be saved to {filename}")
    print("\nStarting incremental testing...")
    test_incremental(filename)
    print("\nStarting random testing...")
    test_random(filename)
    print(f"\nTesting completed. Results saved to {filename}")

if __name__ == "__main__":
    main()
