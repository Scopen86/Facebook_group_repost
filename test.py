import argparse

# Create an argument parser
parser = argparse.ArgumentParser(description="A simple script with arguments")

# Add arguments
parser.add_argument("filename", help="The name of the file to process")
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

# Parse the arguments
args = parser.parse_args()

# Access the arguments
filename = args.filename
verbose = args.verbose

# Use the arguments in your script
print(f"Filename: {filename}")
if verbose:
    print("Verbose mode is enabled")