import secrets
import string

def generate_secure_secret(length=32):
    """Generate a secure random secret key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    print("Generated JWT Secret (add this to your Hugging Face Space secrets):")
    print(generate_secure_secret())