from ollama import Client
import json
import argparse

def generate_response(args):
    # Initialize Ollama client
    client = Client(host='http://localhost:11434')
    
    try:
        # Generate response
        response = client.generate(
            model=args.model,
            prompt=args.prompt,
            options={
                'top_p': args.top_p,
                'top_k': args.top_k
            }
        )

        # Format response as JSON
        output = {
            "model": args.model,
            "prompt": args.prompt,
            "parameters": {
                "top_p": args.top_p,
                "top_k": args.top_k
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
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate text using Ollama with customizable parameters')
    
    # Add arguments
    parser.add_argument('--model', 
                       type=str, 
                       default='llama3.2',
                       help='Model name to use (default: llama3.2)')
    
    parser.add_argument('--prompt', 
                       type=str,
                       default='write 100 words about why humans are awesome',
                       help='Text prompt for generation')
    
    parser.add_argument('--top-p',
                       type=float,
                       default=0.9,
                       help='Top-p value (0-1). Higher values make text more diverse by considering less likely words')
    
    parser.add_argument('--top-k',
                       type=int,
                       default=50,
                       help='Top-k value (1-100). Limits number of words considered at each step')

    # Parse arguments
    args = parser.parse_args()
    
    # Validate arguments
    if not (0 <= args.top_p <= 1):
        parser.error("top-p must be between 0 and 1")
    if not (1 <= args.top_k <= 100):
        parser.error("top-k must be between 1 and 100")
        
    generate_response(args)
