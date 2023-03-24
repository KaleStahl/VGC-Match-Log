import Parser

paste = "Team_Test.txt"
parser = Parser.Parser()
team = parser.parse(paste)

print("CREATED TEAM:\n\n" + str(team))