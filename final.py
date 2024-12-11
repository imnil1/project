import os
import time
import random
import matplotlib.pyplot as plt
from datetime import datetime

# Declaring some variables
welcomeMsg = """\n\033[1mEnter the choice you want to use\033[0m
1. Read previous score
2. Add a new game
3. Remove previous saved score
4. Quit
"""

# Function to add team players to a list
def playerNameInTeam(teamName, howManyPlayersPlaying):
    teamPlayers = []
    print(f"\nEnter players for {teamName}:")
    for i in range(howManyPlayersPlaying):
        while True:
            players = input(f"Enter the {i + 1} player of {teamName}: ").strip()
            if players:
                teamPlayers.append(players)
                break
            else:
                print("Player name cannot be empty. Please enter a valid name.")
    
    return teamPlayers

# Adding player names to file (using fixed filename "cricket.txt")
def addingPlayerNameInFile(teamName, teamPlayers, file):
    file.write(f"Team Name: {teamName}\n")
    for i, player in enumerate(teamPlayers):
        file.write(f"{i + 1}: {player}\n")

# Function to handle the toss process
def doToss(teamName1, teamName2):
    print("\nNow doing the toss...\n")
    time.sleep(2)  # Simulate a delay to create a toss effect
    
    # Randomly select the toss winner
    tossWinner = random.choice([teamName1, teamName2])
    print(f"{tossWinner} won the toss!")

    # Ask for their decision
    while True:
        batOrBowl = input(f"What does {tossWinner} choose to do (bat/bowl)? ").lower()
        if batOrBowl in ["bat", "bowl"]:
            break
        else:
            print("Please enter a valid option (bat/bowl).")

    return tossWinner, batOrBowl

# This function executes every inning
def Play(teamName, howManyOverTheMatchIs, howManyPlayersPlaying, opponentTeamName):
    score = 0
    wickets = 0
    extras = 0
    currentBall = 1  # Track the actual number of valid balls
    currentOver = 1
    ballsInOver = 0
    runsPerOver = []  # Track runs per over
    extrasPerOver = []  # Track extras per over
    wicketsPerOver = []  # Track wickets per over

    print(f"\n\033[1mInnings of {teamName} has started\033[0m\n")

    while currentOver <= howManyOverTheMatchIs:
        print(f"\nBall {currentBall} - Over {currentOver}.{ballsInOver + 1}")
        print("1. Runs\n2. Dot ball\n3. Wicket\n4. Wide Ball/No Ball\n5. Force Quit")

        # Get user input for ball status
        while True:
            try:
                choice = int(input("Enter the choice here: "))
                if choice not in [1, 2, 3, 4, 5]:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")

        runsInThisBall = 0  # Track runs for this ball

        if choice == 1:  # Runs
            while True:
                try:
                    howManyRunsGot = int(input("How many runs did the batsman score? "))
                    if howManyRunsGot < 0:
                        raise ValueError
                    score += howManyRunsGot
                    runsInThisBall = howManyRunsGot
                    break
                except ValueError:
                    print("Please enter a valid number of runs (non-negative).")
            ballsInOver += 1
            currentBall += 1  # Increment for a valid ball

        elif choice == 2:  # Dot ball
            ballsInOver += 1
            currentBall += 1  # Increment for a valid ball

        elif choice == 3:  # Wicket
            ballsInOver += 1
            currentBall += 1  # Increment for a valid ball
            wickets += 1
            if wickets == howManyPlayersPlaying - 1:
                print("All out!")
                break

        elif choice == 4:  # Wide Ball / No Ball (extra run)
            extras += 1
            score += 1
            runsInThisBall = 1  # Extra is counted as a run but not a valid ball

        elif choice == 5:  # Force quit
            print("Exiting the match.")
            return

        # Update runs, extras, and wickets per over
        if ballsInOver == 6:  # End of over
            runsPerOver.append(score)
            extrasPerOver.append(extras)
            wicketsPerOver.append(wickets)  # Track wickets lost in this over
            currentOver += 1
            ballsInOver = 0  # Reset for the next over
            extras = 0  # Reset extras for the new over
            wickets = 0  # Reset wickets for the new over

    return score, runsPerOver, extrasPerOver, wicketsPerOver  # Return score and stats for graphing

