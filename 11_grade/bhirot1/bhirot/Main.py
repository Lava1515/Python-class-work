from Ballot_Box import Ballot_box


class Note:
    def __init__(self, name):
        self.name = name


class Envelope:
    def __init__(self, notes: list):
        self.notes = notes

    # returns a tuple of (bool, Note), (False, None) if not successful
    def status(self):
        validate = self._validate()
        if not validate:
            return False, None
        is_valid = len(validate) == len(self.notes)
        if not is_valid:    # in order to not get out of bounds exception
            return False, None
        return is_valid, self.notes[0]  # successful

    def _validate(self):
        if len(self.notes) < 0 or len(self.notes) > 5:  # invalid length
            return False
        return [x for x in self.notes if x == self.notes[0]]


class Double_Envelope:
    def __init__(self, name, id_number, envelope):
        self.envelope = envelope
        self.id_number = id_number
        self.name = name


class Voter:
    def __init__(self, name: str, id_number: int):
        self.name = name
        self.id_number = id_number

    def Getname(self):
        return self.name

    def GetID(self):
        return self.id_number


class Double_ballot_box(Ballot_box):
    def __init__(self, parties):
        Ballot_box.__init__(self, parties)

    def vote(self, vote: str, voter: Voter) -> Double_Envelope:
        vote = self.GetVote(vote)
        vote = Note(vote)
        env = Envelope([vote])
        return Double_Envelope(voter.name, voter.GetID(), env)

    def send(self):
        """
            this method is responsible for taking the double envelope that vote returns, and send it to the server,
            it would overwrite the send method of the Ballot Box
        """
        pass


class Regular_Ballot_Box(Ballot_box):
    def __init__(self, parties):
        Ballot_box.__init__(self, parties)
        self.voters = []

    def vote(self, vote: str, voter: Voter):
        vote = self.GetVote(vote)
        self.voters.append(voter)
        vote = Note(vote)
        env = Envelope([vote])
        return env

    def send(self):
        """
            this method is responsible for taking the envelope that vote returns, and send it to the server,
            it could overwrite the send method of the Ballot Box, if needed
        """
        pass