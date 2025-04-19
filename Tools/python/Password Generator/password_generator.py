# Python tool for Secure Password Generation. Accepts input for character length and spits out a "secure" password that can be used quickly.

# Author: Tilka

# Password Length and Complexity Input
# - Get User input for length of password (cannot be less than 15).
# - If user pw less than 15, display error message.
import string
import secrets

# Get the Length of the password
# - Ask user for password length
# - Catch errors if user enters letters or characters less than 15
def get_pw_length():
        while True:
            try:
                pw_length = int(input("Enter the Desired Length of your Password (Must be at least 15 chracters): "))

                if pw_length < 15:
                    print("Password length must be at least 15 characters")
                    continue # Ask again if input is too small
                
                return pw_length
            # Catch Errors
            except ValueError:
                print("Error: Please Enter a Valid Number")
                
# Generate Password
# - Generate a pseudorandom secure password based on the length taken from the user
# - Define the character set
def generate_pw(pw_length):
    alphabet = string.ascii_letters + string.digits + string.punctuation # Letters, numbers and special characters
    usr_pw = ''.join(secrets.choice(alphabet) for i in range(pw_length)) # Length of pw chosen by user used to join together password
    print(f'Here is your Password, keep it safe!: {usr_pw}')

# Main
# - Value of pw_length assigned to get_pw_length function
# - Value of pw_length assigned to generate_pw function
def main():
    pw_length = get_pw_length()
    generate_pw(pw_length)

# Call Main
if __name__ == "__main__":
    main()