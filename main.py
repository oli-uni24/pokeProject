import sys

#fix name print part
#pack pokemon and title on parser return

#store variables
title = None
pokedex = None

#----menu option 1----
#-----parsing pokedex-----
def parse_header(header):
    #check header is valid
    if header[:1] != "#":
        return None #not a valid header

    #tuple unpacking
    poke_num, space, name = header[1:].partition(" ")

    if space != " " or not poke_num.isdigit() or not name.strip():
        return None #not a valid header

    #valid header - returns number and name of Pokémon
    return int(poke_num), name.strip()


def parse_pokedex(pokedex):
    #ignore empty lines
    lines = [line.strip() for line in pokedex.split("\n") if line.strip()]

    #must not be empty and start with POKEDEX:
    if not lines or lines[0][:8] != "POKEDEX:":
        print("Invalid Pokedex: first line must be POKEDEX: "
              "followed by a title.\n")
        return None

    title = lines[0][8:].strip()

    #store Pokémon as a dictionary
    pokemon = {}
    names = []
    i = 1

    #pokedex must contain pokemon
    if i >= len(lines):
        print("Invalid Pokedex: it must contain at least one Pokemon.\n")
        return None

    #check if header is valid
    while i < len(lines):
        header = parse_header(lines[i])
        if header is None:
            print("Invalid Pokedex: expected an entry header containing the Pokémon name and number,"
                  "(e.g. #004 Charmander).\n")
            return None

        #tuple unpacking
        number, name = header
        if number <= 0:
            print("Invalid Pokedex: Pokémon number must be positive.\n")
            return None
        i += 1

        #check type exists
        if (i >= len(lines)) or (lines[i][:5]!="Type:"):
            print ("Invalid Pokedex: missing Type for {name}.\n")
            return None

        #check valid number of types
        types = [t.strip() for t in lines[i][6:].split("/")]
        if len(types) > 2 or "" in types:
            print ("Invalid Pokedex: incorrect number of types for {name}.\n")
            return None
        i += 1

        #description - everything left up to net header or eof
        description = []
        while i < len(lines) and parse_header(lines[i]) is None:
            description.append(lines[i].strip())
            i += 1
        if description == []:
            print ("Invalid Pokedex: no description for {name}.\n")
            return None

        #check for duplicate numbers or name
        if number in pokemon or name in names:
            print("Invalid Pokedex: Pokemon {name} or {number} already exists in the Pokedex.\n")
            return None

        #valid entry
        names.append(name)
        pokemon[number] = {"name": name, "types": types, "description": description}

    return title, pokemon

def import_pokedex(user_file):
    raw_pokedex = user_file.strip() #remove whitespace

    while True:
        if raw_pokedex == "0":
            #return to menu
            return None

        #check valid filename
        if raw_pokedex[-4:] != ".txt":
            raw_pokedex = input("Please ensure the provided file is a text file (e.g. myFavouritePokemon.txt), "
                            "or press 0 to return to the main menu.\n").strip() #remove whitespace
            continue

        #check file exists on disk
        try:
            #open utf-8 file
            with open(raw_pokedex, "r", encoding="utf-8") as file:
                data = file.read()
        except FileNotFoundError:
            raw_pokedex = input("File could not be found. Please ensure the provided file exists, "
                            "or press 0 to return to the main menu.\n").strip() #remove whitespace
            continue
        except UnicodeDecodeError:
            print("File is not valid UTF-8.\n")
            return None

        imported_pokemon = parse_pokedex(data)
        print(imported_pokemon) # temp testing
        return imported_pokemon


#----menu option 2:----

#-----counting distinct words in pokedex descriptions-----
def count_distinct_words(imported_pokedex):
    #get all descriptions
    all_descriptions = [pokemon["description"] for pokemon in imported_pokedex[1].values()]

    #flatten list of lists into a single list of words
    all_words = []
    for description in all_descriptions:
        words = description.split() #split description into words
        all_words.extend(words) #add words to all_words list
    distinct_words = []

    #find out if word is already in distinct_words list, if not add it
    for word in all_words:
        if word not in distinct_words:
            distinct_words.append(word)

    return distinct_words


#-----printing summary of pokedex-----
def print_summary(imported_pokedex):
    #get total number of pokemon
    total_pokemon = len(imported_pokedex[1]) #dictionary of pokemon

    #get total number of words in all descriptions
    total_words = sum(len(pokemon["description"]) for pokemon in imported_pokedex[1].values())

    #get number of distinct words in all descriptions - using IDF
    distinct_words = count_distinct_words(imported_pokedex)



    print("The total number of Pokemon:\n"
          "Total number of words:\n"  #all descriptions concatenated?
          "Number of distinct words:\n " #using function
          "Top 10 words:\n" #using function
          "Pokemon per type:\n" #print type and number in loop
    )

#---menu option 3:---


#---menu option 4:---


#---menu option 5:---


#---menu option 6:---





#---main menu:---
#allow user to select valid menu option

while True:
    selected_menu_item = input("Select an option:\n"
                               "1. Import a Pokédex from a text file.\n"
                               "2. Print a summary report.\n"
                               "3. Output the summary report to a text file.\n"
                               "4. View details of a Pokémon.\n"
                               "5. Search the Pokédex.\n"
                               "6. Find similar Pokémon.\n"
                               "0. Exit.\n")

    if selected_menu_item == "1":
        result = import_pokedex(input("Please enter the name of the .txt file containing the Pokédex (e.g. myFavouritePokemon.txt):\n "))
        #validation for imported pokedex
        if result is not None:
            pokedex = result


    elif selected_menu_item == "2":
        print_summary(pokedex)


    elif selected_menu_item == "3":
        print("nothing yet")
    elif selected_menu_item == "4":
        print("nothing yet")
    elif selected_menu_item == "5":
        print("nothing yet")
    elif selected_menu_item == "6":
        print("nothing yet")
    #exit program
    elif selected_menu_item == "0":
        sys.exit()
    #invalid option
    else :
        print("Please select a valid option.\n")