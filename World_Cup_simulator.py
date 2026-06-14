print("=" * 50)
print("     World Cup 2026 Country Simulator")
print("=" * 50)

country = input("Enter your country name: ").strip()
matches_played = 0
wins = 0
draws = 0
losses = 0
eliminated = False

print(f"\n{country} has entered the World Cup 2026!")
print("Let's see if they can win it all!\n")

rounds = ["Group Stage", "Round of 16", "Quarter Final", "Semi Final", "Final"]

for round_name in rounds:

    if eliminated:
        break

    print(f"\n{'=' * 50}")
    print(f"  {round_name}")
    print(f"{'=' * 50}")

    while True:
        print(f"\nWhat happened in the {round_name}?")
        print("  1. Win")
        print("  2. Draw")
        print("  3. Loss")
        print("  4. VAR Review")

        choice = input("\nEnter choice (1/2/3/4): ").strip()

        if choice == "1":
            wins += 1
            matches_played += 1
            print(f"\n{country} won the {round_name}! Advancing to the next round.")
            break

        elif choice == "2":
            # In knockout stages a draw means penalty shootout
            if round_name != "Group Stage":
                print(f"\nDraw in a knockout stage! Going to penalties...")
                penalty = input(
                    "Did you win the penalty shootout? (yes/no): ").strip().lower()
                if penalty == "yes":
                    wins += 1
                    matches_played += 1
                    print(f"{country} won on penalties! Advancing.")
                    break
                else:
                    losses += 1
                    matches_played += 1
                    eliminated = True
                    print(f"{country} lost on penalties. Eliminated!")
                    break
            else:
                draws += 1
                matches_played += 1
                print(
                    f"\nDraw in the Group Stage. {country} still in the tournament.")
                break

        elif choice == "3":
            losses += 1
            matches_played += 1
            eliminated = True
            print(f"\n{country} lost the {round_name} and has been eliminated.")
            break

        elif choice == "4":
            # pass: placeholder — future feature will add VAR review system
            pass
            print(
                f"\nVAR is reviewing a decision in {round_name}. No change for now.")
            continue  # go back and ask again since round isn't decided yet

        else:
            # continue goes back to the top of the while loop to ask again
            print("Invalid choice. Please enter 1, 2, 3 or 4.")
            continue

print(f"\n{'=' * 50}")
print(f"       {country} - World Cup 2026 Report")
print(f"{'=' * 50}")
print(f"Matches played : {matches_played}")
print(f"Wins           : {wins}")
print(f"Draws          : {draws}")
print(f"Losses         : {losses}")

if wins == 5:
    print(f"\nCONGRATULATIONS! {country} WON THE WORLD CUP 2026!")
elif eliminated:
    print(f"\n{country} was eliminated. Better luck next time!")
else:
    print(f"\n{country} had a decent run in the tournament!")
