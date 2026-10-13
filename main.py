import string #from standard library, for stripping punctuation from pokedex
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
        print("Invalid Pokédex: first line must be POKEDEX: "
              "followed by a title.\n")
        return None

    title = lines[0][8:].strip()

    #store Pokémon as a dictionary
    pokemon = {}
    names = []
    i = 1

    #pokedex must contain pokemon
    if i >= len(lines):
        print("Invalid Pokédex: it must contain at least one Pokemon.\n")
        return None

    #check if header is valid
    while i < len(lines):
        header = parse_header(lines[i])
        if header is None:
            print("Invalid Pokédex: expected an entry header containing the Pokémon name and number,"
                  "(e.g. #004 Charmander).\n")
            return None

        #tuple unpacking
        number, name = header
        if number <= 0:
            print("Invalid Pokédex: Pokémon number must be positive.\n")
            return None
        i += 1

        #check type exists
        if (i >= len(lines)) or (lines[i][:5]!="Type:"):
            print ("Invalid Pokédex: missing Type for {name}.\n")
            return None

        #check valid number of types
        types = [t.strip() for t in lines[i][6:].split("/")]
        if len(types) > 2 or "" in types:
            print ("Invalid Pokédex: incorrect number of types for {name}.\n")
            return None
        i += 1

        #description - everything left up to net header or eof
        description = []
        while i < len(lines) and parse_header(lines[i]) is None:
            description.append(lines[i].strip())
            i += 1
        if not description:
            print ("Invalid Pokédex: no description for {name}.\n")
            return None

        #check for duplicate numbers or name
        if number in pokemon or name in names:
            print("Invalid Pokédex: Pokemon {name} or {number} already exists in the Pokédex.\n")
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
        return imported_pokemon


#----menu option 2:----
#-----get all words in pokedex-----
def get_all_words(pokemon):
    words = []
    for entry in pokemon.values():
        for line in entry["description"]:
            words.extend(w.lower().strip(string.punctuation) for w in line.split()) #put all words into lowercase
    no_empty_words = []
    for w in words:
        if w: #skip empty strings
            no_empty_words.append(w)
    return no_empty_words

#-----counting distinct words in pokedex descriptions-----
def count_distinct_words(all_words):
    distinct_words = len(set(all_words)) #set only stores unique items, len gives num of items in set
    return distinct_words

#-----get top 10 words in pokedex-----
def get_top_words(all_words, n=20):
    word_counts = {}
    for word in all_words:
        word_counts[word] = word_counts.get(word, 0) + 1

    #sort by total count (highest first), then by alphabet to break any ties
    sorted_words = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))[:10]
    return sorted_words[:n]

#-----sort pokemon by type-----
def sort_pokemon_by_type(pokemon):
    type_counts = {}
    for entry in pokemon.values():
        for t in entry["types"]:
            type_counts[t] = type_counts.get(t, 0) + 1
    sorted_types = sorted(type_counts.items(), key=lambda item: (-item[1], item[0]))
    return sorted_types


#-----building summary of pokedex as a string-----
def build_summary(imported_pokedex):
    title, pokemon = imported_pokedex #tuple unpacking
    all_words = get_all_words(pokemon)
    top_words = get_top_words(all_words)
    sorted_types = sort_pokemon_by_type(pokemon)

    #get total number of pokemon
    total_pokemon = len(imported_pokedex[1]) #dictionary of pokemon

    #get total number of words in all descriptions
    total_words_count = len(all_words)

    #get total number of distinct words
    distinct_words = count_distinct_words(all_words)

    #build string
    lines = []
    lines.append(f"\nFor Pokédex: {title}")
    lines.append(f"\nThe total number of Pokemon: {total_pokemon}")
    lines.append(f"Total number of words: {total_words_count}")
    lines.append(f"Number of distinct words: {distinct_words}")
    lines.append("")
    lines.append("Top 10 most common words:")
    for word, count in top_words:
        lines.append(f" {word}: {count}")
    lines.append("")
    lines.append("Pokemon per type:")
    for t, count in sorted_types:
        lines.append(f"    {t}: {count}")
    return "\n".join(lines)

def print_summary(imported_pokedex):
    #check pokedex exists
    if imported_pokedex is None:
        print("No Pokédex was provided. Please import one first (option 1).\n")
        return
    else:
        print(build_summary(imported_pokedex) + "\n")
    input("Press enter to return to the main menu.\n")

#---menu option 3:---

def save_summary_file(imported_pokedex):
    #check pokedex exists
    if imported_pokedex is None:
        print("No Pokédex was provided. Please import one first (option 1).\n")
        return
    else:
        #write to file, making sure to check for error

    input("Press enter to return to the main menu.\n")

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
        save_summary_file(pokedex)

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