import json
import statistics
from collections import defaultdict

def analyze_results(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    results = data['results']
    
    # Group by top_p and top_k
    processing_times = defaultdict(list)
    response_lengths = defaultdict(list)
    
    for result in results:
        params = result['parameters']
        key = (params['top_p'], params['top_k'])
        
        processing_times[key].append(result['processing_time'])
        response_lengths[key].append(len(result['response'].split()))
    
    # Calculate averages and identify optimal ranges
    print("\nAnalysis Results:")
    print("=" * 80)
    print(f"{'Top_P':<10} {'Top_K':<10} {'Avg Time':<15} {'Avg Words':<15} {'Notes'}")
    print("-" * 80)
    
    optimal_range = []
    
    for key in sorted(processing_times.keys()):
        top_p, top_k = key
        avg_time = statistics.mean(processing_times[key])
        avg_words = statistics.mean(response_lengths[key])
        
        # Check if this combination is in the sweet spot
        notes = ""
        if 110 <= avg_words <= 115 and 5.2 <= avg_time <= 5.6:
            notes = "✓ Optimal"
            optimal_range.append((top_p, top_k, avg_time, avg_words))
        elif avg_words < 100 or avg_words > 120:
            notes = "! Outside word range"
            
        print(f"{top_p:<10.2f} {top_k:<10d} {avg_time:<15.2f} {avg_words:<15.2f} {notes}")
    
    # Print summary
    print("\nSummary:")
    print("=" * 80)
    print("Optimal Combinations (110-115 words, balanced processing time):")
    for top_p, top_k, avg_time, avg_words in optimal_range:
        print(f"- top_p: {top_p:.2f}, top_k: {top_k:d} (Time: {avg_time:.2f}s, Words: {avg_words:.1f})")
    
    print("\nRecommended Range:")
    print("- top_p: 0.7-0.8")
    print("- top_k: 50-75")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "testtopptopk_20250205_092149.json"
    
    analyze_results(filename)
