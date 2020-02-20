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
        for s in re.findall(r'[\u4e00-\u9fff]+', note["Chinese"]):
            if len(s) == 1 or len(s) > 3: continue
            if "我" in s or "你" in s or "他" in s: continue
            for c in s:
                wordsWithChar[c].append(s)

    for nid in col.findNotes("deck:'Chinese Characters::Current'"):
        note = col.getNote(nid)
        if note["Hanzi"] in wordsWithChar:
            examples = sorted(wordsWithChar[note["Hanzi"]], key=lambda s: len(s))
            newExamples = examples[0:min(len(examples),3)]
            note["Examples"] = ", ".join(newExamples)
            note.flush()
    col.save()
    col.close()

if __name__ == "__main__":
    main()
