"""
Parser.py.

Parser class to extract team from Pokepaste.

Author: Kale Stahl
Last Modified: 3/9/2023
"""

import Pokemon
import Team
import fileinput

class Parser:
    """Parser class."""

    def makeTeam(self, pokemon):
        """
        Make a team from given pokemon.

        Parameters
        ----------
        pokemon : list
            A list containing Pokemon in the team.

        Returns
        -------
        Team
            Team containing the passed Pokemon.

        """
        return Team.Team(pokemon)

    def getName(self, line):
        """
        Retrieve name from given line of pokepaste.

        Parameters
        ----------
        line : string
            Line of Pokepaste to extract name from.

        Returns
        -------
        nickname : string
            Trimmed name of the pokemon.

        """
        if(line.find("(") != -1):
            name = line[line.find("(")+1: line.find(")")]
        else:
            name = line[0: line.find("@")]
        return name.lstrip().rstrip()

    def getNickname(self, line):
        """
        Retrieve nickname from given line of pokepaste.

        Parameters
        ----------
        line : string
            Line of Pokepaste to extract nickname from.

        Returns
        -------
        nickname : string
            Trimmed nickname of the pokemon.

        """
        if(line.find("(") != -1):
            nickname = line[0: line.find("(")-1].lstrip().rstrip()
        else:
            nickname = None
        return nickname

    def getItem(self, line):
        """
        Retrieve item from given line of pokepaste.

        Parameters
        ----------
        line : string
            Line of Pokepaste to extract item from.

        Returns
        -------
        item : string
            Trimmed item of the pokemon.

        """
        if(line.find("@") != -1):
            item = line[line.find("@")+1: -1]
        else:
            item = None
        return item.lstrip().rstrip()

    def getAbility(self, line):
        """
        Retrieve ability from given line of pokepaste.

        Parameters
        ----------
        line : string
            Line of Pokepaste to extract ability from.

        Returns
        -------
        nickname : string
            Trimmed ability of the pokemon.

        """
        ability = line[line.find(":")+1: -1]
        return ability.lstrip().rstrip()

    def getTera(self, line):
        """
        Retrieve tera type from given line of pokepaste.

        Parameters
        ----------
        line : string
            Line of Pokepaste to extract tera type from.

        Returns
        -------
        tera : string
            Trimmed tera type of the pokemon.

        """
        tera = line[line.find(":")+1: -1]
        return tera.lstrip().rstrip()

    def getEvs(self, line):
        """
        Retrive effort values from given line of Pokepaste.

        Parameters
        ----------
        line : string
            Line of Pokepaste to extract effort values from.

        Returns
        -------
        evs : list
            List of effort values of the Pokemon.

        """
        evs = []
        stat_label = ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]
        for i in range(6):
            loc = line.find(stat_label[i])
            if(loc != -1):
                stat = line[loc-4: loc]
                if(stat.find("/") != -1 or stat.find(":") != -1):
                    stat = stat[1::]
                evs.append(int(stat.lstrip().rstrip()))
            else:
                evs.append(0)
        return evs

    def getIvs(self, line):
        """
        Retrive individual values from given line of Pokepaste.

        Parameters
        ----------
        line : string
            Line of Pokepaste to extract individual values from.

        Returns
        -------
        evs : list
            List of individual values of the Pokemon.

        """
        ivs = []
        stat_label = ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]
        for i in range(6):
            loc = line.find(stat_label[i])
            if(loc != -1):
                stat = line[loc-3: loc]
                ivs.append(int(stat.lstrip().rstrip()))
            else:
                ivs.append(31)
        return ivs

    def getNature(self, line):
        """
        Retrieve nature from given line of pokepaste.

        Parameters
        ----------
        line : string
            Line of Pokepaste to extract nature from.

        Returns
        -------
        nature : string
            Trimmed nature of the pokemon.

        """
        nature = line[0: line.find("Nature")-1]
        nature.lstrip().rstrip()
        return nature

    def getMove(self, line):
        """
        Retrieve move from given line of pokepaste.

        Parameters
        ----------
        line : string
               Line of Pokepaste to extract move from.

        Returns
        -------
        moves: string
            Trimmed move of the Pokemon.

        """
        moves = line[line.find("-")+1: -1]
        moves.lstrip().rstrip()
        return moves

    def parse(self, pasteLocation):
        """
        Parse a Pokepaste to create a Team object.

        Parameters
        ----------
        pasteLocation : string
            File location of pokepaste to pass to fileinput.

        Returns
        -------
        Team
            Team gathered from parsing Pokepaste.

        """
        pokemon_count = 0
        first_line = True
        IVs_Added = False
        team = []
        cur_poke = Pokemon.Pokemon("","", "","", [], [], "","","", [])
        fileinput.close()
        fileIn = fileinput.input(pasteLocation)
        for line in fileIn:
            line.rstrip()
            if(line.find("teamend-") != -1):
                break
            if(pokemon_count < 6):
                if(line.find("(") != -1 or line.find("@") != -1):
                    if(first_line):
                        cur_poke = Pokemon.Pokemon("","", "","", [], [], "","","", [])
                        first_line = False
                    else:
                        team.append(cur_poke)
                        del cur_poke
                        cur_poke = Pokemon.Pokemon("","", "", "", [], [], "","","", [])
                        pokemon_count += 1
                        IVs_Added = False
                    cur_poke.name = self.getName(line)
                    if(line.count("(") > 1):
                        cur_poke.gender = line[line.find("(",line.find("(")+1)+1: line.find(")", line.find(")")+1)]
                        cur_poke.nickname = self.getNickname(line)
                    elif(self.getName(line)== "M" or self.getName(line) == "F"):
                        cur_poke.gender = self.getName(line)
                        cur_poke.name = self.getNickname(line)
                        cur_poke.nickname = None
                    elif(line.count("(") == 1):
                        cur_poke.gender = None
                        cur_poke.nickname = self.getNickname(line)
                    else:
                        cur_poke.gender = None
                        cur_poke.nickname = None
                    cur_poke.item = self.getItem(line)
                if(line.find("Ability: ") != -1):
                    cur_poke.ability = self.getAbility(line)
                if(line.find("Tera Type: ") != -1):
                    cur_poke.tera = self.getTera(line)
                if(line.find("EVs: ") != -1):
                    cur_poke.evs = self.getEvs(line)
                if(line.find("IVs: ") != -1):
                    cur_poke.ivs = self.getIvs(line)
                    IVs_Added = True
                elif(IVs_Added == False):
                    cur_poke.ivs = [31, 31, 31, 31, 31, 31]
                if(line[0] == "-"):
                    cur_poke.moves.append(self.getMove(line))
                if(line.find(" Nature") != -1):
                    cur_poke.nature = self.getNature(line)
            else:
                team.append(cur_poke)
                break
        team.append(cur_poke)
        fileIn.close()
        # print(self.makeTeam(team))
        return self.makeTeam(team)