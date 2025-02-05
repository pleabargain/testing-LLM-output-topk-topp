# LLM Parameter Testing Framework

# motivation
I realized that I didn't fully understand top-p and top-k parameters. I wanted to test how they affect the output of a LLM.

# usage
While talking to a friend, I realized that I could set my machine working on a problem while I was sleeping. That problem was generating code/ text/ images/ music/ etc. 

By using top-p and top-k parameters, I can control the diversity of the output. 

A testing framework to find optimal top-p (nucleus sampling) and top-k parameters for Large Language Models (LLMs) to achieve the best output quality.

## Project Overview

This project aims to systematically test and analyze how different top-p and top-k parameters affect LLM output quality. The framework uses Ollama to test various parameter combinations and analyze the results to find optimal settings.

### Key Components

- `topp-orig.py`: Original script for manual testing with user input
- `test_topp_topk.py`: Automated testing framework that runs systematic tests
- `analyze_results.py`: Analysis script to process test results and identify optimal parameters
- Generated JSON files store test results with timestamps

## Current Findings

The analysis suggests optimal parameter ranges:
- top-p: 0.7-0.8 (nucleus sampling threshold)
- top-k: 50-75 (number of top tokens to consider)

These ranges provide a good balance between:
- Response coherence
- Word count consistency (110-115 words)
- Processing time (5.2-5.6 seconds)

### Unique Words Analysis

```python
# Pseudo code for extracting and analyzing unique words from responses
def analyze_unique_words(response_text):
    """
    Extract and analyze unique words from LLM responses
    
    Steps:
    1. Preprocess the text:
       - Convert to lowercase
       - Remove punctuation
       - Split into words
    
    2. Create unique words set:
       - Store all unique words
       - Track frequency of each word
    
    3. Calculate metrics:
       - Unique word ratio
       - Word frequency distribution
       - Common/rare word analysis
    """
    # Initialize containers
    all_words = []
    word_frequency = {}
    
    # Preprocess text
    cleaned_text = remove_punctuation(response_text.lower())
    words = cleaned_text.split()
    
    # Count word frequencies
    for word in words:
        word_frequency[word] = word_frequency.get(word, 0) + 1
        
    # Calculate metrics
    unique_words = set(words)
    total_words = len(words)
    unique_ratio = len(unique_words) / total_words
    
    return {
        'unique_words': list(unique_words),
        'word_frequency': word_frequency,
        'unique_ratio': unique_ratio,
        'total_words': total_words
    }
```

## Suggested Next Steps

### 1. Expand Test Scenarios

```python
# Test different prompt types
def test_prompt_categories():
    prompts = {
        'creative': [
            'Write a story about...',
            'Compose a poem about...',
        ],
        'analytical': [
            'Explain how...',
            'Compare and contrast...',
        ],
        'technical': [
            'Write a function that...',
            'Debug this code...',
        ]
    }
    
    for category, prompt_list in prompts.items():
        for prompt in prompt_list:
            test_parameters(prompt, category)
```

### 2. Implement Response Quality Metrics

```python
def analyze_response_quality(response):
    metrics = {
        'diversity': calculate_text_diversity(response),
        'coherence': measure_coherence(response),
        'relevance': evaluate_prompt_relevance(response),
        'creativity': assess_creativity_score(response)
    }
    return metrics

def calculate_text_diversity(text):
    # Calculate unique words ratio
    words = text.lower().split()
    unique_words = set(words)
    diversity_score = len(unique_words) / len(words)
    return diversity_score

def measure_coherence(text):
    # Implement sentence flow analysis
    sentences = text.split('.')
    coherence_scores = []
    for i in range(len(sentences)-1):
        score = analyze_sentence_transition(sentences[i], sentences[i+1])
        coherence_scores.append(score)
    return sum(coherence_scores) / len(coherence_scores)
```

### 3. Cross-Model Comparison Framework

```python
def compare_models():
    models = [
        'llama3.2',
        'mistral',
        'codellama',
        # Add more models
    ]
    
    test_cases = generate_test_cases()
    results = {}
    
    for model in models:
        for test_case in test_cases:
            result = run_model_test(
                model=model,
                prompt=test_case['prompt'],
                parameters=test_case['parameters']
            )
            results[f"{model}_{test_case['id']}"] = {
                'output': result.response,
                'metrics': analyze_response_quality(result.response),
                'performance': {
                    'latency': result.processing_time,
                    'token_rate': calculate_token_rate(result)
                }
            }
    
    return analyze_cross_model_results(results)
```

### 4. Performance Benchmarking

```python
def benchmark_performance():
    # Test different batch sizes
    batch_sizes = [1, 5, 10, 20]
    
    # Test concurrent requests
    concurrent_levels = [1, 2, 4, 8]
    
    metrics = {
        'throughput': [],
        'latency': [],
        'memory_usage': [],
        'token_rate': []
    }
    
    for batch_size in batch_sizes:
        for concurrency in concurrent_levels:
            result = run_load_test(
                batch_size=batch_size,
                concurrent_requests=concurrency,
                duration_seconds=300
            )
            record_metrics(metrics, result)
    
    return analyze_performance_metrics(metrics)
```

## Setup Instructions

1. Install dependencies:
```bash
pip install ollama
```

2. Run tests:
```bash
python test_topp_topk.py
```

3. Analyze results:
```bash
python analyze_results.py testtopptopk_[timestamp].json
```

## Contributing

To contribute additional test scenarios or analysis metrics:

1. Fork the repository
2. Create a feature branch
3. Add your test cases or metrics
4. Submit a pull request with detailed description of changes
