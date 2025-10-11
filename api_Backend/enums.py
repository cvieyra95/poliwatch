from enum import Enum


class Party(str, Enum):
    Democratic   = "Democratic"
    Republican   = "Republican"
    Independent  = "Independent"
    Libertarian  = "Libertarian"
    Other        = "Other"

class Chamber(str, Enum):
    House  = "House"
    Senate = "Senate"

class VotePosition(str, Enum):
    Yea        = "Yea"
    Nay        = "Nay"
    Present    = "Present"
    NotVoting  = "Not Voting"
    Absent     = "Absent"
    Unknown    = "Unknown"

class CommitteeRole(str, Enum):
    Chair          = "Chair"
    RankingMember  = "Ranking Member"
    ViceChair      = "Vice Chair"
    Member         = "Member"
    ExOfficio      = "Ex Officio"
    Other          = "Other"


class BillType(str, Enum):
    HR       = "HR"
    S        = "S"
    HRES     = "HRES"
    SRES     = "SRES"
    HJRES    = "HJRES"
    SJRES    = "SJRES"
    HCONRES  = "HCONRES"
    SCONRES  = "SCONRES"