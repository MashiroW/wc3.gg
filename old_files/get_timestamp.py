import time

def get_formatted_timestamp():
    # Get the current timestamp
    current_timestamp = int(time.time())

    # Format the timestamp
    formatted_timestamp = str(current_timestamp)

    return formatted_timestamp

# Example usage
timestamp = get_formatted_timestamp()
print(timestamp)