"""
Team.py.

Team class to compile a team of Pokemon from a paste.

Author: Kale Stahl
Last Modified: 3/4/2023

"""

class Team: 
    """Team Class."""
    
    def __init__(self, pokemon):
        """
        Initialize the Team with a list of up to 6 pokemon.

        Parameters
        ----------
        pokemon : list of Pokemon
            Up to 6 pokemon to add to the team.

        Returns
        -------
        None.

        """
        self.pokemon = pokemon
        
    def __str__(self):
        """
        Format the Team to return in a format that Showdown can read.

        Returns
        -------
        paste : string
            A string with proper formatting for Showdown import.

        """
        paste = ""
        for poke in self.pokemon:
            paste += "{} \n".format(poke)
        return paste
