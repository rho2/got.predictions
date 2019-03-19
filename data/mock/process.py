import json
import os

YEAR = 305  # start year of season 8
FILE = "chars/test.json"


def parseDate(dateString):
    l = []
    d = dateString.split()

    for i, a in enumerate(d):
        if not a.isdigit():
            continue
        if len(d) <= i + 1:
            return ""  # something is wrong with the date
        if "AC" in d[i+1]:
            l.append(int(a))
        else:
            l.append(-int(a))

    if not l:
        return ""

    return sum(l) / len(l)


with open(FILE, 'r') as f:
    j = json.load(f)

outfile = open("chars/processed.json", 'w')
print("[", file=outfile)

cc = 0
for c in j:
    nc = {"name": c["name"], "culture": c["culture"]}
    nc["isMale"] = c["gender"] == "Male"

    print(c["name"])

    nc["birth"] = ""
    nc["death"] = ""

    if c["born"]:
        nc["birth"] = parseDate(c["born"])
    if c["died"]:
        nc["death"] = parseDate(c["died"])

    if nc["birth"] and nc["death"]:
        nc["age"] = abs(nc["death"] - nc["birth"])
        cc += 1
    elif nc["birth"]:
        nc["age"] = abs(YEAR - nc["birth"])
        cc += 1
    else:
        nc["age"] = ""

    nc["alCount"] = len(c["allegiances"])
    nc["bookCount"] = len(c["books"])
    nc["povCount"] = len(c["povBooks"])

    json.dump(nc, outfile)
    print(",", file=outfile)


outfile.seek(outfile.tell() - 2, os.SEEK_SET)

print("]", file=outfile)
outfile.close()


print(len(j))
print(cc)
