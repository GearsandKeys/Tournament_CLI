import random
from data_access import (
    get_players,
    get_player_stats,
    create_tournament_and_return_id,
    create_round,
    get_rounds_without_winner,
    update_winner,
    get_player_name,
    get_tournament_rankings,
)


def shuffle_and_group_players(players):
    shuffled_players = random.sample(players, len(players))

    half_length = len(shuffled_players) // 2

    shuffled_group_a = shuffled_players[:half_length]
    shuffled_group_b = shuffled_players[half_length:]

    return shuffled_group_a, shuffled_group_b


def start_tournament():
    players = get_players()

    shuffled_group_a, shuffled_group_b = shuffle_and_group_players(players)

    tournament_id = create_tournament_and_return_id()

    for round_number in range(1, 4):
        print("\n")
        print(f"Round {round_number}")
        for i in range(len(shuffled_group_a)):
            player1 = shuffled_group_a[i]
            player2 = shuffled_group_b[i]
            create_round(tournament_id, round_number, player1[0], player2[0])
            print(f"{player1[1]} vs {player2[1]}")

        # Here, logic to ask who won
        update_rounds()

        # Rotate the players in group B for the next round
        shuffled_group_b = [shuffled_group_b[-1]] + shuffled_group_b[:-1]

    # Print final rankings
    final_scores = get_tournament_rankings(tournament_id)
    print_tournament_rankings(final_scores)


def print_tournament_rankings(rankings: tuple) -> None:
    print("FINAL RANKINGS")
    for rank, (player_name, wins, losses, win_loss_ratio) in enumerate(
        rankings, start=1
    ):
        win_rate_percentage = 0.0
        if losses == 0:
            win_rate_percentage = 100.0
        else:
            win_rate_percentage = (wins / (wins + losses)) * 100

        print(f"{rank}. {player_name} - {win_rate_percentage:.2f}%")


def generate_tournament_bracket():
    players = get_players()

    shuffled_group_a, shuffled_group_b = shuffle_and_group_players(players)

    tournament_id = create_tournament_and_return_id()

    for round_number in range(1, 4):
        print("\n")
        print(f"Round {round_number}")
        for i in range(len(shuffled_group_a)):
            player1 = shuffled_group_a[i]
            player2 = shuffled_group_b[i]
            create_round(tournament_id, round_number, player1[0], player2[0])
            print(f"{player1[1]} vs {player2[1]}")

        # Rotate the players in group B for the next round
        shuffled_group_b = [shuffled_group_b[-1]] + shuffled_group_b[:-1]


def print_all_players():
    players = get_players()

    print("List of all players:")
    for player_stats in players:
        player_id, player_name = player_stats
        wins, losses, win_loss_ratio = get_player_stats(
            player_id,
        )

        print(
            f"{player_id} {player_name} Wins: {wins}, Losses: {losses}, Win Rate: {win_loss_ratio:.2f}%"
        )


def update_rounds():
    rounds_without_winner = get_rounds_without_winner()

    for round_info in rounds_without_winner:
        round_id, round_number, player1_id, player2_id = round_info
        print("\n")
        print(
            f"Round {round_number}: {get_player_name(player1_id)} vs {get_player_name(player2_id)}"
        )

        winner_choice = input(f"Which player won? (1 or 2): ")
        if winner_choice == "1":
            update_winner(round_id, player1_id, player2_id)
            print("Round updated with Player 1 as the winner.")
        elif winner_choice == "2":
            update_winner(round_id, player2_id, player1_id)
            print("Round updated with Player 2 as the winner.")
        else:
            print("Invalid choice. Round not updated.")
