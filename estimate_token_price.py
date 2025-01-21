import sys

def calculate_cost(input_tokens, output_tokens, input_cost_per_million=15.00, output_cost_per_million=60.00):
    """
    Calculates the cost of input and output tokens for a request.

    Parameters:
        input_tokens (int): Number of input tokens.
        output_tokens (int): Expected number of output tokens.
        input_cost_per_million (float): Cost per million input tokens (default is $15.00).
        output_cost_per_million (float): Cost per million output tokens (default is $60.00).

    Returns:
        dict: A dictionary with detailed costs for input, output, and total cost.
    """
    # Convert tokens to millions
    input_tokens_millions = input_tokens / 1_000_000 ## TODO: user input model / pricing https://openai.com/api/pricing/
    output_tokens_millions = output_tokens / 1_000_000

    # Calculate costs
    input_cost = input_tokens_millions * input_cost_per_million
    output_cost = output_tokens_millions * output_cost_per_million
    total_cost = input_cost + output_cost

    # Return results as a dictionary
    return {
        "Input tokens": f"${input_cost:.2f} USD",
        "Output tokens": f"${output_cost:.2f} USD",
        "Total cost": f"${total_cost:.2f} USD"
    }

if __name__ == "__main__":
	if sys.stdin.isatty():
		input_tokens = input("Number of input tokens: ")
	else:
		input_tokens = int(sys.stdin.read().strip())
	output_tokens = input("Expected number of output tokens: ")

	costs = calculate_cost(input_tokens, output_tokens)

	# Print results
	for key, value in costs.items():
			print(f"{key}: {value}")
