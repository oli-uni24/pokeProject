import math
import sys
from collections import Counter #standard-library modules

#----menu option 1----
#-----parsing pokedex-----
def parse_header(header):
    #check header is valid
    if header[:1] != "#":
        return None #not a valid header

    #tuple unpacking
    poke_num, space, name = header[1:].partition(" ")

    if space != " " or not poke_num.isdecimal() or not name.strip():
        return None #not a valid header

    #valid header - returns number and name of Pokémon
    return int(poke_num), name.strip()


def parse_pokedex(text):
    #ignore empty lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    #must not be empty and start with POKEDEX:
    if not lines or not lines[0].startswith("POKEDEX:"):
        print("Invalid Pokédex: first line must be POKEDEX: "
              "followed by a title.\n")
        return None

    title = lines[0][len("POKEDEX:"):].strip()

    #store Pokémon as a dictionary
    pokemon = {}
    names = []
    i = 1

    #pokedex must contain pokemon
    if i >= len(lines):
        print("Invalid Pokédex: it must contain at least one Pokémon.\n")
        return None

    #check if header is valid
    while i < len(lines):
        header = parse_header(lines[i])
        if header is None:
            print("Invalid Pokédex: expected an entry header containing the Pokémon name and number, "
                  "(e.g. #004 Charmander).\n")
            return None

        #tuple unpacking
        number, name = header
        if number <= 0:
            print("Invalid Pokédex: Pokémon number must be positive.\n")
            return None
        i += 1

        #check type exists
        if (i >= len(lines)) or not (lines[i].startswith("Type:")):
            print(f"Invalid Pokédex: missing Type for {name}.\n")
            return None

        #check valid number of types
        types = [t.strip() for t in lines[i][len("Type:"):].split("/")]
        if len(types) > 2 or "" in types:
            print(f"Invalid Pokédex: incorrect number of types for {name}.\n")
            return None
        i += 1

        #description - everything left up to next header or eof
        description = []
        while i < len(lines) and parse_header(lines[i]) is None:
            description.append(lines[i].strip())
            i += 1
        if not description:
            print(f"Invalid Pokédex: no description for {name}.\n")
            return None

        #check for duplicate numbers or name
        if number in pokemon or name in names:
            print(f"Invalid Pokédex: Pokémon {name} or {number} already exists in the Pokédex.\n")
            return None

        #valid entry
        names.append(name)
        pokemon[number] = {"name": name, "types": types, "description": description}

    print(f"{title} imported successfully.")
    return title, pokemon, build_cache(pokemon)

def import_pokedex(user_file):
    raw_pokedex = user_file.strip() #remove whitespace

    while True:
        if raw_pokedex == "0":
            #return to menu
            return None

        #check valid filename
        if not raw_pokedex.lower().endswith(".txt"):
            raw_pokedex = input("Please ensure the provided file is a text file (e.g. myFavouritePokémon.txt), "
                            "or press 0 to return to the main menu.\n").strip() #remove whitespace
            continue

        #check file exists on disk
        try:
            #open utf-8 file
            with open(raw_pokedex, "r", encoding="utf-8-sig") as file:
                data = file.read()
        except FileNotFoundError:
            raw_pokedex = input("File could not be found. Please ensure the provided file exists, "
                            "or press 0 to return to the main menu.\n").strip() #remove whitespace
            continue
        except OSError:
            print("File could not be opened.\n")
            return None
        except UnicodeDecodeError:
            print("File is not valid UTF-8.\n")
            return None

        return parse_pokedex(data)

#----menu option 2:----
#-----get all words in one entry-----
def get_entry_words(entry):
    words = []
    for line in entry["description"]:
        words.extend(clean_words(line)) #put all words into lowercase
    return words

#-----counting distinct words in pokedex descriptions-----
def count_distinct_words(all_words):
    distinct_words = len(set(all_words)) #set only stores unique items, len gives num of items in set
    return distinct_words

#-----get top 10 words in pokedex-----
def get_top_words(all_words, n=10):
    word_counts = Counter(all_words) #counts how many times each word appears

    #sort by total count (highest first), then by alphabet to break any ties
    sorted_words = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))
    return sorted_words[:n]

