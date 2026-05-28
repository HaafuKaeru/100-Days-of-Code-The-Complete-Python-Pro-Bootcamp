# TODO: Create a letter using starting_letter.txt
# for each name in invited_names.txt
# Replace the [name] placeholder with the actual name.
# Save the letters in the folder "ReadyToSend".
    
#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

def main():

    invitees = []
    with open("./Input/Names/invited_names.txt", 'r') as file_names:
        for line in file_names:
            invitees.append(line.strip())

    starting_letter_str = ""
    with open("./Input/Letters/starting_letter.txt", 'r') as file_letter:
        starting_letter_str += file_letter.read().strip()

    for invitee in invitees:
        with open(f"./Output/ReadyToSend/letter_for_{invitee}.txt", 'w') as f:
            f.write(starting_letter_str.replace("[name]", invitee))


if __name__ == '__main__':
    main()
