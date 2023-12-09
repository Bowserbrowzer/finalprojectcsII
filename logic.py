import csv
from PyQt6.QtCore import QFile
from PyQt6.QtWidgets import *

from gui import Ui_MainWindow


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Define a set to store used voting IDs
        self.used_voting_ids = set()

        # Define a list of valid voting IDs
        self.valid_voting_ids = list(range(1, 11))

        # Dictionary to store vote count for each candidate
        self.vote_count = {}

        # Dictionary to track which voter ID is voting for which candidate
        self.voter_candidates = {}

        # Connect the "Submit" button to the submit method
        self.pushButton.clicked.connect(self.submit)

        # Connect a custom method to display results
        self.pushButton.clicked.connect(self.display_results)

    def submit(self):
        # Get the entered voting ID from the QLineEdit
        voting_id_text = self.lineEdit.text()

        try:
            # Convert the entered ID to an integer
            voting_id = int(voting_id_text)

            # Check if the entered ID is in the list of valid IDs
            if voting_id in self.valid_voting_ids:
                if voting_id not in self.used_voting_ids:
                    # Get the selected candidate and convert to lowercase
                    candidate = self.lineEdit_2.text().lower()

                    # Check if the candidate is a string and not a numeric value
                    if not isinstance(candidate, str) or candidate.isdigit():
                        self.show_error_message("Error", "Candidate name must be a non-numeric string.")
                        return

                    # Update the vote count for the candidate
                    self.vote_count[candidate] = self.vote_count.get(candidate, 0) + 1

                    # Track which voter ID is voting for which candidate
                    self.voter_candidates[voting_id] = candidate

                    # Mark the voting ID as used
                    self.used_voting_ids.add(voting_id)

                    # Save voting information to CSV file
                    self.save_to_csv(voting_id, candidate)

                    print(f"Voting ID {voting_id} for {candidate} accepted. Thank you for voting.")
                else:
                    self.show_error_message("Error", f"Voting ID {voting_id} has already been used. Please enter a different ID.")
            else:
                # Display an error message for invalid IDs
                self.show_error_message("Error", f"Invalid voting ID: {voting_id}. Please enter a valid ID.")

        except ValueError:
            # Display an error message for non-numeric input
            self.show_error_message("Error", "Invalid input. Please enter a numeric voting ID.")

    def display_results(self):
        # Display the results in the QListWidget
        self.listWidget.clear()
        for candidate, votes in self.vote_count.items():
            result_text = f"{candidate}: {votes} votes"
            self.listWidget.addItem(result_text)

        # Check if all ten votes are in
        if len(self.used_voting_ids) == 10:
            # Determine the winner
            winner = max(self.vote_count, key=self.vote_count.get)
            winner_votes = self.vote_count[winner]

            # Display the winner in the QListWidget
            winner_message = f"\nWinner: {winner} with {winner_votes} votes"
            self.listWidget.addItem(winner_message)

    def save_to_csv(self, voter_id, candidate):
        # Save voting information to CSV file
        file_path = 'voting_results.csv'
        fieldnames = ['Voter ID', 'Candidate']

        # Check if the file exists
        file_exists = QFile(file_path).exists()

        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header if the file is created or empty
            if not file_exists or csvfile.tell() == 0:
                writer.writeheader()

            # Write voting information
            writer.writerow({'Voter ID': voter_id, 'Candidate': candidate})

    def show_error_message(self, title, message):
        error_box = QMessageBox(self)
        error_box.setWindowTitle(title)
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setText(message)
        error_box.exec()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Logic()
    window.show()
    sys.exit(app.exec())
