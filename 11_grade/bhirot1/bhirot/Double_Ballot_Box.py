"""
----------------------------
    Double_ballot_box.py
----------------------------
    implements a class "Double_Ballot_box", that serves as a ballot box that's found abroad.
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

    - vote:
        takes a vote (string), and voter (Voter),
        returns an envelope with a Note that contains a valid vote on it
"""

from Double_Envelope import Double_Envelope
from Envelope import Envelop
from Note import Note
from Voter import Voter
from Ballot_Box import Ballot_box
import socket


class Double_ballot_box(Ballot_box):
    def __init__(self, parties):
        Ballot_box.__init__(self, parties)

    def vote(self, vote: str, voter: Voter):
        vote = self.GetVote(vote)
        vote = Note(vote)
        env = Envelope([vote])
        return Double_Envelope(voter.name, voter.id_number, env)

    def send(self):
        name = input("Your name: ")
        id = input("Your ID: ")
        vote = input("Choose tour vote: ")
        double_env = self.vote(vote, Voter(name, id))

        self.socket.send(double_env)#TODO add binary


if __name__ == "__main__":
    box = Double_ballot_box(["a"])
    box.Connect()