#-----sort pokemon by type-----
def sort_pokemon_by_type(pokemon):
    type_counts = Counter()
    for entry in pokemon.values():
        type_counts.update(entry["types"]) #add 1 to count of each type in list
    return sorted(type_counts.items(), key=lambda item: (-item[1], item[0]))

#-----printing summary of pokedex as a string-----
def build_summary(imported_pokedex):
    title, pokemon, cache = imported_pokedex #tuple unpacking

    all_words = []
    for words in cache["words"].values():
        all_words.extend(words)

    top_words = get_top_words(all_words)
    sorted_types = sort_pokemon_by_type(pokemon)

    #get total number of pokemon
    total_pokemon = len(pokemon) #dictionary of pokemon

    #get total number of words in all descriptions
    total_words_count = len(all_words)

    #get total number of distinct words
    distinct_words = count_distinct_words(all_words)

    #build string
    lines = []
    lines.append(f"Summary Report: {title}")
    lines.append(f"\nNumber of Pokémon: {total_pokemon}")
    lines.append(f"Total number of words: {total_words_count}")
    lines.append(f"Number of distinct words: {distinct_words}")
    lines.append("")
    lines.append("Top 10 Words:")
    for n, (word, count) in enumerate(top_words, start=1):
        lines.append(f"{n}. {word}: {count}")
    lines.append("")
    lines.append("Pokémon per type:")
    for n, (t, count) in enumerate(sorted_types, start=1):
        lines.append(f"{n}. {t}: {count}")
    return "\n".join(lines)

#-----building summary of pokedex-----
def print_summary(imported_pokedex):
    #check pokedex exists
    if imported_pokedex is None:
        print("No Pokédex was provided. Please import one first (option 1).\n")
    else:
        print(build_summary(imported_pokedex) + "\n")
    input("Press enter to return to the main menu.\n")

#---menu option 3:---
#-----create text file of pokedex summary-----
def save_summary_file(imported_pokedex):
    #check pokedex exists
    if imported_pokedex is None:
        print("No Pokédex was provided. Please import one first (option 1).\n")
    else:
        #write to file, making sure to check for error
        try:
            with open("summary_pokedex.txt", "w", encoding="utf-8") as file:
                file.write(build_summary(imported_pokedex) + "\n")
            print("Summary saved to summary_pokedex.txt.\n")
        except OSError: #covers writing errors from OS
            print("Could not write to summary_pokedex.txt.\n")

    input("Press enter to return to the main menu.\n")

#---menu option 4:---
#-----standardise words in description-----
def clean_words(text):
    #lowercase everything and treat curly apostrophies the same as straight ones
    text = text.lower().replace("’", "'")

    words = []
    current_word = ""

    for i, char in enumerate(text):
        #if next character is a letter
        next_is_letter =  i + 1 < len(text) and text[i + 1].isalpha()

        if char.isalpha():
            current_word += char
        elif char == "'" and current_word and next_is_letter:
            current_word += char #apostrophe with a letter on either side stays in word
        else:
            #anything else ends current word
            if current_word:
                words.append(current_word)
                current_word = ""

    #if text ends mid word
    if current_word:
        words.append(current_word)

    return words

#-----calculate inverse document frequency per word-----
def calculate_idf(pokemon):
    n = len(pokemon) #number of documents
    doc_frequency = {}
    for entry in pokemon.values():
        for word in set(get_entry_words(entry)): #using set ensures each doc counts once (+1 per description containing word)
            doc_frequency[word] = doc_frequency.get(word, 0) + 1 #creates dictionary - gives 0 if word isn't in dict yet
    idf = {}
    for word, df in doc_frequency.items():
        idf[word] = math.log(n/df)
    return idf

#-----calculate tf-idf score for all words for one pokemon-----
def calculate_tfidf_words(entry, idf):
    #avoid dividing by 0 in case of desc with no words
    words = get_entry_words(entry)
    if not words:
        return {}

    #get freq of word in pokemon desc
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1

    #calculate tf-idf of the word
    scores={}
    for word, count in counts.items():
        tf = count / len(words)
        scores[word] = tf * idf[word]
    return scores

