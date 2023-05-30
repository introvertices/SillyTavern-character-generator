import poe


# Put your Poe token here, you can get this by going to the dev console of your browser and pasting the p-b value of the cookie in the cookies section
token = "YOUR TOKEN"


client = poe.Client(token)




def main():

    header()
    
    char_input = input("Briefly describe your character: ")
    char_request = "Write me a W++ description in for " + char_input

    with open('./w++prompt.txt','r') as file:
        prompt = file.read()

    print("")
    send_message(char_request, prompt, char_input)

  



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

def send_message(char_request, prompt, char_input):
    
    message = char_request + prompt

    print("Please wait, it takes a lil time :)\n\n") 

    # You can change the bot engine here, use free bots if you have a free account:
    # FREE: a2 - Claude-Instant   |   chinchilla - GPT    |   capybara - Sage     |   nutria - Dragonfly
    # PAID: a2_100k - Claude 100k |   beaver - GPT 4.0    |   a2_2 - Claude+   
    for chunk in client.send_message("chinchilla", message, with_chat_break = True):
        pass
       

    # Prints output
    print(chunk["text"])

    # Saves file to a txt
    with open(f'./characters/{char_input}.txt','w') as file:
        file.write(chunk["text"])

    


if __name__ == "__main__":
   main()