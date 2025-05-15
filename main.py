import g4f

def chat_with_g4f(prompt):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        reply = chat_with_g4f(user_input)
        print("Bot:", reply)
