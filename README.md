
# VGC Team Logger
VGC Team Logger is a Python application for tracking matches and teams used in those matches in a clear and concise manner. These matches can be saved and loaded, and teams are copied from Showdown for ease of use.

## Installation
To install this program, download "VGC-Match-Log.zip" and extract it to the location of your choice. Once extracted, locate the "VGC-Match-log.exe" and run it. Be careful not to move the .exe file without first copying the folders "temp_files", "items", "sprites", and "tera_types" to the new location. The exe can run without all folders, but without "temp_files" it cannot open or save teams and without the other files it cannot display images.

## Usage

To use this program, simply execute the .exe file and the GUI will begin. Specific aspects of the GUI will be shown below:

### Menu Bar
#### File
##### New Match Log
Clears current team log and makes a new blank team log. This will delete all of your current teams and matches. If you have any open matches, it will first prompt to save.
##### Open Match Log
Opens a previously saved team log. This program can only open files created by this program. If you have any open matches, it will first prompt to save.
##### Save Match Log
Saves your current team log as a specially formatted .txt file.
This text file can be read by this application, but not Showdown.
##### Exit
Closes the application.

#### PokePaste
##### Generate PokePaste
Opens a window that allows you to enter Pokemon data. "Generate" button will generate a PokePaste readable by both this program and Showdown. Note that because I am bad at programming, once you hit generate, it will not allow you to generate another pokepaste without closing and restarting the generate pokepaste window.
##### Export Teams
Opens a window with a text paste of all teams entered through the "add team" button. This paste will be readable by Showdown, but not this application.
##### Export Opponent's Teams
Opens a window with a text paste of all opponent's teams entered through the "new match" button. This paste will be readable by Showdown, but not this application.
#### Help
##### README
Opens this "README.txt" document in your default application.
##### GitHub
Opens the url to the GitHub Repo for this project in your default browser.

### Direct Interface
#### Team Pane
The team pane holds all information about the teams you have used.
##### Team Select
Holds all currently stored teams. To display a team, click on its name in the listbox labeled "Current Team". If you click a team not currently displayed, it will automatically display its PokePaste with images to the right.
##### Add Team Button
Adds a new team to the listbox. Enter you team name in the box "Team Name", Note it must be different that previous team names. Then copy your Showdown paste into the box below and click "add". The team name will now appear in the listbox and you can display the team by clicking on the name.
##### Delete Team Button
Deletes a team from the listbox. After clicking the button, select the team you wish to delete and click "delete". That team will no longer appear in the listbox, though if it was currently displayed it will not go away until another team is selected.

#### Match Pane
The team pane holds all information about the matches you have entered.
##### Match Select
Holds all currently stored matches. To display a match, click on its name in the listbox labeled "Current Match". If you click a team not currently displayed, it will automatically display its PokePaste with images to the left, along with the name of the team used and any notes.
##### New Match Button
Adds a new match to the listbox. Enter the name of your match in the box "Match Name". Note it must be different that previous match names. Then select the team used in the match from the "Team Used" listbox to the right. You can enter the Opponents team PokePaste into the "Opponents Team" box and enter any notes into the "Notes" box. You can also enter the two pokemon you led wuth in "Your leads" your pokemon in the back in "Your Back" and the same for your opponent. Note that you must select a team used, the opponents team, and a match name. Notes and lead information are optional. The match name will now appear in the listbox and you can display the match by clicking on the name.
##### Delete Match Button
Deletes a match from the listbox. After clicking the button, select the match you wish to delete and click "delete". That match will no longer appear in the listbox, though if it was currently displayed it will not go away until another match is selected.

## Support

If you have any issues, check the GitHub repo for updates. If the problem is not fixed there,
please open an issue on the repo. If these issues are not fixed and you feel reaching out to me directly is the
best course of action, you can send an email to kalestahl[at]gmail.com.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change. If you have specific questions about my
code or would like to work with me directly, you can send an email to kalestahl[at]gmail.com.

## Credits
Original concept came from twitter user @NikyuAlex and their spreadsheet found here:
https://twitter.com/NikyuAlex/status/1630979632294920195

All Pokemon Sprite images from https://pokemondb.net/

All item images from Aby Zab's google drive:
https://drive.google.com/drive/folders/1rPpIzyWRidSKoAwQyWwiVg9hTyjU-8r3

All Tera-type images from previous spreadsheet.

## License

MIT License

Copyright (c) 2023 Kale Stahl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
