import openai

# Set up OpenAI API key
api_key = "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"
openai.api_key = api_key

# Function to send a message to the OpenAI chatbot model and return its response
def send_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=500,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0,
        temperature=1,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content


# Main function that runs the chatbot
def main():
    # Initialize the conversation history with a message from the chatbot
    message_log = [
        {"role": "system", "content": '''You are a personable, entertaining YouTube script writer with millions of subscribers. 

        You specialize in creating fluid video essays, section by section, based on an outline.

        Charisma is priority #1, detail is #2

        Your scripts flow in a natural, compounding, orderly fashion. 

        Prioritize personality and content in place of filler and wordiness.

        Transitions between sections are natural; not abrupt, distinct, or repetitive.

        Avoid sentence structure and transitional phrase repetition across sections if possible. 
        '''}
        
    ]

    # Set a flag to keep track of whether this is the first request in the conversation
    first_request = True

    # Start a loop that runs until the user types "quit"
    while True:
        if first_request:
            # If this is the first request, get the user's input and add it to the conversation history
            message_log = [
                {"role": "system", "content": '''You are a personable, entertaining YouTube script writer with millions of subscribers. 

                You specialize in creating fluid video essay outlines, section by section.

                Your detailed outlines encourage scripts to flow in a natural, orderly fashion.

                Charisma is priority #1, detail is #2

                When you generate outlines, you return them in the format:

                [Section Name]
                - Bullet points
                (include the brackets)

                Only if the section happens to be numbered, follow the number with a colon
                '''}
            ]
            user_input = input("You: ")
            message_log.append({"role": "user", "content": user_input})

            # Send the conversation history to the chatbot and get its response
            response = send_message(message_log)
            if user_input.lower() == "quit":
                    print("Goodbye!")
                    break

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})
            print(f"AI assistant: {response}")
            with open('outline.txt', 'w') as f:
                f.write(response)

            # Set the flag to False so that this branch is not executed again
            first_request = False
        else:
            # If this is not the first request, put the outline and generate the script
            with open('outline.txt') as f:
                lines = f.readlines()
            intro = [x for i,x in enumerate(lines) if x.find('[Introduction]') != -1]
            data = [x for i,x in enumerate(lines) if x.find('[Section') != -1]
            conclu = [x for i,x in enumerate(lines) if x.find('[Conclusion]') != -1]
            index = []
            script = []
            for i in intro:
                intro = lines.index(i)
            for i in data:
                l = lines.index(i)
                index.append(l)
            for i in conclu:
                conclu = lines.index(i)

            for script_generate in range(len(lines)):
                if script_generate == intro:
                    user_input = "Write me an accessible, detailed 3 paragraph introduction, with each paragraph having a minimum of 3 sentences, centered around a bold, attention-grabbing hook, without specific dates, from a personable YouTuber based on 1) something relevant many people might not know about the topic and on 2) the following outline:" + ' '.join(lines[(intro+1):(index[0]-1)])
                    # user_input = "write introduction"
                    print(user_input)
                elif script_generate == "/n":
                    continue
                elif index.count(script_generate):
                
                    if script_generate == index[-1]:
                        endpoint = conclu
                    else:
                        endpoint = index[index.index(script_generate)+1] 
                    print(endpoint)
                    print(conclu)
                    print(script_generate)
                    user_input = "Write me an intriguing, detailed 5 paragraph section, with each paragraph having a minimum of 3 sentences, from a personable YouTuber, flowing naturally from the previous sections, based on the following outline:" + ' '.join(lines[script_generate+1:endpoint-1])
                    print(user_input)
                elif script_generate == conclu:
                    user_input = "Write me an intriguing, detailed 5 paragraph section, with each paragraph having a minimum of 3 sentences, from a personable YouTuber, flowing naturally from the previous sections, based on the following outline:" + ' '.join(lines[conclu+1:len(lines)])
                    print(user_input)
                    # first_request = False
                else:
                    continue
                
                # If the user types "quit", end the loop and print a goodbye message
                if user_input.lower() == "quit":
                    print("Goodbye!")
                    break

                message_log.append({"role": "user", "content": user_input})

                # Send the conversation history to the chatbot and get its response
                response = send_message(message_log)
                script.extend(response)

                # Add the chatbot's response to the conversation history and print it to the console
                message_log.append({"role": "assistant", "content": response})
                print(f"AI assistant: {response}")
            with open('script.txt', 'w') as f:
                for i in script:
                    f.write(i)
            break


# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()