"""
User_Interface.py.

Class to manage interaction with user interface.

Author: Kale Stahl
Last Modified: 4/18/2023

"""
import tkinter as tk
import Parser
import Match
import Leads
import Pokemon
from tkinter import ttk
from tkinter.filedialog import asksaveasfile, askopenfilename
import math

class UserInterface:
    """Class to create the application GUI."""

    _MatchLog = []
    _MatchName = []
    _LeadLog = []
    _Team = []
    _TeamName = []
    _IsSaved = True
    curMatch = -1
    curTeam = -1

    global _curTeamPaste
    global _newMatchButton
    global _deleteMatchButton
    global _deleteTeamButton
    global _addTeamButton
    global _curTeamPaste
    global _menuBar
    global _fileMenu
    global _helpMenu
    global _teamSelect
    global _matchSelect
    global _selectedTeam
    global _pasteFrame
    global _matchFrame

    def __init__(self, ux):
        self._ux = ux

    def uxReadMe(self):
        """
        Event handler for README menu bar item.

        Returns
        -------
        None.

        """
        from os import startfile
        startfile("README.txt")

    def uxGithub(self):
        """
        Event handler for GitHub menu bar item.

        Returns
        -------
        None.

        """
        import webbrowser
        webbrowser.open_new("https://github.com/KaleStahl/VGC-Match-Log.git")

    def uxOpenFile(self):
        """
        Event handler for Open Team Log menu bar item.

        Returns
        -------
        None.

        """
        try:
            if(self._IsSaved == False):
                if(len(self._MatchName) != 0):
                    response = tk.messagebox.askyesnocancel("Save Progress", "Would you like to save your current match log?", icon ='question')
                    if(response == True):
                        self.uxSaveFile()
                    elif(response == None):
                        return
            path = askopenfilename()
            if not path:
                return
            matchHelp = Match.Match(None, None, None, None, None)
            self._MatchName.clear()
            self._TeamName.clear()
            self._Team.clear()
            self._MatchLog = matchHelp.readMatch(path)
            for match in self._MatchLog:
                self._MatchName.append(match.name)
                if(match.teamName not in self._TeamName):
                    self._TeamName.append(match.teamName)
                    self._Team.append(match.team)
            self.updateListbox(self._teamSelect, self._TeamName)
            self._teamSelect.select_set(0)
            self.updateListbox(self._matchSelect, self._MatchName)
            self._matchSelect.select_set(0)
            self._deleteMatchButton.config(state =tk.NORMAL)
            self._deleteTeamButton.config(state =tk.NORMAL)
            self._newMatchButton.config(state =tk.NORMAL)
            self._IsSaved = True
        except Exception as e:
            tk.messagebox.showerror('Open Team Log Error', 'Error: An error occurred. \nError Code: ' + str(e))

    def uxSaveFile(self):
        """
        Event handler for Save Team Log menu bar item.

        Returns
        -------
        None.

        """
        try:
            file = asksaveasfile(title="Select Location", filetypes=(("Text Files", "*.txt"),))
            if not file:
                return
            text2save = ""
            for match in self._MatchLog:
                text2save += str(match)
            file.write(text2save)
            file.close()
            self._IsSaved = True
        except Exception as e:
            tk.messagebox.showerror('Save Team Log Error', 'Error: An error occurred. \nError Code: ' + str(e))

    def uxNewFile(self):
        """
        Event handler for New Team Log menu bar item.

        Returns
        -------
        None.

        """
        try:
            if(self._IsSaved == False):
                if(len(self._MatchName) != 0):
                    response = tk.messagebox.askyesnocancel("Save Progress", "Would you like to save your current match log?", icon ='question')
                    if(response == True):
                        self.uxSaveFile()
                    elif(response == None):
                        return
            self._MatchLog = []
            self._MatchName = []
            self._Team = []
            self._TeamName = []
            self.updateListbox(self._matchSelect, self._MatchName)
            self.updateListbox(self._teamSelect, self._TeamName)
            self._IsSaved = True
        except Exception as e:
            tk.messagebox.showerror('New Team Log Error', 'Error: An error occurred. \nError Code: ' + str(e))

    def uxExportOpponentsTeams(self):
        """
        Export all opponent's teams to a PokePaste.

        Returns
        -------
        None.

        """
        newWindow = tk.Toplevel(self._ux)
        newWindow.title("Export Opponent's Teams")
        newWindow.lift()
        newWindow.attributes('-topmost',True)
        newWindow.after_idle(newWindow.attributes,'-topmost',False)
        newWindow.geometry("500x450")

        frame = tk.Frame(newWindow, padx = 10, pady =10)
        frame.pack()
        PokePaste = tk.Text(frame)
        PokePaste.pack(side = "left",fill = 'y' )

        # Adds scrollbar functionality
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        PokePaste.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = PokePaste.yview)

        teamstr = ""
        for match in self._MatchLog:
            teamstr += "=== " + str(match.name) +" === \n \n"
            teamstr += str(match.oppTeam)
        PokePaste.delete(1.0, tk.END)
        PokePaste.insert(tk.END, teamstr)
        PokePaste.config(state=tk.DISABLED)

    def uxExportTeams(self):
        """
        Export all teams to a PokePaste.

        Returns
        -------
        None.

        """
        newWindow = tk.Toplevel(self._ux)
        newWindow.title("Export Teams")
        newWindow.lift()
        newWindow.attributes('-topmost',True)
        newWindow.after_idle(newWindow.attributes,'-topmost',False)
        newWindow.geometry("500x450")

        frame = tk.Frame(newWindow, padx = 10, pady =10)
        frame.pack()
        PokePaste = tk.Text(frame)
        PokePaste.pack(side = "left",fill = 'y' )

        # Adds scrollbar functionality
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        PokePaste.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = PokePaste.yview)

        teamstr = ""
        for i in range(len(self._Team)):
            teamstr += "=== " + str(self._TeamName[i]) +" === \n \n"
            teamstr += str(self._Team[i])
        PokePaste.delete(1.0, tk.END)
        PokePaste.insert(tk.END, teamstr)
        PokePaste.config(state=tk.DISABLED)


    def generatePaste(self, text,pokemon, nature, tera, ivs,evs, item, moves, ability):
        poke = Pokemon.Pokemon(name = pokemon,
                               nickname = None,
                               gender = None,
                               nature = nature.get(),
                               tera = tera.get(),
                               ivs =[ivs[0].get(),ivs[1].get(),ivs[2].get(),ivs[3].get(),ivs[4].get(),ivs[5].get()],
                               evs =[evs[0].get(),evs[1].get(),evs[2].get(),evs[3].get(),evs[4].get(),evs[5].get()],
                               ability = ability.get(),
                               item = item,
                               moves =[moves[0].get(), moves[1].get(),moves[2].get(),moves[3].get()]
                               )
        text.delete(1.0, tk.END)
        text.insert(tk.END, str(poke))
        text.config(state=tk.DISABLED)
        return

    def uxGeneratePokepaste(self):
        newWindow = tk.Toplevel(self._ux)
        newWindow.title("PokePaste Generator")
        newWindow.lift()
        newWindow.attributes('-topmost',True)
        newWindow.after_idle(newWindow.attributes,'-topmost',False)
        newWindow.geometry("600x600")

        newWindow.rowconfigure(0, weight = 1)
        newWindow.rowconfigure(1, weight = 1)
        newWindow.rowconfigure(2, weight = 1)
        newWindow.rowconfigure(3, weight = 1)
        newWindow.rowconfigure(4, weight = 1)
        newWindow.rowconfigure(5, weight = 1)
        newWindow.rowconfigure(6, weight = 1)
        newWindow.rowconfigure(7, weight = 1)
        newWindow.rowconfigure(8, weight = 1)
        newWindow.rowconfigure(9, weight = 1)
        newWindow.rowconfigure(10, weight = 5)
        newWindow.columnconfigure(0, weight = 2)
        newWindow.columnconfigure(1, weight = 1)
        newWindow.columnconfigure(2, weight = 1)
        newWindow.columnconfigure(3, weight = 1)
        newWindow.columnconfigure(4, weight = 1)
        newWindow.columnconfigure(5, weight = 1)
        newWindow.columnconfigure(6, weight = 1)
        newWindow.columnconfigure(7, weight = 1)
        newWindow.columnconfigure(8, weight = 1)

        # Adds labels
        tk.Label(newWindow, text = "Pokemon:").grid(row = 0, column = 0, sticky = "e")
        pokemon = tk.Entry(newWindow)
        pokemon.grid(row =0, column = 1, columnspan = 6, sticky = "w")

        tk.Label(newWindow, text = "Item:").grid(row = 1, column = 0, sticky = "e")
        item_value = tk.StringVar(newWindow)
        item = tk.Entry(newWindow, textvariable=item_value)
        item.grid(row =1, column = 1, columnspan = 6, sticky = "w")

        tk.Label(newWindow, text = "Ability:").grid(row = 2, column = 0, sticky = "e")
        ability = tk.Entry(newWindow)
        ability.grid(row =2, column = 1, columnspan = 6, sticky = "w")

        tk.Label(newWindow, text = "Tera Type:").grid(row = 3, column = 0, sticky = "e")
        types = ["Dragon", "Grass", "Bug", "Fire", "Water", "Ice", "Electric", "Psychic", "Ghost", "Poison", "Fairy", "Dark", "Steel", "Rock", "Fighting", "Ground", "Normal", "Flying"]
        types.sort()
        fours = [4* i for i in range(0, 64)]
        tera_value = tk.StringVar(newWindow)
        tera = tk.OptionMenu(newWindow,tera_value,*types)
        tera.grid(row =3, column = 1, columnspan = 6, sticky = "w")

        tk.Label(newWindow, text = "HP:").grid(row = 4, column = 1)
        tk.Label(newWindow, text = "ATK:").grid(row = 4, column = 2)
        tk.Label(newWindow, text = "DEF:").grid(row = 4, column = 3)
        tk.Label(newWindow, text = "SPA:").grid(row = 4, column = 4)
        tk.Label(newWindow, text = "SPD:").grid(row = 4, column = 5)
        tk.Label(newWindow, text = "SPE:").grid(row = 4, column = 6)

        tk.Label(newWindow, text = "EVs:").grid(row = 5, column = 0, sticky = "e")
        hpev_value = tk.StringVar(newWindow)
        hpev_value.set("0")
        hpev = ttk.Spinbox(newWindow, width = 4, from_=0, to=252, values = fours, textvariable= hpev_value, wrap = False)
        hpev.grid(row = 5, column = 1)
        atkev_value = tk.StringVar(newWindow)
        atkev_value.set("0")
        atkev = ttk.Spinbox(newWindow,width = 4, from_=0, to=252, values = fours, textvariable= atkev_value, wrap = False)
        atkev.grid(row = 5, column = 2)
        defev_value = tk.StringVar(newWindow)
        defev_value.set("0")
        defev = ttk.Spinbox(newWindow,width = 4, from_=0, to=252,  values = fours,textvariable= defev_value, wrap = False)
        defev.grid(row = 5, column = 3)
        spaev_value = tk.StringVar(newWindow)
        spaev_value.set("0")
        spaev = ttk.Spinbox(newWindow,width = 4, from_=0, to=252, values = fours, textvariable= spaev_value, wrap = False)
        spaev.grid(row = 5, column = 4)
        spdev_value = tk.StringVar(newWindow)
        spdev_value.set("0")
        spdev = ttk.Spinbox(newWindow,width = 4, from_=0, to=252, values = fours, textvariable= spdev_value, wrap = False)
        spdev.grid(row = 5, column = 5)
        speev_value = tk.StringVar(newWindow)
        speev_value.set("0")
        speev = ttk.Spinbox(newWindow,width = 4, from_=0, to=252, values = fours, textvariable= speev_value, wrap = False)
        speev.grid(row = 5, column = 6)

        tk.Label(newWindow, text = "IVs:").grid(row = 6, column = 0, sticky = "e")
        hpiv_value = tk.StringVar(newWindow)
        hpiv_value.set("31")
        hpiv = ttk.Spinbox(newWindow,width = 4, from_=0, to=31, textvariable= hpiv_value, wrap = True)
        hpiv.grid(row = 6, column = 1)
        atkiv_value = tk.StringVar(newWindow, value = 31)
        atkiv = ttk.Spinbox(newWindow,width = 4, from_=0, to=31, textvariable= atkiv_value, wrap = True)
        atkiv.grid(row = 6, column = 2)
        defiv_value = tk.StringVar(newWindow)
        defiv_value.set("31")
        defiv = ttk.Spinbox(newWindow,width = 4, from_=0, to=31, textvariable= defiv_value, wrap = True)
        defiv.grid(row = 6, column = 3)
        spaiv_value = tk.StringVar(newWindow)
        spaiv_value.set("31")
        spaiv = ttk.Spinbox(newWindow,width = 4, from_=0, to=31, textvariable= spaiv_value, wrap =True)
        spaiv.grid(row = 6, column = 4)
        spdiv_value = tk.StringVar(newWindow)
        spdiv_value.set("31")
        spdiv = ttk.Spinbox(newWindow,width = 4, from_=0, to=31, textvariable= spdiv_value, wrap = True)
        spdiv.grid(row = 6, column = 5)
        speiv_value = tk.StringVar(newWindow)
        speiv_value.set("31")
        speiv = ttk.Spinbox(newWindow,width = 4, from_=0, to=31, textvariable= speiv_value, wrap = True)
        speiv.grid(row = 6, column = 6)

        tk.Label(newWindow, text = "Nature:").grid(row = 7, column = 0, sticky = "e")
        nature = tk.Entry(newWindow)
        nature.grid(row =7, column = 1 ,columnspan=6, sticky = "ew", padx = 2)

        tk.Label(newWindow, text = "Moves:").grid(row = 8, column = 0, sticky = "e")
        move1 = tk.Entry(newWindow)
        move1.grid(row =8, column = 1 ,columnspan=2, sticky = "ew", padx = 2)
        move2 = tk.Entry(newWindow)
        move2.grid(row =8, column = 3, columnspan=2, sticky = "ew", padx = 2)
        move3 = tk.Entry(newWindow)
        move3.grid(row =8, column = 5,columnspan=2, sticky = "ew", padx = 2)
        move4 = tk.Entry(newWindow)
        move4.grid(row =8, column = 7,columnspan=2,  sticky = "ew", padx = 2)


        ivs =[hpiv_value,atkiv_value,defiv_value,spaiv_value,spdiv_value, speiv_value]
        evs =[hpev_value,atkev_value,defev_value,spaev_value,spdev_value, speev_value]
        moves =[move1, move2,move3,move4]
        text = tk.Text(newWindow)
        text.grid(row = 11, column = 0, columnspan = 10, sticky ="ew", padx= 5, pady=5)
        tk.Button(newWindow, text = "Generate", command= lambda: self.generatePaste(text,
                                                                                    pokemon.get(),
                                                                                    nature,
                                                                                    tera_value,
                                                                                    ivs,
                                                                                    evs,
                                                                                    item_value.get(),
                                                                                    moves,
                                                                                    ability
                                                                                    )).grid(row = 9, column = 0, columnspan = 8)

    def uxFileMenu(self, root):
        """
        Generate the file menu at the top of the application.

        Parameters
        ----------
        root : TK
            TKinter object to add file menu to.

        Returns
        -------
        None.

        """
        self._menuBar = tk.Menu(root)

        # Create file meny bar
        self._fileMenu = tk.Menu(self._menuBar, tearoff=0)
        self._fileMenu.add_command(label="New Team Log", command=self.uxNewFile)
        self._fileMenu.add_command(label="Open Team Log", command=self.uxOpenFile)
        self._fileMenu.add_command(label="Save Team Log", command=self.uxSaveFile)
        self._fileMenu.add_separator()
        self._fileMenu.add_command(label="Exit", command=root.destroy)
        self._menuBar.add_cascade(label="File", menu=self._fileMenu)

        #Create Pokepaste menu bar
        self._fileMenu = tk.Menu(self._menuBar, tearoff=0)
        self._fileMenu.add_command(label="Generate PokePaste", command=self.uxGeneratePokepaste)
        self._fileMenu.add_separator()
        self._fileMenu.add_command(label="Export Teams", command=self.uxExportTeams)
        self._fileMenu.add_command(label="Export Opponent's Teams", command=self.uxExportOpponentsTeams)
        self._menuBar.add_cascade(label="PokePaste", menu=self._fileMenu)

        # Initializes help menu bar
        self._helpMenu = tk.Menu(self._menuBar, tearoff=0)
        self._helpMenu.add_command(label="README", command=self.uxReadMe)
        self._helpMenu.add_command(label="GitHub", command=self.uxGithub)
        self._menuBar.add_cascade(label="Help", menu=self._helpMenu)
        root.config(menu=self._menuBar)

    def uxAddTeam(self):
        """
        Event handler for the addteam button.

        Returns
        -------
        None.

        """
        # Creates new popup window
        newWindow = tk.Toplevel(self._ux)
        newWindow.title("Add Team")
        newWindow.lift()
        newWindow.attributes('-topmost',True)
        newWindow.after_idle(newWindow.attributes,'-topmost',False)
        newWindow.geometry("500x450")

        # Adds team name entry
        tk.Label(newWindow, text ="Team Name:").pack()
        TeamName = tk.Entry(newWindow, width = 20)
        TeamName.insert(0, "Team "+ str(len(self._TeamName)+1))
        TeamName.pack()

        # Adds a textbox for sumbitting a pokepaste
        frame = tk.Frame(newWindow)
        frame.pack()
        PokePaste = tk.Text(frame, width = 50, height = 20)
        PokePaste.pack(side = 'left',fill = 'y' )

        # Adds scrollbar functionality
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        PokePaste.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = PokePaste.yview)

        # Adds a button to add team
        addTeam_button = tk.Button(newWindow, text='Add Team', command = lambda:self.addTeam(PokePaste, newWindow, TeamName.get()))
        addTeam_button.pack()

    def addTeam(self, box, window, teamName):
        """
        Add Helper Function for uxAddTeam to update gui after adding team.

        Parameters
        ----------
        box : tkinter.Text
            Text box to draw team paste from.
        window : tk.Frame
            New window popup for team to be placed.
        teamName : string
            Team name entered.

        Returns
        -------
        None.

        """
        if(teamName == ""):
            tk.messagebox.showerror('No Team Name', 'Error: Your team must have a name.')
            window.lift()
            return
        if(box.get("1.0",tk.END).lstrip().rstrip() == ""):
            tk.messagebox.showerror('No Team', 'Error: No team was entered.')
            window.lift()
            return
        dupeName = False
        for name in self._TeamName:
            if(teamName == name):
                dupeName = True
        if(dupeName == True):
            tk.messagebox.showerror('Duplicate Team Name', 'Error: You already have a team with that name. Please select another name.')
            window.lift()
            return
        else:
            try:
                # Writes team to file and parses, then deletes file contents
                FileName = 'temp_files/temp_team.txt'
                pasteFile = open(FileName, 'w')
                pasteFile.write(box.get("1.0",tk.END))
                pasteFile.close()
                parser = Parser.Parser()
                newPaste = parser.parse(FileName)
                pasteFile = open(FileName, 'w')
                pasteFile.write("")
                pasteFile.close()

                # Updates local variables and kills the new window
                self._Team.append(newPaste)
                self._TeamName.append(teamName)
                self.updateListbox(self._teamSelect, self._TeamName)
                self.displayPokePaste(self._pasteFrame, self._Team[-1])
                self._deleteTeamButton.config(state =tk.NORMAL)
                self._newMatchButton.config(state =tk.NORMAL)
                self._IsSaved = False
                window.destroy()
            except Exception as e:
                tk.messagebox.showerror('PokePaste Error', 'Error: There is an error with your paste. \nError Code: ' + str(e))
                window.lift()

    def uxDeleteTeam(self):
        """
        Event handler for Delete Team button.

        Returns
        -------
        None.

        """
        # Creates New popup window
        newWindow = tk.Toplevel(self._ux)
        newWindow.title("Delete Team")
        newWindow.lift()
        newWindow.attributes('-topmost', True)
        newWindow.after_idle(newWindow.attributes,'-topmost',False)
        newWindow.geometry("300x300")

        # Adds listbox to select team
        frame = tk.Frame(newWindow)
        frame.pack()
        tk.Label(newWindow, text ="Select team to delete:").pack()
        teamToDelete = tk.Listbox(frame)
        teamToDelete.pack(side = 'left',fill = 'y' )
        self.updateListbox(teamToDelete, self._TeamName)

        # Adds scrollbar to listbox
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        teamToDelete.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = teamToDelete.yview)

        # Adds delete team button
        deleteTeamButton = tk.Button(newWindow, text='Delete Team', command = lambda:self.deleteTeam(newWindow, teamToDelete.get(teamToDelete.curselection())))
        deleteTeamButton.pack()

    def deleteTeam(self, window, name):
        """
        Delete Helper Method for uxDeleteTeam.

        Parameters
        ----------
        window : tkinter.frame
            Frame to retriev selected team.
        name : string
            Name of team to delete.

        Returns
        -------
        None.

        """
        if(self._TeamName == []):
            tk.messagebox.showerror('Delete Team Error', 'Error: There is no team to delete.')
            window.lift()
        else:
            try:
                delInd = self._TeamName.index(name)
                self._TeamName.remove(name)
                self._Team.remove(self._Team[delInd])
                self.updateListbox(self._teamSelect, self._TeamName)
                if(self._TeamName == []):
                    self._deleteTeamButton.config(state =tk.DISABLED)
                self._IsSaved = False
                window.destroy()
            except Exception as e:
                tk.messagebox.showerror('Delete Team Error', 'Error: There was an error deleting your team. \nError Code: ' + str(e))
                window.lift()

    def checkTeam(self, event):
        """
        Check selected team and display its Pokepaste.

        Parameters
        ----------
        team : string
            Name of team to display.

        Returns
        -------
        None.

        """
        teamNo = self._TeamName.index(event.widget.get(event.widget.curselection()))
        team = self._Team[teamNo]
        if(teamNo != self.curTeam):
            self.displayPokePaste(self._pasteFrame, team)
            self.curTeam = teamNo

    def uxNewMatch(self):
        """
        Event handler for "New Match" button.

        Returns
        -------
        None.

        """
        # Creates New popup window
        newWindow = tk.Toplevel(self._ux)
        newWindow.title("New Match")
        newWindow.lift()
        newWindow.attributes('-topmost', True)
        newWindow.after_idle(newWindow.attributes,'-topmost',False)
        newWindow.geometry("1000x600")
        newWindow.columnconfigure(0, weight = 2)
        newWindow.columnconfigure(1, weight = 2)
        newWindow.rowconfigure(0, weight = 2)
        newWindow.rowconfigure(1, weight = 2)
        newWindow.rowconfigure(2, weight = 2)
        newWindow.rowconfigure(3, weight = 2)
        newWindow.rowconfigure(4, weight = 2)

        ## Adds listbox to select team
        teamFrame = tk.Frame(newWindow)
        teamFrame.grid(row = 2, column = 0)
        tk.Label(teamFrame, text ="Team Used:").pack()
        teamBox = tk.Listbox(teamFrame)
        teamBox.pack(side = 'left',fill = 'y' )
        self.updateListbox(teamBox, self._TeamName)
        # Adds scrollbar to listbox
        scrollbar = tk.Scrollbar(teamFrame)
        scrollbar.pack(side="right", fill="y")
        teamBox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = teamBox.yview)

        ## Adds frame to input leads and back
        leadsFrame = tk.Frame(newWindow)
        leadsFrame.grid(row = 1, column = 0)
        tk.Label(leadsFrame, text = "Your Lead:").pack()
        yourLead1 = tk.Entry(leadsFrame, width = 20)
        yourLead2 = tk.Entry(leadsFrame, width = 20)
        yourLead1.pack()
        yourLead2.pack()
        tk.Label(leadsFrame, text = "Your Back:").pack()
        yourBack1 = tk.Entry(leadsFrame, width = 20)
        yourBack2 = tk.Entry(leadsFrame, width = 20)
        yourBack1.pack()
        yourBack2.pack()

        tk.Label(leadsFrame, text = "Opponent's Lead:").pack()
        oppLead1 = tk.Entry(leadsFrame, width = 20)
        oppLead2 = tk.Entry(leadsFrame, width = 20)
        oppLead1.pack()
        oppLead2.pack()
        tk.Label(leadsFrame, text = "Opponent's Back:").pack()
        oppBack1 = tk.Entry(leadsFrame, width = 20)
        oppBack2 = tk.Entry(leadsFrame, width = 20)
        oppBack1.pack()
        oppBack2.pack()

        leads = [yourLead1, yourLead2, yourBack1, yourBack2, oppLead1, oppLead2, oppBack1, oppBack2]

        ## Adds textbox to select opponents team
        oppTeamFrame = tk.Frame(newWindow)
        oppTeamFrame.grid(row = 0, column = 1, rowspan = 2)
        tk.Label(oppTeamFrame, text ="Opponents Team:").pack()
        PokePaste = tk.Text(oppTeamFrame)
        PokePaste.pack(side = 'left',fill = 'y' )
        # Adds scrollbar functionality
        scrollbar = tk.Scrollbar(oppTeamFrame)
        scrollbar.pack(side="right", fill="y")
        PokePaste.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = PokePaste.yview)

        ## Adds textbox to add Notes
        notesFrame = tk.Frame(newWindow)
        notesFrame.grid(row = 1, column = 1, rowspan = 2)
        tk.Label(notesFrame, text ="Notes:").pack()

        notes = tk.Text(notesFrame)
        notes.pack(side = 'left',fill = 'y' )

        # Adds scrollbar functionality
        scrollbar = tk.Scrollbar(notesFrame)
        scrollbar.pack(side="right", fill="y")
        notes.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = notes.yview)

        # Adds box to input match name
        nameFrame = tk.Frame(newWindow)
        nameFrame.grid(row = 0, column =0)
        tk.Label(nameFrame, text ="Match Name:").pack()
        MatchName = tk.Entry(nameFrame, width = 20)
        MatchName.insert(0, "Match "+str(len(self._MatchLog)+1))
        MatchName.pack(side = 'left',fill = 'y' )

        # Adds a button to add match
        buttonFrame = tk.Frame(newWindow)
        buttonFrame.grid(row = 5, column = 1)
        addTeam_button = tk.Button(buttonFrame, text='Add Match', command = lambda : self.newMatch(newWindow, teamBox, PokePaste, notes, MatchName, leads))
        addTeam_button.pack(fill = "y")

    def newMatch(self, window, teamSelect, oppTeamBox, notesBox, nameBox, leadsList):
        """
        Add Match helper method.

        Parameters
        ----------
        window : window
            Pop-up window to get information from.
        teamSelect : listbox
            Listbox to get selected team from.
        oppTeamBox : text
            Textbox to retrieve opponents team.
        notesBox : text
            Textbox to retrieve notes.
        nameBox : entry
            Entry to get entered match name.
        leadsList : list of entry objects
            List of entries to retrieve leads and backs from.

        Returns
        -------
        None.

        """
        matchGood = True
        name = nameBox.get()
        if(name == "" or name == None):
            matchGood = False
            tk.messagebox.showerror('No Match Name', 'Your match must have a name.')
            window.lift()
            return
        dupeName = False
        for matchName in self._MatchName:
            if(matchName == name):
                dupeName = True
        if(dupeName == True):
            matchGood = False
            window.lift()
            tk.messagebox.showerror('Duplicate Match Name', 'You already have a match with that name. Please select another name.')
            window.lift()
            return
        teamUsed = teamSelect.curselection()
        if(teamUsed == "" or teamUsed == []):
            matchGood = False
            window.lift()
            tk.messagebox.showerror('No Team', 'You must select a team used.')
            window.lift()
            return
        teamName = teamSelect.get(teamUsed)
        team = self._Team[self._TeamName.index(teamName)]
        if(oppTeamBox.get("1.0",tk.END).lstrip().rstrip() == "" or oppTeamBox.get("1.0",tk.END) == None):
            matchGood = False
            window.lift()
            tk.messagebox.showerror('No Opposing Team', 'You must enter the opposing team.')
            window.lift()
            return
        if(matchGood == True):
            try:
                # Parses given opponents team
                FileName = 'temp_files/temp_team.txt'
                pasteFile = open(FileName, 'w')
                pasteFile.write(oppTeamBox.get("1.0",tk.END))
                pasteFile.close()
                parser = Parser.Parser()
                oppTeam = parser.parse(FileName)
                pasteFile = open(FileName, 'w')
                pasteFile.write("")
                pasteFile.close()
                notes = notesBox.get("1.0",tk.END)
                leads = Leads.Leads([None, None],[None, None],[None, None],[None, None])
                leads.yourLead[0] = leadsList[0].get().lstrip().rstrip()
                leads.yourLead[1] = leadsList[1].get().lstrip().rstrip()
                leads.yourBack[0] = leadsList[2].get().lstrip().rstrip()
                leads.yourBack[1] = leadsList[3].get().lstrip().rstrip()
                leads.oppLead[0] = leadsList[4].get().lstrip().rstrip()
                leads.oppLead[1] =leadsList[5].get().lstrip().rstrip()
                leads.oppBack[0] =leadsList[6].get().lstrip().rstrip()
                leads.oppBack[1] =leadsList[7].get().lstrip().rstrip()
                match = Match.Match(name, teamName, team, oppTeam, notes, leads)
                self._MatchLog.append(match)
                self._MatchName.append(match.name)
                self.displayMatch(self._matchFrame, match)
                self.updateListbox(self._matchSelect, self._MatchName)
                self._deleteMatchButton.config(state =tk.NORMAL)
                self._IsSaved = False
                window.destroy()
            except Exception as e:
                tk.messagebox.showerror('New Match Error', 'There was an error adding your match. \nError Code: ' + str(e))
                window.lift()

    def uxDeleteMatch(self):
        """
        Event handler for "Delete Match" button.

        Returns
        -------
        None.

        """
        # Creates New popup window
        newWindow = tk.Toplevel(self._ux)
        newWindow.title("Delete Match")
        newWindow.lift()
        newWindow.attributes('-topmost', True)
        newWindow.after_idle(newWindow.attributes,'-topmost',False)
        newWindow.geometry("300x300")

        # Adds listbox to select team
        frame = tk.Frame(newWindow)
        frame.pack()
        tk.Label(newWindow, text ="Select match to delete:").pack(side = "top")
        matchToDelete = tk.Listbox(frame)
        matchToDelete.pack(side = 'left',fill = 'y' )
        self.updateListbox(matchToDelete, self._MatchName)

        # Adds scrollbar to listbox
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        matchToDelete.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = matchToDelete.yview)

        # Adds delete team button
        deleteMatchButton = tk.Button(newWindow, text='Delete Match', command = lambda:self.deleteMatch(newWindow, matchToDelete.get(matchToDelete.curselection())))
        deleteMatchButton.pack()

    def deleteMatch(self, window, name):
        """
        Delete Match helper method.

        Parameters
        ----------
        window : window
            Pop-up window to get information from.
        name : strimg
            Name of match to delete.

        Returns
        -------
        None.

        """
        if(self._MatchName == []):
            tk.messagebox.showerror('No Match', 'There is no match to delete.')
            window.lift()
        else:
            try:
                delInd = self._MatchName.index(name)
                self._MatchName.remove(name)
                self._MatchLog.remove(self._MatchLog[delInd])
                self.updateListbox(self._matchSelect, self._MatchName)
                if(self._MatchName == []):
                    self._deleteMatchButton.config(state =tk.DISABLED)
                self._IsSaved = False
                window.destroy()
            except Exception as e:
                tk.messagebox.showerror('Delete Match Error', 'Error: There was an error deleting your match. \nError Code: ' + str(e))
                window.lift()
        return

    def displayMatch(self, frame, match):
        """
        Display a given match in the given frame.

        Parameters
        ----------
        frame : frame
            Frame to display match.
        match : Match
            Match to display.

        Returns
        -------
        None.
        """
        frame.update()
        #Clears frame
        for widget in frame.winfo_children():
            widget.destroy()
        frame.columnconfigure(0, weight = 1)
        frame.columnconfigure(1, weight = 1)
        frame.rowconfigure(1, weight = 1)
        frame.rowconfigure(2, weight = 1)
        frame.rowconfigure(3, weight = 12)
        frame.rowconfigure(4, weight = 4)

        #tk.Label(frame, text = "Matches").grid(column = 0, row = 0)

        teamUsedFrame = tk.Frame(frame, padx = 1, pady = 1)
        teamUsedFrame.columnconfigure(0, weight = 1)
        teamUsedFrame.columnconfigure(1, weight = 1)
        tk.Label(teamUsedFrame, text = "Team Used: ", font = 'Helvetica 9 bold').grid(row =0, column = 0, sticky = "w")
        tk.Label(teamUsedFrame, text = match.teamName).grid(row = 0, column = 1, sticky = "w")
        teamUsedFrame.grid(column = 0, row = 1, sticky = "w")

        ## Adds Leads
        leadsFrame = tk.Frame(frame, padx = 1, pady =1)
        leadsFrame.columnconfigure(0, weight =1)
        leadsFrame.columnconfigure(1, weight =1)
        leadsFrame.columnconfigure(2, weight =1)
        leadsFrame.columnconfigure(3, weight =1)
        leadsFrame.rowconfigure(0, weight =1)
        leadsFrame.rowconfigure(1, weight =1)
        tk.Label(leadsFrame, text = "Your Leads:", font = 'Helvetica 9 bold').grid(column = 0, row = 0, sticky = "n")
        tk.Label(leadsFrame, text = "Opponent's Leads:", font = 'Helvetica 9 bold').grid(column = 0, row = 1, sticky = "n")
        tk.Label(leadsFrame, text = "Your Back:", font = 'Helvetica 9 bold').grid(column = 2, row = 0, sticky = "n")
        tk.Label(leadsFrame, text = "Opponent's Back:", font = 'Helvetica 9 bold').grid(column = 2, row = 1, sticky = "n")
        yourLeadsFrame = tk.Frame(leadsFrame)
        yourLeadsFrame.grid(column = 1, row = 0)
        tk.Label(yourLeadsFrame, text = match.leads.yourLead[0]).pack()
        tk.Label(yourLeadsFrame, text = match.leads.yourLead[1]).pack()
        yourBackFrame = tk.Frame(leadsFrame)
        yourBackFrame.grid(column = 3, row = 0)
        tk.Label(yourBackFrame, text = match.leads.yourBack[0]).pack()
        tk.Label(yourBackFrame, text = match.leads.yourBack[1]).pack()
        oppLeadsFrame = tk.Frame(leadsFrame)
        oppLeadsFrame.grid(column = 1, row = 1)
        tk.Label(oppLeadsFrame, text = match.leads.oppLead[0]).pack()
        tk.Label(oppLeadsFrame, text = match.leads.oppLead[1]).pack()
        oppBackFrame = tk.Frame(leadsFrame)
        oppBackFrame.grid(column = 3, row = 1)
        tk.Label(oppBackFrame, text = match.leads.oppBack[0]).pack()
        tk.Label(oppBackFrame, text = match.leads.oppBack[1]).pack()

        leadsFrame.grid(column = 1, row = 1)

        tk.Label(frame, text = "Opponent's Team:", font = 'Helvetica 9 bold').grid(column = 0, row = 2, sticky = "w")

        oppTeamFrame = tk.Frame(frame)
        self.displayPokePaste(oppTeamFrame, match.oppTeam)
        oppTeamFrame.grid(column = 0, row = 3, columnspan = 2)

        notesFrame = tk.Frame(frame, pady=5, padx = 5)
        notesFrame.grid(column = 0, row = 4, columnspan = 2)

        notesFrame.rowconfigure(0, weight = 1)
        notesFrame.rowconfigure(1, weight = 4)
        notesFrame.update()
        notesFrame.columnconfigure(0, weight = 1)
        notesFrame.columnconfigure(1, weight = 1)

        tk.Label(notesFrame, text = "Notes:", font = 'Helvetica 9 bold').grid(row = 0, column = 0, sticky = "w")

        scrollbar = tk.Scrollbar(notesFrame)
        scrollbar.grid(column =1, row = 1, sticky = "nsew")
        notes = tk.Text(notesFrame, height = 5, width = 55)
        notes.grid(row = 1, column = 0, sticky = "w")

        notes.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = notes.yview)

        notes.delete(1.0, tk.END)
        notes.insert(tk.END, match.notes)
        notes.config(state=tk.DISABLED)


    def checkMatch(self, event):
        """
        Event handler for selection of item in matchSelect listbox.

        Parameters
        ----------
        event : event
            Object to check when variable is changed.

        Returns
        -------
        None.

        """
        matchName = self._MatchName.index(event.widget.get(event.widget.curselection()))
        match = self._MatchLog[matchName]
        if(matchName != self.curMatch):
            self.displayMatch(self._matchFrame, match)
            self.curMatch = matchName

    def onClose(self, window):
        if(len(self._MatchName) != 0 and self._IsSaved == False):
            response = tk.messagebox.askyesnocancel("Save Progress", "Would you like to save your current match log?", icon ='question')
            if(response == True):
                self.uxSaveFile()
            elif(response == None):
                return
        window.destroy()

    def uxLayout(self, root):
        """
        Make the layout for the application.

        Parameters
        ----------
        root : tkinter.frame
            Frame to add window to.

        Returns
        -------
        None.

        """
        ## Configures column setup

        root.geometry("1400x680")
        #root.state('zoomed')
        root.title("VGC Match Log")
        root.update()
        root.protocol("WM_DELETE_WINDOW",lambda: self.onClose(root))
        root.columnconfigure(0, weight = 1, minsize = root.winfo_width()/2)
        root.columnconfigure(1, weight = 1, minsize = root.winfo_width()/2)
        root.rowconfigure(0, weight = 1, minsize = root.winfo_height())
        # separator = ttk.Separator(root, orient='vertical')
        # separator.place(relx=0.5, rely=0, relwidth=0.2, relheight=1)


        ## Configure Match section
        Team = tk.Frame(root)
        Team.update()
        Team.grid(row = 0, column = 0)
        Team.columnconfigure(0, weight = 2, minsize = root.winfo_width()/7)
        Team.columnconfigure(1, weight = 5, minsize = 5*root.winfo_width()/14)
        Team.rowconfigure(0, weight = 1, minsize = root.winfo_height()/8)
        Team.rowconfigure(1, weight = 1, minsize = root.winfo_height()/8)
        Team.rowconfigure(2, weight = 4, minsize = root.winfo_height()/2)
        Team.rowconfigure(3, weight = 1, minsize = root.winfo_height()/8)
        Team.rowconfigure(4, weight = 1, minsize = root.winfo_height()/8)

        # Listbox label
        tk.Label(Team, text='Teams', font = 'Helvetica 11 bold underline', anchor = "center").grid(column=0, row=0, columnspan = 2)
        # Configures a Listbox for selecting team
        TSoptions = self._TeamName
        TSframe = tk.Frame(Team, padx = 10, pady=5)
        tk.Label(TSframe, text='Current team:', font = 'Helvetica 9 bold').pack()
        TSframe.grid(column = 0, row = 2)
        self._teamSelect = tk.Listbox(TSframe)
        self._teamSelect.bind('<<ListboxSelect>>', self.checkTeam)
        self.updateListbox(self._teamSelect, TSoptions)
        self._teamSelect.pack(side = 'left',fill = 'y' )

        # Adds "Add Team" button
        self._addTeamButton = tk.Button(Team, text='Add Team', command = self.uxAddTeam)
        self._addTeamButton.grid(column = 0, row = 3)

        # Adds "Delete Team" button
        self._deleteTeamButton = tk.Button(Team, text='Delete Team', command = self.uxDeleteTeam)
        self._deleteTeamButton.grid(column = 0, row = 4)
        self._deleteTeamButton.config(state =tk. DISABLED)

        # Adds scrollbar functionality
        scrollbar = tk.Scrollbar(TSframe)
        self._teamSelect.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = self._teamSelect.yview)
        scrollbar.pack(side="right", fill="y")

        # Sets Frame to put Pokepaste
        self._pasteFrame = tk.Frame(Team)
        self._pasteFrame.grid(column=1, row =1, rowspan = 4)

        ## Configure Match section
        Match = tk.Frame(root)
        Match.grid(row = 0, column = 1)
        Match.columnconfigure(0, weight = 5, minsize = 5*root.winfo_width()/14)
        Match.columnconfigure(1, weight = 2, minsize = root.winfo_width()/7)
        Match.rowconfigure(0, weight = 1, minsize = root.winfo_height()/8)
        Match.rowconfigure(1, weight = 1, minsize = root.winfo_height()/8)
        Match.rowconfigure(2, weight = 4, minsize = root.winfo_height()/2)
        Match.rowconfigure(3, weight = 1, minsize = root.winfo_height()/8)
        Match.rowconfigure(4, weight = 1, minsize = root.winfo_height()/8)

        # Configures a Listbox for selecting match
        tk.Label(Match, text='Matches', font = 'Helvetica 11 bold underline', anchor = "center").grid(column=0, row=0, columnspan = 2, sticky = tk.NS)
        MSoptions = self._MatchLog
        MSframe = tk.Frame(Match, padx = 10, pady=5)
        MSframe.grid(column = 1, row = 2)
        tk.Label(MSframe, text='Current Match:', font = 'Helvetica 9 bold').pack()
        self._matchSelect = tk.Listbox(MSframe)
        self._matchSelect.bind('<<ListboxSelect>>', self.checkMatch)
        self.updateListbox(self._matchSelect, MSoptions)
        self._matchSelect.pack(side = 'right',fill = 'y' )

        # Adds scrollbar functionality
        MSscrollbar = tk.Scrollbar(MSframe)
        self._matchSelect.config(yscrollcommand = MSscrollbar.set)
        MSscrollbar.config(command = self._matchSelect.yview)
        MSscrollbar.pack(side="left", fill="y")

        # Adds frame to put match data
        self._matchFrame = tk.Frame(Match)
        self._matchFrame.grid(column=0, row = 1, rowspan = 4)

        # Adds "New Match" button
        self._newMatchButton = tk.Button(Match, text='New Match', command = self.uxNewMatch)
        self._newMatchButton.grid(column=1, row=3)
        self._newMatchButton.config(state =tk.DISABLED)

        # Adds "Delete Match" button
        self._deleteMatchButton = tk.Button(Match, text='Delete Match', command = self.uxDeleteMatch)
        self._deleteMatchButton.grid(column = 1, row = 4)
        self._deleteMatchButton.config(state =tk.DISABLED)

    def updateOptionMenu(self, optionMenu, options):
            """
            Update a the options in a given OptionMenu.

            Parameters
            ----------
            optionMenu : tkinter.OptionMenu
                OptionMenu to add options to.
            options : list
                List of options to add to the menu.

            Returns
            -------
            None.

            """
            menu = optionMenu["menu"]
            menu.delete(0, "end")
            for string in options:
                menu.add_command(label=string, command=lambda value=string: tk.StringVar().set(value))

    def updateLabel(self, label, labelText):
        """
        Update text of a label.

        Parameters
        ----------
        label : tkinter.label
            Label to update text.
        labelText : string
            Text to change label to.

        Returns
        -------
        None.

        """
        label.config(text = labelText)

    def updateListbox(self, listBox, options):
        """
        Update options in Listbox.

        Parameters
        ----------
        listBox : tkinter.Listbox
            Listbox to update options.
        options : list
            List of options to add in listbox.

        Returns
        -------
        None.

        """
        listBox.delete(0, tk.END)
        for i in range(len(options)):
            listBox.insert(i, options[i])
        listBox.select_set("end")

    def displayPokePaste(self, frame, team):
        """
        Update a frame with the pokepaste of a given team.

        Parameters
        ----------
        frame : tkinter.frame
            Frame to display.
        team : Team.Team
            Team to add to display.

        Returns
        -------
        None.

        """
        for widget in frame.winfo_children():
            widget.destroy()
        frame.columnconfigure(0, weight = 1)
        frame.columnconfigure(1, weight = 1)
        frame.rowconfigure(0, weight = 1)
        frame.rowconfigure(1, weight = 1)
        frame.rowconfigure(2, weight = 1)
        col_count, row_count = frame.grid_size()
        for col in range(col_count):
            frame.grid_columnconfigure(col, minsize=50)
        for row in range(row_count):
            frame.grid_rowconfigure(row, minsize=50)
        for i in range(6):
            pokeframe = tk.Frame(frame)
            pokeframe.rowconfigure(0, weight = 1)
            pokeframe.rowconfigure(1, weight = 1)
            pokeframe.rowconfigure(2, weight = 1)
            pokeframe.columnconfigure(0, weight = 1)
            pokeframe.columnconfigure(1, weight = 4)
            col = i % 2
            row = math.floor(i/2)
            if(i < len(team.pokemon)):
                poke = tk.Label(pokeframe, text = str(team.pokemon[i]), anchor = "w", justify = "left")
                from pathlib import Path
                from PIL import Image, ImageTk
                #add sprite image
                spritePath = "sprites/" +str(team.pokemon[i].name).replace(" ", "-")+ ".png"
                my_file = Path(spritePath)
                if my_file.is_file():
                    pic = Image.open(spritePath)
                    resize = pic.resize((60, 60),Image.LANCZOS)
                    img = ImageTk.PhotoImage(resize)
                    imageLab = tk.Label(pokeframe, image = img)
                    imageLab.image = img
                else:
                    imageLab = tk.Label(pokeframe, text = "[No Image]")
                imageLab.grid(row = 0, column = 0, sticky = tk.E)

                #add item image
                itemPath = "items/" +str(team.pokemon[i].item).replace(" ", "-")+ ".png"
                my_file = Path(itemPath)
                if my_file.is_file():
                    pic = Image.open(itemPath)
                    resize = pic.resize((20, 20),Image.LANCZOS)
                    imgItem = ImageTk.PhotoImage(resize)
                    itemLab = tk.Label(pokeframe, image = imgItem)
                    itemLab.image = imgItem
                else:
                    itemLab = tk.Label(pokeframe, text = "[No Image]")
                itemLab.grid(row = 2, column = 0)

                #add tera image
                teraPath = "tera_types/" +str(team.pokemon[i].tera)+ ".png"
                my_file = Path(teraPath)
                if my_file.is_file():
                    pic = Image.open(teraPath)
                    resize = pic.resize((60, 15),Image.LANCZOS)
                    imgTera = ImageTk.PhotoImage(resize)
                    teraLab = tk.Label(pokeframe, image = imgTera)
                    teraLab.image = imgTera
                else:
                    teraLab = tk.Label(pokeframe, text = "[No Image]")
                teraLab.grid(row = 1, column = 0, sticky = tk.E)

            else:
                poke = tk.Label(pokeframe, text = "", anchor = "w", justify = "left")
            poke.grid(row = 0, column = 1, sticky = tk.NW, rowspan = 3)
            pokeframe.grid(column = col, row = row, sticky = tk.NW)

    def uxInitialize(self, root):
        """
        Initialize the application.

        Parameters
        ----------
        root : tkinter.tk
            Interface to initialize.

        Returns
        -------
        None.

        """
        self.uxFileMenu(root)
        self.uxLayout(root)
        self._ux.mainloop()