# Function to plot the graph of runs scored per over
# Function to plot the graph of runs scored per over
def plotRunsGraph(team1Score, team1RunsPerOver, team1ExtrasPerOver, team1WicketsPerOver,
                  team2Score, team2RunsPerOver, team2ExtrasPerOver, team2WicketsPerOver,
                  team1Name, team2Name, filename='match_score_comparison.png'):
    # Calculate total runs including extras
    total_team1_runs = team1Score + sum(team1ExtrasPerOver)
    total_team2_runs = team2Score + sum(team2ExtrasPerOver)
    
    # Generate overs based on number of entries
    overs = list(range(1, len(team1RunsPerOver) + 1))
    
    # Create a figure
    plt.figure(figsize=(12, 6))

    # Bar Graph for Runs
    bar_width = 0.35
    index = range(len(overs))

    # Create bars for both teams
    plt.bar(index, team1RunsPerOver, bar_width, label=team1Name, color='blue', alpha=0.7)
    plt.bar([i + bar_width for i in index], team2RunsPerOver, bar_width, label=team2Name, color='orange', alpha=0.7)

    # Adding markers for wickets
    # Calculate the positions for the wickets
    team1WicketsPositions = [i + bar_width / 2 for i in index]  # Centered on the bars
    team2WicketsPositions = [i + bar_width + bar_width / 2 for i in index]  # Centered on the bars

    # Scatter plot for wickets
    plt.scatter(team1WicketsPositions, team1WicketsPerOver, color='red', marker='o', label=f'Wickets ({team1Name})', s=100)
    plt.scatter(team2WicketsPositions, team2WicketsPerOver, color='green', marker='o', label=f'Wickets ({team2Name})', s=100)

    # Adding labels and title
    plt.xlabel('Overs')
    plt.ylabel('Runs')
    plt.title('Cricket Match Score Comparison')
    plt.xticks([i + bar_width / 2 for i in index], overs)  # Center the x-ticks
    plt.legend()
    plt.grid(axis='y')

    plt.tight_layout()

    # Check if the file already exists and modify the filename if necessary
    base_filename, file_extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(new_filename):
        new_filename = f"{base_filename}_{counter}{file_extension}"
        counter += 1

    # Save the figure
    plt.savefig(new_filename, format='png')  # You can change 'png' to 'pdf', 'svg', etc.
    print(f"Figure saved as {new_filename}")

    # Show the plot
    plt.show()

# Function for reading previous scores
def choice1():
    try:
        with open('cricket.txt', 'r') as file:
            print("\n\033[1mScore\033[0m\n")
            allTheContent = file.read()
            print(allTheContent)
            print("______________________________________\n")
    except FileNotFoundError:
        print("\n\033[1mNo score exists\033[0m")
        print("_______________")

# Function to write match results to cricket.txt
def writeMatchResult(winner):
    try:
        with open("cricket.txt", "a") as file:
            file.write(f"\n\nMatch Result: {winner}\n")  # Added an extra newline
    except Exception as e:
        print(f"Error saving match result: {e}")

def choice3():
    # Function for removing previous scores
    try:
        os.remove("cricket.txt")
        print("\033[1mPrevious Scores Removed\033[0m")
    except FileNotFoundError:
        print("\n\033[1mNo score exists\033[0m")
        print("______________")
        
    # Remove all graph files with .png extension
    graph_files = [f for f in os.listdir() if f.endswith('.png')]
    if graph_files:
        for graph_file in graph_files:
            os.remove(graph_file)
            print(f"\033[1mRemoved graph: {graph_file}\033[0m")
    else:
        print("\033[1mNo graph exists to remove\033[0m")

