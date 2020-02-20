import sys, re, os
from collections import defaultdict
sys.path.append("pylib/build/lib")
from anki.storage import Collection
PROFILE_HOME = "/home/brandon/.local/share/Anki2/User 1"
cpath = os.path.join(PROFILE_HOME, "collection.anki2")
col = Collection(cpath, log=True)

def main():
    wordsWithChar = defaultdict(list)
    for nid in col.findNotes("note:Basic"):
        note = col.getNote(nid)
        if note.hasTag("phrases"): continue
        for s in re.findall(r'[\u4e00-\u9fff]+', note["Chinese"]):
            for c in s:
                wordsWithChar[c].append(s)

    curDeckID = col.decks.nameMap()["Chinese Characters::Current"]["id"]

    for nid in col.findCards("deck:'Chinese Characters::Remaining'"):
        card = col.getCard(nid)
        if card.note()["Hanzi"] in wordsWithChar:
            card.did = curDeckID
            card.flush()
    col.save()
    col.close()

if __name__ == "__main__":
    main()