#-----cache everything on pokedex import-----
def build_cache(pokemon):
    idf = calculate_idf(pokemon) #same for whole file - only need it once

    words = {} #all words in each pokemons description
    tfidf = {} #tf-idf of every word in each pokemons description

    for number, entry in pokemon.items():
        words[number] = get_entry_words(entry)
        tfidf[number] = calculate_tfidf_words(entry, idf)

    return {"words": words, "idf": idf, "tfidf": tfidf}

#-----top words in order of tf-idf-----
def get_top_tfidf_words(scores, n=5):
    #sorts by score then alphabet in case of ties
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:n]

#-----find pokemon from user input-----
def find_pokemon(pokemon, query):
    #if user asks for pokemon by its number
    if query.isdecimal():
        number = int(query)
        if number in pokemon:
            return number, pokemon[number]
    #if user asks for pokemon by its name
    else:
        for number, entry in pokemon.items():
            if entry["name"].lower() == query.lower(): #change to lower case
                return number, entry
    return None

#-----print pokemon requested by user-----
def print_pokemon(imported_pokedex):
    if imported_pokedex is None:
        print("No Pokédex was provided. Please import one first (option 1).\n")
        input("Press enter to return to the main menu.\n")
        return

    pokemon = imported_pokedex[1]
    cache = imported_pokedex[2]

    #ask user for pokemon, return None if exited
    result = ask_user_for_pokemon(pokemon)
    if result is None:
        return

    number, entry = result
    words = cache["words"][number]
    scores = cache["tfidf"][number]

    #format output
    print(f"\n#{number:03d} {entry['name']}") #ensure number is 3 dec places (0s before)
    print(f"Type: {' / '.join(entry['types'])}")
    print(f"{' '.join(entry['description'])}")
    print(f"\nNumber of words: {len(words)}")

    print("\nMost frequent words:")
    for num, (word, count) in enumerate(get_top_words(words, 5), start=1):
        print(f"{num}. {word}: {count}")

    print("\nTop TF-IDF keywords:")
    for num, (word, score) in enumerate(get_top_tfidf_words(scores), start=1):
        print(f"{num}. {word}: {score:.4f}")

    print()
    input("Press enter to return to the main menu.\n")

#---menu option 5:---
def search_pokedex(pokemon, query, tfidf):
    search_results = []
    for number, entry in pokemon.items():
        scores = tfidf[number]
        total = sum(scores.get(w, 0) for w in query)
        if total > 0: #score of 0 to be ignored
            search_results.append((number, entry["name"], total))

    #order by highest score first
    search_results.sort(key=lambda sr: (-sr[2], sr[0])) #if scores are equal, sort by lower pokedex num first
    return search_results[:5]

#-----search menu/ui-----
def search_menu(imported_pokedex):
    if imported_pokedex is None:
        print("No Pokédex was provided. Please import one first (option 1).\n")
        input("Press enter to return to the main menu.\n")
        return

    pokemon = imported_pokedex[1]

    #keep asking until a word is entered
    while True:
        query = clean_words(input("Search for: "))
        if query:
            break
        print("Please enter at least one word.\n")

    query = sorted(set(query)) #remove repeated words
    cache = imported_pokedex[2]
    idf = cache["idf"]

    #words that don't appear at all
    not_found = [w for w in query if w not in idf]
    if not_found:
        print(f"\nNot found in Pokédex: {', '.join(not_found)}")

    result = search_pokedex(pokemon, query, cache["tfidf"])

    if not result:
        print("\nNo Pokémon match your search criteria.\n")
    else:
        print("\nBest matches:")
        for rank, (number, name, score) in enumerate(result, start=1):
            print(f"{rank}. #{number:03d} {name} (score {score:.4f})")

    print()
    input("Press enter to return to the main menu.\n")

