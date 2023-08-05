from data_access import init_db, debug
from business_logic import (
    print_all_players,
    generate_tournament_bracket,
    start_tournament,
    update_rounds,
)


def main():
    init_db()
    print("Options:")
    print("1) Player stats")
    print("2) Start Tournament")
    print("3) Debug")
    print("4) Exit")

    while True:
        choice = input("Please choose an option: ")

        if choice == "1":
            print_all_players()
        elif choice == "2":
            start_tournament()
        elif choice == "3":
            print_all_players()
            debug()
        elif choice == "4" or choice == "q":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
