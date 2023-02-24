import random

def handle_command(message) -> str:
    p_message = message.lower()
    if p_message == '!ping':
        return 'pong!'

    if p_message == '!roll':
        return str(random.randint(1, 6))

    if p_message == '!help':
        return "Useless bot xd" 
