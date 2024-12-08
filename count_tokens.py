import os
import tiktoken
import argparse
import sys

# Function to count tokens in a file
def count_tokens_in_file(file_path, model="gpt-4o"):
	try:
		tokenizer = tiktoken.encoding_for_model(model)
	except Exception as e:
		print(f"Invalid model: {e}")
		return 0;

	try:
		with open(file_path, 'r', encoding='utf-8') as file:
			content = file.read()
		return len(tokenizer.encode(content))
	except Exception as e:
		print(f"Error reading {file_path}: {e}")
		return 0

# Main function to count tokens in specified file types
def count_tokens_in_folder(folder_path, model="gpt-4o"):
  # Load the tokenizer for the specified model
	try:
		tokenizer = tiktoken.encoding_for_model(model)
	except Exception as e:
		print(f"Invalid model: {e}")
		return 0;


    # File extensions to process
    valid_extensions = ['.txt', '.c', '.h', '.py', '.java', '.md']

    total_tokens = 0
    file_token_counts = {}

    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.endswith(ext) for ext in valid_extensions):
                file_path = os.path.join(root, file)
                tokens = count_tokens_in_file(file_path, model)
                file_token_counts[file] = tokens
                total_tokens += tokens

    return file_token_counts, total_tokens


if __name__ == "__main__":
	# Set up the argument parser
	parser = argparse.ArgumentParser(description="Count tokens in files or folders.")
	parser.add_argument(
		'-i', '--interactive',
		action='store_true',
		help="Run in interactive mode."
	)
	parser.add_argument(
		'-p', '--pipe',
		action='store_true',
		help="Run in pipe mode and output only token count."
	)
	parser.add_argument(
		'path',
		nargs='?',
		default=None,
		help="Optional file or folder path to process."
	)
	parser.add_argument(
		'-m', 
		'--model', 
		default="gpt-4o"
		help="Specify the model (e.g., gpt-4, gpt-3.5-turbo)."
	)
	args = parser.parse_args()

	# Interactive mode
	if args.interactive:
		model_in = "gpt-4o"
		choose_model = input("Choose Model? (y / n): ").strip().lower()
		if choose_model in ["yes", "y"]:
			global model_in
			model_in = input("Model: ")

		# Input handling for file or folder
		match input("Count Individual File or Folder\n").strip().lower():
				case "file":
						file_path = input("Enter file path: ").strip()
						try:
								# Count tokens
								tokens = count_tokens_in_file(file_path, model_in)
								print(f"{file_path}: {tokens} tokens")
						except Exception as e:
								print(f"Error: {e}")
								sys.exit(1)

				case "folder":
						folder_path = input("Folder Path (default is ./): ").strip() or "./"

						# Run the token counting
						file_token_counts, total_tokens = count_tokens_in_folder(folder_path, model_in)
						uinput = input("Print count for all files? (yes/y or no/n):\n").strip().lower()
						if uinput in ["all", "yes", "y"]:
								# Print token counts for each file
								print("Token counts per file:")
								for file, tokens in file_token_counts.items():
										print(f"{file}: {tokens} tokens")

						# Print total token count
						print(f"Total tokens in folder: {total_tokens}")

				case _:
						print("Invalid input. Please enter 'file' or 'folder'.")
	# Pipe Mode
	elif args.pipe:
		if not args.path:
				print("Error: You must specify a file or folder path for pipe mode.", file=sys.stdrr)
				sys.exit(1)

		if os.path.isfile(args.path):
				tokens = count_tokens_in_file(args.path, args.model)
				print(tokens)  # Pipe-friendly output
		elif os.path.isdir(args.path):
				total_tokens = count_tokens_in_folder(args.path, args.model)
				print(total_tokens)  # Pipe-friendly output
		else:
				print("Error: Invalid path.", file=sys.stderr)
				sys.exit(1)
		else:
		parser.print_help()
