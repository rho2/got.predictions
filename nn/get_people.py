import json


def get_people():
    with open("../data/episodes.json", 'r') as file:
        episodes = json.load(file)["episodes"]

    writers = set()
    directors = set()
    for a in episodes:
        w = a["written_by"].split(",")
        d = a["directed_by"].split(",")

        for ww in w:
            writers.add(ww.strip())
        for dd in d:
            directors.add(dd.strip())

    wl = list(zip(writers, range(0, len(writers))))
    dl = list(zip(directors, range(0, len(directors))))

    el = []
    el2 = []
    for e in episodes:
        wa = [s.strip() for s in e["written_by"].split(",")]
        da = [s.strip() for s in e["directed_by"].split(",")]

        iw = []
        for n, i in wl:
            iw.append(n in wa)
        el.append(iw)

        id_ = []
        for n, i in dl:
            id_.append(n in da)
        el2.append(id_)
    return (writers, directors, el, el2)


if __name__ == "__main__":
    writers, directors, el, el2 = get_people()
    #print(*el, sep='\n')
    print(*el2, sep='\n')
    print("Count of writers:\t {}".format(len(writers)))
    print("Count of directors:\t {}".format(len(directors)))
