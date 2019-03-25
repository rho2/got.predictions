import json

writer = [('George R.R. Martin', 0), ('Bryan Cogman', 1), ('David Benioff', 2),
          ('Vanessa Taylor', 3), ('D.B. Weiss', 4), ('Jane Espenson', 5), ('Dave Hill', 6)]
episodes = [('Alex Graves', 0), ('Michelle MacLaren', 1), ('Jack Bender', 2), ('Tim Van Patten', 3), ('Daniel Minahan', 4), ('Mark Mylod', 5), ('David Benioff & D.B. Weiss', 6), ('Neil Marshall', 7), ('Brian Kirk', 8),
            ('Alan Taylor', 9), ('David Petrarca', 10), ('David Nutter', 11), ('Miguel Sapochnik', 12), ('Daniel Sackheim', 13), ('Jeremy Podeswa', 14), ('Michael Slovis', 15), ('Alik Sakharov', 16), ('Matt Shakman', 17)]


chars, episodes = None, None
with open("data/chars.json") as file:
    chars = json.load(file)

with open("data/episodes.json") as file:
    episodes = json.load(file)
