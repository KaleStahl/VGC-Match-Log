"""
Match.py.

Pokemon class to create a match with Pokepaste data and notes.

Author: Kale Stahl
Last Modified: 5/17/2023

"""
import fileinput
import Parser
import Leads
import Team

class Match:
    """Match class to store data of a battle."""

    def __init__(self, name = "", teamName = "", team= Team.Team(), oppTeam = Team.Team(), notes = "", Leads = Leads.Leads()):
        """
        Initialize match class.

        Parameters
        ----------
        name : string
            Name of match.
        teamName : string
            Name of team used.
        team : Team
            Data of team used.
        oppTeam : Team
            Opponent's team.
        notes : string
            Note on match.

        Returns
        -------
        None.

        """
        self.name = name
        self.teamName = teamName
        self.team = team
        self.oppTeam = oppTeam
        self.notes = notes
        self.leads = Leads

    def __str__(self):
        """
        Initialize match as string.

        Returns
        -------
        paste : string
            Collection of data about match.

        """
        paste = ""
        paste += "Match Name: {} \n".format(self.name)
        paste += "Team Name: {} \n".format(self.teamName)
        paste += "Team Used: \n"
        paste += str(self.team)+ "\n-teamend-\n\n"
        paste += "Opponents Team: \n"
        paste += str(self.oppTeam)+ "\n-teamend-\n\n"
        #
        paste += "\nYour Lead: "
        for lead1 in self.leads.yourLead:
            paste += str(lead1)+ "; "
        paste += "\nYour Back: "
        for back1 in self.leads.yourBack:
            paste += str(back1)+ "; "
        paste += "\nOpponents Lead: "
        for lead2 in self.leads.oppLead:
            paste += str(lead2)+ "; "
        paste += "\nOpponents Back: "
        for back2 in self.leads.oppBack:
            paste += str(back2)+ "; "
        #
        paste += "\nNotes: \n"
        paste += self.notes + "\n\n>-----<\n\n"
        return paste

    def readMatch(self, matchFile):
        """
        Read match data from given file.

        Parameters
        ----------
        matchFile : string
            Location of file to read.

        Returns
        -------
        matchList : Match
        Created match.

        """
        matchList = []
        match = Match()

        # Copies match data to new file
        tempFile = 'temp_files/temp_match_list.txt'
        with open(matchFile,'r') as firstfile, open(tempFile,'a') as secondfile:
            for line in firstfile:
                 secondfile.write(line)

        fileinput.close()
        fileIn = open(matchFile)
        notesBlock = False
        for line in fileIn:
            line.rstrip()
            if(line.find("Match Name:") != -1):
                match.name = line[line.find(": ")+1:].rstrip().lstrip()
            if(line.find("Team Name:") != -1):
                match.teamName = line[line.find(": ")+1:].rstrip().lstrip()
            if(line.find("Team Used:") != -1):
                parser1 = Parser.Parser()
                match.team = parser1.parse(tempFile)
                teamFile = open(tempFile, 'r')
                teamString = teamFile.read()
                teamFile.close()
                removeTeam = teamString[teamString.index("teamend-")+7:-1].rstrip().lstrip()
                teamFile = open(tempFile, 'w')
                teamFile.write(removeTeam)
                teamFile.close()
            if(line.find("Opponents Team:") != -1):
                parser2 = Parser.Parser()
                match.oppTeam = parser2.parse(tempFile)
                teamOppFile = open(tempFile, 'r')
                teamOppString = teamOppFile.read()
                removeOppTeam = teamOppString[teamOppString.index("teamend-")+7: -1]
                teamOppFile = open(tempFile, 'w')
                teamOppFile.write(removeOppTeam)
                teamOppFile.close()
            if(line.find("Your Lead:") != -1):
                firstMon = line[line.find(": ")+1:line.find(";")].rstrip().lstrip()
                match.leads.yourLead.append(firstMon)
                secondMon = line[line.find(";")+1:line.find(";", line.find(";")+1)].rstrip().lstrip()
                match.leads.yourLead.append(secondMon)
            if(line.find("Your Back:") != -1):
                firstMon = line[line.find(": ")+1:line.find(";")].rstrip().lstrip()
                match.leads.yourBack.append(firstMon)
                secondMon = line[line.find(";")+1:line.find(";", line.find(";")+1)].rstrip().lstrip()
                match.leads.yourBack.append(secondMon)
            if(line.find("Opponents Lead:") != -1):
                firstMon = line[line.find(": ")+1:line.find(";")].rstrip().lstrip()
                match.leads.oppLead.append(firstMon)
                secondMon = line[line.find(";")+1:line.find(";", line.find(";")+1)].rstrip().lstrip()
                match.leads.oppLead.append(secondMon)
            if(line.find("Opponents Back:") != -1):
                firstMon = line[line.find(": ")+1:line.find(";")].rstrip().lstrip()
                match.leads.oppBack.append(firstMon)
                secondMon = line[line.find(";")+1:line.find(";", line.find(";")+1)].rstrip().lstrip()
                match.leads.oppBack.append(secondMon)
            if(line.find(">-----<") != -1):
                matchList.append(match)
                del match
                match = Match()
                notesBlock = False
            if(notesBlock == True):
                match.notes += line
            if(line.find("Notes:") != -1):
                notesBlock = True
        # Clears temp file
        teamFile = open(tempFile, 'w')
        teamFile.write("")
        teamFile.close()
        fileinput.close()

        return matchList

    def getChanges(self, newteam):
        team = self.team.pokemon
        changes = ""
        nonPokeChanges = []
        pokeChanges = []
        for poke in team:
            for newpoke in newteam:
                if(poke.name == newpoke.name):
                    nonPokeChanges.append(newpoke)
        for newpoke in newteam:
            if(nonPokeChanges.count(newpoke) == 0):
                pokeChanges.append(newpoke)
        for changePoke in nonPokeChanges:
            for poke in team:
                if(changePoke.name == poke.name):
                    changes += "\n" + poke.name + "\n"
                    if(changePoke.item != poke.item):
                        changes += "Item: {} --> {}\n".format(poke.item, changePoke.item)
                    if(changePoke.ability != poke.ability):
                        changes += "Ability: {} --> {}\n".format(poke.ability, changePoke.ability)
                    if(changePoke.tera != poke.tera):
                        changes += "Tera Type: {} --> {}\n".format(poke.tera, changePoke.tera)
                    stat_label = ["{} HP", "{} Atk", "{} Def", "{} SpA", "{} SpD", "{} Spe"]
                    if(changePoke.evs != poke.evs):
                        changeEvs = ""
                        ev_count = 0
                        for ev in range(6):
                            if(changePoke.evs[ev] != 0):
                                ev_count += 1
                                changeEvs += stat_label[ev].format(changePoke.evs[ev])
                                if(ev_count < 6-changePoke.evs.count(0)):
                                    changeEvs += " / "
                        oldEvs = ""
                        ev_count = 0
                        for ev in range(6):
                            if(changePoke.evs[ev] != 0):
                                ev_count += 1
                                oldEvs += stat_label[ev].format(poke.evs[ev])
                                if(ev_count < 6-poke.evs.count(0)):
                                    oldEvs += " / "
                        changes += "EVs: {}\n --> {}\n".format(oldEvs, changeEvs)
                    if(changePoke.ivs != poke.ivs):
                        changeivs = ""
                        iv_count = 0
                        for iv in range(6):
                            if(changePoke.ivs[iv] != 0):
                                iv_count += 1
                                changeivs += stat_label[iv].format(changePoke.ivs[iv])
                                if(iv_count < 6-changePoke.ivs.count(0)):
                                    changeivs += " / "
                        oldivs = ""
                        iv_count = 0
                        for iv in range(6):
                            if(changePoke[iv] != 0):
                                iv_count += 1
                                oldivs += stat_label[iv].format(poke[iv])
                                if(iv_count < 6-poke.ivs.count(0)):
                                    oldivs += " / "
                        changes += "IVs: {}\n --> {}\n".format(oldivs, changeivs)
                    if(changePoke.moves != poke.moves):
                        oldMoves = ""
                        newMoves = ""
                        for move in poke.moves:
                            if(changePoke.moves.count(move) == 0):
                                oldMoves += move
                                newMoves += changePoke.moves[poke.moves.index(move)]
                        changes += "Moves: {} --> {}\n".format(oldMoves,newMoves)
        return changes
