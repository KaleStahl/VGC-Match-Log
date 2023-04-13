"""
Pokemon.py.

Pokemon class to create a pokemon with Pokepaste data.

Author: Kale Stahl
Last Modified: 4/13/2023
"""
class Pokemon:
    """Pokemon class."""

    def __init__(self, name, nickname, gender, tera, ivs, evs, nature, ability, item, moves):
        """
        Intialize the Pokemon class.

        Parameters
        ----------
        name : string
            Name of Pokemon.
        nickname : string
            Nickname of Pokemon.
        gender : string
            Gender of Pokemon.
        tera : string
            Tera Type of Pokemon.
        ivs : list if int
            List of the individual values of a pokemon in the order:
                HP, ATK, DEF, SPA, SPD, SPE.
        evs : list of int
            List of the effort values of a pokemon in the order:
                HP, ATK, DEF, SPA, SPD, SPE.
        nature : string
            Nature of Pokemon.
        ability : string
            Ability of Pokemon.
        item : string
            Held Item of Pokemon.
        moves : list of string
            List of up to four moves of the Pokemon.

        Returns
        -------
        None.

        """
        self.name = name
        self.nickname = nickname
        self.gender = gender
        self.tera = tera
        self.ivs = ivs
        self.evs = evs
        self.ability = ability
        self.item = item
        self.moves = moves
        self.nature = nature

    def __str__(self):
        """
        Format the Pokemon object in a manner that is readable by Showdown.

        Returns
        -------
        paste : string
            A string in the format of Showdown Pastes.

        """
        paste = ""
        if(self.nickname != None and self.nickname != ""):
            paste += "{} ({})".format(self.nickname, self.name)
        else:
            paste = "{}".format(self.name)
        if(self.gender != None and self.gender != "--" and self.gender != ""):
            paste += " ({})".format(self.gender)
        if(self.item != None and self.item != ""):
            paste += " @ {}\n".format(self.item)
        else:
            paste += "\n"
        if(self.ability != None and self.ability != ""):
            paste += "Ability: {}\n".format(self.ability)
        if(self.tera != None and self.tera != ""):
            paste += "Tera Type: {}\n".format(self.tera)
        stat_label = ["{} HP", "{} Atk", "{} Def", "{} SpA", "{} SpD", "{} Spe"]
        if(self.evs != [0,0,0,0,0,0] and self.evs != None and self.evs != []):
            paste += "EVs: "
            ev_count = 0
            for ev in range(6):
                if(self.evs[ev] != 0):
                    ev_count += 1
                    paste += stat_label[ev].format(self.evs[ev])
                    if(ev_count < 6-self.evs.count(0)):
                        paste += " / "
            paste += "\n"
        if(self.ivs != [31,31,31,31,31,31] and self.ivs != None and self.ivs != []):
            paste += "IVs: "
            iv_count = 0
            for iv in range(6):
                if(self.ivs[iv] != 31):
                    iv_count += 1
                    paste += stat_label[iv].format(self.ivs[iv])
                    if(iv_count < 6-self.ivs.count(31)):
                        paste += " / "
            paste += "\n"
        if(self.nature != None and self.nature != ""):
            paste += "{} Nature\n".format(self.nature)
        if(self.moves != [] and self.moves != None):
            for move in self.moves:
                paste += "- {}\n".format(move)
        return paste
