from ollama import Client
import json

def generate_response():
    # Initialize Ollama client
    client = Client(host='http://localhost:11434')
    
    # Default values
    default_model = "llama3.2"  # Note: using llama2 as llama3.2 isn't a standard model name
    default_prompt = "write 100 words about why humans are awesome"
    
    try:
        # Get user inputs with defaults
        model = input(f"Enter the model name (default '{default_model}'): ").strip() or default_model
        prompt = input(f"Enter your prompt (press Enter for default): ").strip() or default_prompt
        top_p = float(input("Enter top_p value (0-1, default 0.9). A high value means the model looks at more possible words, even less likely ones, making text more diverse: ") or "0.9")
        top_k = int(input("Enter top_k value (1-100, default 50). This limits the number of top words the model considers at each step. Higher values = more diverse but potentially less focused text: ") or "50")

        # Generate response
        response = client.generate(
            model=model,
            prompt=prompt,
            options={
                'top_p': top_p,
                'top_k': top_k
            }
        )

        # Format response as JSON
        output = {
            "model": model,
            "prompt": prompt,
            "parameters": {
                "top_p": top_p,
                "top_k": top_k
            },
            "response": response['response']
        }

        # Print formatted JSON
        print("\nGenerated Response:")
        print(json.dumps(output, indent=2))

    except ValueError as e:
        print(f"\nError with input values: {e}")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    generate_response()