#---menu option 6:---
#-----similarity between two pokemons tf-idf scores-----
def cosine_similarity(scores1, scores2):
    #get overlap sum
    overlap_sum = 0

    for word, score1 in scores1.items():
        if word in scores2:
            score2 = scores2[word]  #get score for scores2 if word also exists in it
            overlap_sum += score1 * score2 #multiply the two scores and add to the overlap sum

    #get scores1s totals
    sum_square_1 = 0
    for score in scores1.values():
        sum_square_1 += score * score #square scores and add together

    total1 = math.sqrt(sum_square_1) #square root of score1

    #get scores2 totals
    sum_square_2 = 0
    for score in scores2.values():
        sum_square_2 += score * score #square scores and add together

    total2 = math.sqrt(sum_square_2) #square root of score2

    #avoid dividing by 0 if either pokemon has only 0 scores
    if total1 == 0 or total2 == 0:
        return 0

    #final division
    return overlap_sum / (total1 * total2)

#-----find the 3 most similar pokemon to the entered one-----
def find_similar(pokemon, number, tfidf):
    target = tfidf[number]
    results = []

    for n, entry in pokemon.items():
        if n == number: #don't compare pokemon to itself
            continue
        similarity = cosine_similarity(target, tfidf[n])
        if similarity > 0: #don't include similarity score of 0
            results.append((n, entry["name"], similarity))

    #highest similarity ordered first, then by lowest pokedex number for ties
    results.sort(key=lambda sr: (-sr[2], sr[0]))
    return results[:3]

#-----ask user for pokemon and return the number & entry, or error -----
def ask_user_for_pokemon(pokemon):
    while True:
        print("Pokédex Search System")
        user_pokemon = input("Enter a Pokémon name or a Pokédex number "
                             "(or 0 to return to the main menu):\n").strip()
        if user_pokemon=="0":
            return None
        result = find_pokemon(pokemon, user_pokemon)
        if result is not None:
            return result
        print("Pokémon not found, please check the name or number.\n")

#-----actual menu function-----
def similar_menu(imported_pokedex):
    if imported_pokedex is None:
        print("No Pokédex was provided. Please import one first (option 1).\n")
        input("Press enter to return to the main menu.\n")
        return

    pokemon = imported_pokedex[1]

    result = ask_user_for_pokemon(pokemon)
    if result is None:
        return
    number, entry = result

    cache = imported_pokedex[2]
    similar = find_similar(pokemon, number, cache["tfidf"])

    if not similar:
        print(f"\nNo Pokémon match your search criteria of {entry['name']}.\n")
    else:
        print(f"Most similar:")
        for rank, (similar_number, name, score) in enumerate(similar, start=1):
            print(f"{rank}. #{similar_number:03d} {name} (score {score:.4f})")

    print()
    input("Press enter to return to the main menu.\n")


#---main menu:---
def main():
    pokedex = None #empty until user imports

    #allow user to select valid menu option
    while True:
        selected_menu_item = input("Select an option:\n"
                                   "1. Import a Pokédex from a text file.\n"
                                   "2. Print a summary report.\n"
                                   "3. Output the summary report to a text file.\n"
                                   "4. View details of a Pokémon.\n"
                                   "5. Search the Pokédex.\n"
                                   "6. Find similar Pokémon.\n"
                                   "0. Exit.\n").strip()

        if selected_menu_item == "1":
            result = import_pokedex(input("Please enter the name of the .txt file containing the Pokédex (e.g. myFavouritePokémon.txt), "
                                          "or 0 to return to the main menu:\n ").strip())
            #validation for imported pokedex
            if result is not None:
                pokedex = result

        elif selected_menu_item == "2":
            print_summary(pokedex)

        elif selected_menu_item == "3":
            save_summary_file(pokedex)

        elif selected_menu_item == "4":
            print_pokemon(pokedex)

        elif selected_menu_item == "5":
            search_menu(pokedex)

        elif selected_menu_item == "6":
            similar_menu(pokedex)

        #exit program
        elif selected_menu_item == "0":
            sys.exit()

        #invalid option
        else:
            print("Please select a valid option.\n")

if __name__ == "__main__":
    main()