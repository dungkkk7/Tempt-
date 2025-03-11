import socket
import time
import random

# Define the alphabet used by the server
alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def generate_token(seed, length=20):
    """Generate a token for a given seed, matching the server's logic."""
    random.seed(seed)
    token = ''
    for _ in range(length):
        token += random.choice(alphabet)
    return token

def attempt_connection():
    """Connect to the server, estimate time, and try to guess the token."""
    # Create a socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Record time before connecting
    t0 = time.time()
    s.connect(('verbal-sleep.picoctf.net', 50152))
    
    # Receive the initial prompt
    data = s.recv(1024).decode()
    t1 = time.time()
    
    # Estimate server time and uncertainty
    rtt = t1 - t0
    t_server = t0 + rtt / 2
    delta = rtt / 2
    
    # Generate possible seeds within the uncertainty window
    min_seed = int((t_server - delta) * 1000)
    max_seed = int((t_server + delta) * 1000)
    possible_seeds = list(range(min_seed, max_seed + 1))
    
    # Limit to 50 attempts; if more than 50 seeds, take a subset
    seeds_to_try = possible_seeds[:50] if len(possible_seeds) > 50 else possible_seeds
    
    # Generate tokens for each seed
    tokens_to_try = [generate_token(seed) for seed in seeds_to_try]
    
    # Try each token
    for token in tokens_to_try:
        s.send((token + '\n').encode())
        response = s.recv(1024).decode()
        
        if "Congratulations" in response:
            print("Success! Token:", token)
            print("Server response:", response)
            # Extract flag (assuming it's in the response after "Congratulations")
            flag = response.split('\n')[-2] if '\n' in response else response
            s.close()
            return flag
        else:
            print(f"Guess failed: {token}")
    
    # If all attempts fail, close connection
    s.close()
    return None

# Keep trying until the flag is found
while True:
    flag = attempt_connection()
    if flag:
        print(f"Flag: {flag}")
        SystemExit(0)
    else:
        print("Failed to guess token. Retrying with a new connection...")
        time.sleep(1)  # Small delay to avoid overwhelming the server