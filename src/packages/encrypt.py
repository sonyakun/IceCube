import base64

def decode(text):
    return base64.b64decode(text.encode()).decode()

def encode(text):
    return base64.b64encode(text).decode()