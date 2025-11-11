import requests
import json
import os
import sys
import time
import threading

# Configuration
API_KEY = os.getenv("ORTEX_API_KEY", "your-api-key-here")
BASE_URL = "https://api.ortex.cc"

# Animation state
loading = False

def loading_animation():
    animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    idx = 0
    while loading:
        sys.stdout.write(f"\r{animation[idx % len(animation)]} Thinking...")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")  # Clear the line
    sys.stdout.flush()

# Send a chat completion request
def chat_completion(messages, model="auto", chain="Solana"):
    global loading
    url = f"{BASE_URL}/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": messages,
        "model": model,
        "chain": chain
    }
    
    # Start loading animation
    loading = True
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.daemon = True
    animation_thread.start()
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        loading = False
        time.sleep(0.2)  # Give animation time to stop
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        loading = False
        time.sleep(0.2)
        print(f"\n Error making request: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"   {error_data.get('error', {}).get('message', e.response.text)}")
            except:
                print(f"   {e.response.text}")
        raise

def print_header():
    print("\n" + "="*60)
    print("Ortex - Python Example")
    print("="*60)
    print("\nCommands:")
    print("  • Type your question to chat")
    print("  • '/clear' to start a new conversation")
    print("  • '/exit' or '/quit' to exit")
    print("  • '/stats' to show usage statistics")
    print("\n" + "="*60 + "\n")

def format_usage(usage, cost):
    return f"[Tokens: {usage['total_tokens']} | Cost: ${cost:.6f}]"

def main():
    print_header()
    
    conversation = []
    total_tokens = 0
    total_cost = 0.0
    message_count = 0
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['/exit', '/quit']:
                print("\n Goodbye.\n")
                break
            
            elif user_input.lower() == '/clear':
                conversation = []
                total_tokens = 0
                total_cost = 0.0
                message_count = 0
                print("\n Conversation history cleared.\n")
                continue
            
            elif user_input.lower() == '/stats':
                print("\n Session Statistics:")
                print(f"   Messages: {message_count}")
                print(f"   Total Tokens: {total_tokens}")
                print(f"   Total Cost: ${total_cost:.6f}")
                print()
                continue
            
            # Add user message to conversation
            conversation.append({
                "role": "user",
                "content": user_input
            })
            
            # Call API
            try:
                response = chat_completion(conversation)
                
                # Display AI response
                print(f"\n AI: {response['content']}")
                print(f"    {format_usage(response['usage'], response['cost'])}\n")
                
                # Update statistics
                total_tokens += response['usage']['total_tokens']
                total_cost += response['cost']
                message_count += 1
                
                # Add assistant response to conversation
                conversation.append({
                    "role": "assistant",
                    "content": response['content']
                })
                
            except Exception as e:
                print(f"\n Failed to get response. Please try again.\n")
                # Remove the failed user message
                conversation.pop()
        
        except KeyboardInterrupt:
            print("\n\n Goodbye.\n")
            break
        
        except EOFError:
            print("\n\n Goodbye.\n")
            break

if __name__ == "__main__":
    # Check if API key is set
    if API_KEY == "your-api-key-here":
        print("  Please set your ORTEX_API_KEY environment variable or update the API_KEY variable")
        print("  Get your API key from: https://ortex.cc/settings/api-keys\n")
        exit(1)
    
    try:
        main()
    except Exception as e:
        print(f"\n Fatal Error: {e}\n")
