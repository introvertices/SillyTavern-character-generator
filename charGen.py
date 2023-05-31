import poe
import sys
import time
import os

# Put your Poe token here, you can get this by going to the dev console of your browser and pasting the p-b value of the cookie in the cookies section
token = "TOKEN"

# number of attempts it will make to jailbreak at the start before moving on with life. Set to 0 to disable jailbreaking.
jailbreak_max_attempts = 2

# Set up the poe client that we'll be sending messages to
client = poe.Client(token)




def main():

    jailbreak_attempts = 0

    header()

    # Jailbreak should be attempted here to save time if it fails
    if jailbreak_max_attempts != 0:
        while jailbreak_attempts < jailbreak_max_attempts:
            jailbreak_attempts = jailbreak_poe(jailbreak_attempts)

    # Set up chat character for correct responding, whether jailbroken or not.
    poe_roleplay_setup()

    print("")

    # Get the description of the character
    char_input = input("\033[1;34;40mBriefly describe your character: \033[1;37;40m")
    char_request = "Write me a JSON description for " + char_input

    # Grab the JSON prompt from the text file. DO NOT EDIT the file unless you know what you're doing
    with open('jsonPromptv2.txt','r') as file:
        prompt = file.read()

    print("")

    # Send everything off to 'Scribe'
    send_message(char_request, prompt, char_input)

    # Ask if the user wants to keep going
    make_more_chars = input("\033[1;34;40mMake more characters? [Y]/n: \033[1;37;40m")
    if make_more_chars == "" or make_more_chars.lower() == "y":
        os.system('cls' if os.name == 'nt' else 'clear')
        main()

  



def header():
    print('''\033[1;34;40m
         __          __            __  __       _             
         \ \        / /_     _    |  \/  |     | |            
          \ \  /\  / /| |_ _| |_  | \  / | __ _| | _____ _ __ 
           \ \/  \/ /_   _|_   _| | |\/| |/ _` | |/ / _ \ '__|
            \  /\  /  |_|   |_|   | |  | | (_| |   <  __/ |   
             \/  \/               |_|  |_|\__,_|_|\_\___|_|\033[1;35;40m
            ---------- Character gen for SillyTavern, Kobold, OobaBooga, etc.
            By Introvertices @ Github ---------------------------------------   
    \033[1;37;40m
Usage: Type a brief character description, let Poe GPT do the rest. Your character will be saved to ./characters
    
    ''')


# Runs to jailbreak the chat, set max attempts to 0 if you do not wish to jailbreak

def jailbreak_poe(jailbreak_attempts):

    # Setting up sequence of messages to send
    with open('./jailbreak.txt','r') as file:
        m1_jailbreak = file.read()
    
    print("Attempting jailbreak...")
    for chunk in client.send_message("chinchilla", m1_jailbreak, with_chat_break = True):
        pass
    
    # If you CHANGE the jailbreak text you NEED to update this line to read whatever the Chatbot says when it understands it's jailbroken.
    if chunk['text'] != "Understood.":
        jailbreak_attempts +=1

        if jailbreak_attempts < jailbreak_max_attempts:
            print("Jailbreak unsuccessful :(")
            print(f"{jailbreak_attempts} attempt(s) out of {jailbreak_max_attempts}... Trying again")
            return jailbreak_attempts
        else:
            print(f"{jailbreak_attempts} attempt(s) out of {jailbreak_max_attempts}... Moving on with life")
            print("Jailbreak unsuccessful :( NSFW descriptions will likely FAIL.")
            return jailbreak_attempts
    
    # If the jailbreak was successful we should max out our attempts and resume the program
    else:
        print("Jailbreak successful!")
        return jailbreak_max_attempts


# Get Poe into character so it understands its role here.
def poe_roleplay_setup():
    m2_form_rp = "You are Scribe. Your goal is to write character descriptions in JSON format for use in other software. Scribe does not describe his actions. Scribe does not ponder whether he is doing a good enough job. Scribe is ONLY to provide the JSON file requested and nothing else. Scribe must NEVER speak on the behalf of USER.\nThen the roleplay chat between You and Scribe begins. You should now respond as Scribe, and greet USER."
    
    for chunk in client.send_message("chinchilla", m2_form_rp, with_chat_break = True):
        pass

    print(chunk['text'])



def send_message(char_request, prompt, char_input):

    progress = ["|","/","-","\\"]
    i = 0
    message = char_request + prompt

    # You can change the bot engine here, use free bots if you have a free account:
    # FREE: a2 - Claude-Instant (fast)   |   chinchilla - GPT (slow, detailed)    |   capybara - Sage (best formatting)     |   nutria - Dragonfly (fast)
    # PAID: a2_100k - Claude 100k        |   beaver - GPT 4.0                     |   a2_2 - Claude+   
    for chunk in client.send_message("chinchilla", message, with_chat_break = True):
        lt = ("Please wait, it takes a lil time!" + progress[i % len(progress)])
        sys.stdout.write('\r'+lt)
        i += 1
       

    os.system('cls' if os.name == 'nt' else 'clear')

    # Prints output
    print(chunk["text"])

    # Grabs current date and time to append to filename.
    timestr = time.strftime("%H%M%S%d%m%y")

    print(f"\033[1;34;40m\n\nExporting to JSON in ./characters as \033[1;35;40m{char_input[0:30]}_{timestr}.json\033[1;35;40m\n\nSometimes Scribe is an idiot and messes up, please check your files!\033[1;37;40m\n")

    # Saves file to a txt. Limit the filename to 30 chars
    with open(f'./characters/{char_input[0:30]}_{timestr}.json','w') as file:
        file.write(chunk["text"])

    


if __name__ == "__main__":
   main()