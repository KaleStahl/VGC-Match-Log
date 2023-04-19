"""
leads.py.

Class to create leads for matches.

Author: Kale Stahl
Last Modified: 4/18/2023

"""

class Leads:

    def __init__(self, yourLead=[], oppLead=[], yourBack= [], oppBack = []):
        self.yourLead = yourLead
        self.yourBack = yourBack
        self.oppLead = oppLead
        self.oppBack = oppBack
