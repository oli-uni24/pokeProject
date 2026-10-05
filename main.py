import sys

#---menu option 1:---
#import pokedex
def import_pokedex(user_file):
    pokedex = user_file.strip() #remove whitespace

    while True:
        if pokedex == "0":
            #return to menu
            return None

        #check valid filename
        if pokedex[-4:] != ".txt":
            pokedex = input("Please ensure the provided file is a text file (e.g. myFavouritePokemon.txt), "
                            "or press 0 to return to the main menu.\n").strip() #remove whitespace
            continue

        #check file exists on disk
        try:
            with open(pokedex, "r") as file:
                data = file.read()

            #check data is valid pokedex


            return data
        except FileNotFoundError:
            pokedex = input("File could not be found. Please ensure the provided file exists, "
                         "or press 0 to return to the main menu.\n").strip() #remove whitespace


#---menu option 2:---


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
        import_pokedex(input("Please enter the name of the .txt file containing the Pokédex (e.g. myFavouritePokemon.txt):\n "))
    elif selected_menu_item == "2":
        print("nothing yet")
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