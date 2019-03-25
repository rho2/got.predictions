import json
import re

STATE_ALIVE = 1
STATE_UNKNOWN = 0
STATE_DEAD = -1

RE = re.compile('[^a-zA-Z]')


def get_episode_names():
    with open("../data/episodes.json", 'r') as file:
        episodes = json.load(file)["episodes"]

    ep = {}
    for e in episodes:
        name = RE.sub('', e["title"])
        id_ = e["number"]

        ep[name] = id_-1
    return ep


def get_appearance_data(ep):
    ep = get_episode_names()

    with open("../data/chars.json", 'r') as file:
        chars = json.load(file)

    cal = []
    for c in chars:
        co = []
        print(c["slug"])
        ca = [STATE_UNKNOWN] * len(ep)
        # print(len(c["appearances"]))
        for a in c["appearances"]:
            state = STATE_ALIVE

            if a.endswith("*"):
                state = STATE_DEAD
                a = a[:-1].strip()
            a = RE.sub('', a)

            ei = ep[a]
            ca[ei] = state

        cal.append(ca)
        if len(cal) == 2:
            break  # todo remove
    return cal


def interpolate_single(data):
    start = 0
    cur = False

    return data


def interpolate_data(abc):
    cd = []
    for d in abc:
        foo = interpolate_single(d)
        print(foo)
        cd.append(foo)


def get_appearances():
    ep = get_episode_names()
    cal = get_appearance_data(ep)

    cal_clean = interpolate_data(cal)

    return cal_clean


if __name__ == "__main__":
    [print(a) for a in get_appearances()]
