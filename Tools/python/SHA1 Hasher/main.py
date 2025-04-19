# SHA1 Hash Cracker

import hashlib

# Function to convert text to sha1
def text_to_sha(text):
    # Create hash object
    digest = hashlib.sha1(
        # Encode text
        text.encode()
    ).hexdigest() # Returns hex char string
    
    return digest

def main():
    # Get the hash from the user
    user_sha = input("Enter SHA1 Hash to Crack: ")
    # To lowercase
    cleaned_sha = user_sha.strip().lower()
    
    # Open password file
    with open('./passwords.txt') as file:
        for line in file:
            # Strip spaces
            password = line.strip()
            converted_sha1 = text_to_sha(password)
            
            # Check if user hash is the same as converted
            if cleaned_sha == converted_sha1:
                print(f"Password found: {password}")
                return
            
    print("Password could not be found")

if __name__ == '__main__':
    main()