# Function to get a valid team name
def getValidTeamName(prompt):
    while True:
        team_name = input(prompt).strip()
        if team_name:
            return team_name
        else:
            print("Team name cannot be empty. Please enter a valid name.")

# Starting the program
def main():
    while True:
        print("\033[1m\nWelcome to our Cricket Scoreboard software\033[0m")
        print(welcomeMsg)

        while True:
            try:
                choice = int(input("Enter your choice (1, 2, 3, or 4): "))
                if choice not in [1, 2, 3, 4]:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter a valid option.\n")

        if choice == 1:
            choice1()  # Read previous scores

        elif choice == 2:
            team1Name = getValidTeamName("Enter team 1 name: ")
            team2Name = getValidTeamName("Enter team 2 name: ")

            while True:
                try:
                    howManyPlayersPlaying = int(input("How many players are playing (from one team) in the match? "))
                    if howManyPlayersPlaying < 1:
                        raise ValueError("Number of players must be greater than 0.")
                    break
                except ValueError:
                    print("Enter a valid number greater than 0.\n")

            team1Players = playerNameInTeam(team1Name, howManyPlayersPlaying)  # Get team 1 players
            team2Players = playerNameInTeam(team2Name, howManyPlayersPlaying)  # Get team 2 players

            # Write player names to fixed file 'cricket.txt'
            with open("cricket.txt", "a") as file:
                addingPlayerNameInFile(team1Name, team1Players, file)  # Write team 1 players to file
                addingPlayerNameInFile(team2Name, team2Players, file)  # Write team 2 players to file

            while True:
                try:
                    howManyOverTheMatchIs = int(input("Enter how many overs this match is: "))
                    if howManyOverTheMatchIs < 1:
                        raise ValueError
                    break
                except ValueError:
                    print("Please enter a valid number of overs (greater than 0).")

            # Write match details (overs) to the file
            with open("cricket.txt", "a") as file:
                file.write(f"\nMatch overs: {howManyOverTheMatchIs}\n")

            # Call the toss function and get the toss result
            whoWonTheToss, batOrBowl = doToss(team1Name, team2Name)

            # Write the toss results to the file
            with open("cricket.txt", "a") as file:
                file.write(f"{whoWonTheToss} won the toss and chose to {batOrBowl} first\n")

            # Declare variables to store scores of both teams
            team1Score = 0
            team2Score = 0
            team1RunsPerOver = []
            team2RunsPerOver = []
            team1ExtrasPerOver = []
            team2ExtrasPerOver = []
            team1WicketsPerOver = []
            team2WicketsPerOver = []

            # Start the match
            if whoWonTheToss == team1Name:
                if batOrBowl == "bat":
                    team1Score, team1RunsPerOver, team1ExtrasPerOver, team1WicketsPerOver = Play(team1Name, howManyOverTheMatchIs, howManyPlayersPlaying, team2Name)  # Pass team2Name
                    print("\033[1mInnings 1 finished\033[0m")
                    team2Score, team2RunsPerOver, team2ExtrasPerOver, team2WicketsPerOver = Play(team2Name, howManyOverTheMatchIs, howManyPlayersPlaying, team1Name)  # Pass team1Name
                else:
                    team2Score, team2RunsPerOver, team2ExtrasPerOver, team2WicketsPerOver = Play(team2Name, howManyOverTheMatchIs, howManyPlayersPlaying, team1Name)  # Pass team1Name
                    print("\033[1mInnings 1 finished\033[0m")
                    team1Score, team1RunsPerOver, team1ExtrasPerOver, team1WicketsPerOver = Play(team1Name, howManyOverTheMatchIs, howManyPlayersPlaying, team2Name)  # Pass team2Name
            else:
                if batOrBowl == "bat":
                    team2Score, team2RunsPerOver, team2ExtrasPerOver, team2WicketsPerOver = Play(team2Name, howManyOverTheMatchIs, howManyPlayersPlaying, team1Name)  # Pass team1Name
                    print("\033[1mInnings 1 finished\033[0m")
                    team1Score, team1RunsPerOver, team1ExtrasPerOver, team1WicketsPerOver = Play(team1Name, howManyOverTheMatchIs, howManyPlayersPlaying, team2Name)  # Pass team2Name
                else:
                    team1Score, team1RunsPerOver, team1ExtrasPerOver, team1WicketsPerOver = Play(team1Name, howManyOverTheMatchIs, howManyPlayersPlaying, team2Name)  # Pass team2Name
                    print("\033[1mInnings 1 finished\033[0m")
                    team2Score, team2RunsPerOver, team2ExtrasPerOver, team2WicketsPerOver = Play(team2Name, howManyOverTheMatchIs, howManyPlayersPlaying, team1Name)  # Pass team1Name

            # Calculate Strike Rate and Run Rate for both teams
            team1BallsFaced = sum(team1RunsPerOver)  # Total balls faced by team 1
            team2BallsFaced = sum(team2RunsPerOver)  # Total balls faced by team 2

            # Calculate Strike Rate
            team1StrikeRate = (team1Score / team1BallsFaced) * 100 if team1BallsFaced > 0 else 0
            team2StrikeRate = (team2Score / team2BallsFaced) * 100 if team2BallsFaced > 0 else 0

            # Calculate Run Rate
            team1OversFaced = team1BallsFaced / 6
            team2OversFaced = team2BallsFaced / 6
            team1RunRate = team1Score / team1OversFaced if team1OversFaced > 0 else 0
            team2RunRate = team2Score / team2OversFaced if team2OversFaced > 0 else 0

            # Display results in console
            print(f"\033[1mFinal Score: {team1Name}: {team1Score} vs {team2Name}: {team2Score}\033[0m")
            print(f"{team1Name} Strike Rate: {team1StrikeRate:.2f}")
            print(f"{team2Name} Strike Rate: {team2StrikeRate:.2f}")
            print(f"{team1Name} Run Rate: {team1RunRate:.2f}")
            print(f"{team2Name} Run Rate: {team2RunRate:.2f}")

            # Write results to the text file
            with open("cricket.txt", "a") as file:
                file.write(f"\nFinal Score: {team1Name}: {team1Score} vs {team2Name}: {team2Score}\n")
                file.write(f"{team1Name} Strike Rate: {team1StrikeRate:.2f}\n")
                file.write(f"{team2Name} Strike Rate: {team2StrikeRate:.2f}\n")
                file.write(f"{team1Name} Run Rate: {team1RunRate:.2f}\n")
                file.write(f"{team2Name} Run Rate: {team2RunRate:.2f}\n")

            # Compare scores and display the result
            if team1Score > team2Score:
                print(f"{team1Name} wins!")
                winner = f"{team1Name} wins!"
            elif team1Score < team2Score:
                print(f"{team2Name} wins!")
                winner = f"{team2Name} wins!"
            else:
                print("It's a tie!")
                winner = "It's a tie!"

            # Write the winner to the fixed file 'cricket.txt'
            writeMatchResult(winner)

            # Plot the graph only after the match is finished
            plotRunsGraph(team1Score, team1RunsPerOver, team1ExtrasPerOver, team1WicketsPerOver, team2Score, team2RunsPerOver, team2ExtrasPerOver, team2WicketsPerOver, team1Name, team2Name, filename='match_score_comparison.png')
        elif choice == 3:
            choice3()  # Remove previous scores

        elif choice == 4:
            print("Thank you for using the cricket scoreboard!")
            break

        else:
            print("Invalid choice, please try again.\n")

if __name__ == "__main__":
    main()