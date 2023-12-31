"""
---------------------
    Ballot_Box.py
---------------------
    implements a class "Ballot_box", that serves as a parent for the Double_Ballot_box, and the Regular_Ballot_box.
    it has a property called parties that stores all the political parties.

    methods:

    - GetVote:
        takes a vote (string),
        and returns a Note with a valid vote in it.

    - Validate:
        takes a vote (string),
        and returns True if it is valid, False otherwise

    - Revote:
        returns a new vote (string)
"""


from Main import Note


class Ballot_box:
    def __init__(self, parties: list):
        self.parties = parties

    def GetVote(self, vote: str):
        while not self.Validate(vote):
            vote = self.Revote()
        return Note(vote)

    def Validate(self, vote: str):
        return vote in self.parties

    def Revote(self):
        return input("Your vote was invalid, please vote again: ")

    def Connect(self):
        """
            this method is responsible for connecting to the server,
            then sending the data, and finally disconnecting from the server
        """
        pass

    def send(self):
        """
            this method is responsible for sending the data to the server
        """
        pass
