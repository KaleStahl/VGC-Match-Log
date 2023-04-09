"""
User_Interface.py.

Class to manage interaction with user interface.

Author: Kale Stahl
Last Modified: 4/8/2023

"""
import tkinter as tk
import Parser
import Match
from tkinter.filedialog import asksaveasfile, askopenfilename
import math

class Application:
    """Class to create the application GUI."""

    _MatchLog = []
    _MatchName = []
    _Team = []
    _TeamName = []

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
        from os import startfile
        startfile("README.txt")

    def uxGithub(self):
        import webbrowser
        webbrowser.open_new("https://github.com/KaleStahl/VGC-Match-Log.git")

    def uxOpenFile(self):
        path = askopenfilename()
        matchHelp = Match.Match(None, None, None, None, None)
        self._MatchLog = matchHelp.readMatch(path)
        for match in self._MatchLog:
            self._MatchName.append(match.name)
            self._TeamName.append(match.teamName)
            self._Team.append(match.team)
        self.updateListbox(self._teamSelect, self._TeamName)
        self._teamSelect.select_set(0)
        self.updateListbox(self._matchSelect, self._MatchName)
        self._matchSelect.select_set(0)
        self._deleteMatchButton.config(state =tk.NORMAL)
        self._deleteTeamButton.config(state =tk.NORMAL)
        self._newMatchButton.config(state =tk.NORMAL)

    def uxSaveFile(self):
        file = asksaveasfile(title="Select Location", filetypes=(("Text Files", "*.txt"),))
        text2save = ""
        for match in self._MatchLog:
            text2save += str(match)
        file.write(text2save)
        file.close()

    def uxNewFile(self):
        self._MatchLog = []
        self._MatchName = []
        self._Team = []
        self._TeamName = []
        self.updateListbox(self._matchSelect, self._MatchName)
        self.updateListbox(self._teamSelect, self._TeamName)

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

        # Initializes help menu bar
        self._helpMenu = tk.Menu(self._menuBar, tearoff=0)
        self._helpMenu.add_command(label="ReadMe", command=self.uxReadMe)
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
        if(box.get("1.0",tk.END) == ""):
            tk.messagebox.showerror('No Team', 'Error: No team was entered.')
            window.lift()
        dupeName = False
        for name in self._TeamName:
            if(teamName == name):
                dupeName = True
        if(dupeName == True):
            tk.messagebox.showerror('Duplicate Team Name', 'Error: You already have a team with that name. Please select another name.')
            window.lift()
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
        #print(f"the variable has changed to '{team}'")
        self.displayPokePaste(self._pasteFrame, self._Team[self._TeamName.index(event.widget.get(event.widget.curselection()))])

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

        ## Adds listbox to select team
        teamFrame = tk.Frame(newWindow)
        teamFrame.grid(row = 0, column = 0)
        tk.Label(teamFrame, text ="Team Used:").pack()
        teamBox = tk.Listbox(teamFrame)
        teamBox.pack(side = 'left',fill = 'y' )
        self.updateListbox(teamBox, self._TeamName)
        # Adds scrollbar to listbox
        scrollbar = tk.Scrollbar(teamFrame)
        scrollbar.pack(side="right", fill="y")
        teamBox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = teamBox.yview)

        ## Adds textbox to select opponents team
        oppTeamFrame = tk.Frame(newWindow)
        oppTeamFrame.grid(row = 0, column = 1, rowspan = 1)
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
        nameFrame.grid(row = 1, column =0)
        tk.Label(nameFrame, text ="Match Name:").pack()
        MatchName = tk.Entry(nameFrame, width = 20)
        MatchName.insert(0, "Match "+str(len(self._MatchLog)+1))
        MatchName.pack(side = 'left',fill = 'y' )


        # Adds a button to add match
        buttonFrame = tk.Frame(newWindow)
        buttonFrame.grid(row = 4, column = 1)
        addTeam_button = tk.Button(buttonFrame, text='Add Match', command = lambda : self.newMatch(newWindow, teamBox, PokePaste, notes, MatchName))
        addTeam_button.pack(side = "bottom", fill = "y")

    def newMatch(self, window, teamSelect, oppTeamBox, notesBox, nameBox):
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

        Returns
        -------
        None.

        """
        matchGood = True
        name = nameBox.get()
        if(name == "" or name == None):
            matchGood = False
            tk.messagebox.showerror('Match Name Error', 'Error: Your match must have a name.')
            window.lift()
        dupeName = False
        for matchName in self._MatchName:
            if(matchName == name):
                dupeName = True
        if(dupeName == True):
            matchGood = False
            tk.messagebox.showerror('Duplicate Match Name', 'Error: You already have a match with that name. Please select another name.')
            window.lift()
        teamUsed = teamSelect.curselection()
        if(teamUsed == "" or teamUsed == []):
            matchGood = False
            tk.messagebox.showerror('No Team Error', 'Error: You must select a match.')
            window.lift()
        teamName = teamSelect.get(teamUsed)
        team = self._Team[self._TeamName.index(teamName)]
        if(oppTeamBox.get("1.0",tk.END) == "" or oppTeamBox.get("1.0",tk.END) == None):
            matchGood = False
            tk.messagebox.showerror('No Opposing Team Error', 'Error: You must enter the opposing team.')
            window.lift()
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
                match = Match.Match(name, teamName, team, oppTeam, notes)

                self._MatchLog.append(match)
                self._MatchName.append(match.name)
                self.displayMatch(self._matchFrame, match)
                self.updateListbox(self._matchSelect, self._MatchName)
                self._deleteMatchButton.config(state =tk.NORMAL)
                window.destroy()
            except Exception as e:
                tk.messagebox.showerror('New Match Error', 'Error: There was an error adding your match. \nError Code: ' + str(e))
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
            tk.messagebox.showerror('Delete Match Error', 'Error: There is no match to delete.')
            window.lift()
        else:
            try:
                delInd = self._MatchName.index(name)
                self._MatchName.remove(name)
                self._MatchLog.remove(self._MatchLog[delInd])
                self.updateListbox(self._matchSelect, self._MatchName)
                if(self._MatchName == []):
                    self._deleteMatchButton.config(state =tk.DISABLED)
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
        #Clears frame
        for widget in frame.winfo_children():
            widget.destroy()
        frame.columnconfigure(0, weight = 2)
        frame.columnconfigure(1, weight = 2)
        frame.rowconfigure(0, weight = 1)
        frame.rowconfigure(1, weight = 12)
        frame.rowconfigure(2, weight = 4)

        teamFrame = tk.Frame(frame)
        tk.Label(teamFrame, text = "Team Used: " + match.teamName).pack()

        oppTeamFrame = tk.Frame(frame)
        tk.Label(oppTeamFrame, text = "Opponent's Team:\n").pack()
        self.displayPokePaste(oppTeamFrame, match.oppTeam)

        notesFrame = tk.Frame(frame)
        tk.Label(notesFrame, text = "Notes:").pack()
        notes = tk.Text(notesFrame, height = 5, width = 50)
        notes.delete(1.0, tk.END)
        notes.insert(tk.END, match.notes)
        notes.config(state=tk.DISABLED)
        notes.pack()

        # changesFrame = tk.Frame(frame)
        # changeText ="Changes: \n" + match.getChanges(self._Team[0].pokemon)
        # tk.Label(changesFrame, text = changeText ).pack()

        teamFrame.grid(row = 0, column = 0)
        notesFrame.grid(row = 2, column = 0)
        oppTeamFrame.grid(row = 1, column = 0)
        # changesFrame.grid(row = 0, column = 1, rowspan = 3)

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
        self.displayMatch(self._matchFrame, self._MatchLog[self._MatchName.index(event.widget.get(event.widget.curselection()))])

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

        root.geometry("1360x680")
        root.title("VGC Team Logger")
        root.columnconfigure(0, weight = 1)
        root.columnconfigure(1, weight = 4)
        root.columnconfigure(2, weight = 4)
        root.columnconfigure(3, weight = 1)
        root.rowconfigure(0, weight = 1)
        root.rowconfigure(1, weight = 1)
        root.rowconfigure(2, weight = 10)
        root.grid_columnconfigure(1, minsize=100)
        root.grid_rowconfigure(2, minsize=100)
        root.grid_columnconfigure(2, minsize=100)
        root.rowconfigure(3, weight = 1)
        root.rowconfigure(4, weight = 1)

        ## Configure First column

        # Listbox label
        TSoptions = self._TeamName
        tk.Label(root, text='Current team:').grid(column=0, row=0, sticky = "S")

        # Configures a Listbox for selecting team
        TSframe = tk.Frame(root)
        TSframe.grid(column = 0, row = 1)
        self._teamSelect = tk.Listbox(TSframe)
        self._teamSelect.bind('<<ListboxSelect>>', self.checkTeam)
        self.updateListbox(self._teamSelect, TSoptions)
        self._teamSelect.pack(side = 'left',fill = 'y' )

        # Adds scrollbar functionality
        scrollbar = tk.Scrollbar(TSframe)
        self._teamSelect.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = self._teamSelect.yview)
        scrollbar.pack(side="right", fill="y")

        # Sets Frame to put Pokepaste
        self._pasteFrame = tk.Frame(root)
        self._pasteFrame.grid(column=1, row =0, rowspan = 5)

        # Adds "Add Team" button
        self._addTeamButton = tk.Button(root, text='Add Team', command = self.uxAddTeam)
        self._addTeamButton.grid(column = 0, row = 3)

        # Adds "Delete Team" button
        self._deleteTeamButton = tk.Button(root, text='Delete Team', command = self.uxDeleteTeam)
        self._deleteTeamButton.grid(column = 0, row = 4)
        self._deleteTeamButton.config(state =tk. DISABLED)

        ## Configure Second column

        # Configures a Listbox for selecting match
        MSoptions = self._MatchLog
        tk.Label(root, text='Current Match:').grid(column=3, row=0, sticky = "S")
        MSframe = tk.Frame(root)
        MSframe.grid(column = 3, row = 1)
        self._matchSelect = tk.Listbox(MSframe)
        self._matchSelect.bind('<<ListboxSelect>>', self.checkMatch)
        self.updateListbox(self._matchSelect, MSoptions)
        self._matchSelect.pack(side = 'left',fill = 'y' )

        # Adds scrollbar functionality
        MSscrollbar = tk.Scrollbar(MSframe)
        self._matchSelect.config(yscrollcommand = MSscrollbar.set)
        MSscrollbar.config(command = self._matchSelect.yview)
        MSscrollbar.pack(side="right", fill="y")

        # Adds frame to put match data
        self._matchFrame = tk.Frame(root)
        self._matchFrame.grid(column=2, row = 0, rowspan = 5)

        # Adds "New Match" button
        self._newMatchButton = tk.Button(root, text='New Match', command = self.uxNewMatch)
        self._newMatchButton.grid(column=3, row=3)
        self._newMatchButton.config(state =tk.DISABLED)

        # Adds "Delete Match" button
        self._deleteMatchButton = tk.Button(root, text='Delete Match', command = self.uxDeleteMatch)
        self._deleteMatchButton.grid(column = 3, row = 4)
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
            pokeframe.columnconfigure(0, weight = 1)
            pokeframe.columnconfigure(1, weight = 4)
            col = i % 2
            row = math.floor(i/2)
            if(i < len(team.pokemon)):
                poke = tk.Label(pokeframe, text = str(team.pokemon[i]),anchor = "w", justify = "left")
                from pathlib import Path
                from PIL import Image, ImageTk
                spritePath = "sprites/" +str(team.pokemon[i].name).replace(" ", "-")+ ".png"
                my_file = Path(spritePath)
                if my_file.is_file():
                    pic = Image.open(spritePath)
                    resize = pic.resize((50, 50),Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(resize)
                    imageLab = tk.Label(pokeframe, image = img, anchor = tk.CENTER)
                    imageLab.image = img
                else:
                    imageLab = tk.Label(pokeframe, text = "[No Image]", anchor = tk.CENTER)
                imageLab.grid(column = 0, sticky = tk.EW)
            else:
                poke = tk.Label(pokeframe, text = "", anchor = "NW", justify = "left")
            poke.grid(column = 1, sticky = tk.EW)
            #poke.pack(side = "left", fill="both", expand=True)
            pokeframe.grid(column = col, row = row, sticky = tk.NS)

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
        ux.mainloop()

ux = tk.Tk()
app = Application(ux)
app.uxInitialize(ux)