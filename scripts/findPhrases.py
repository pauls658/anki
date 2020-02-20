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
        elif len(note["Chinese"]) > 3:
            print(note["Chinese"])

if __name__ == "__main__":
    main()
