import sys, re, os
sys.path.append("pylib/build/lib")
from anki.storage import Collection
PROFILE_HOME = "/home/brandon/.local/share/Anki2/User 1"
cpath = os.path.join(PROFILE_HOME, "collection.anki2")
col = Collection(cpath, log=True)

PinyinToneMark = {
    0: "aoeiuv\u00fc",
    1: "\u0101\u014d\u0113\u012b\u016b\u01d6\u01d6",
    2: "\u00e1\u00f3\u00e9\u00ed\u00fa\u01d8\u01d8",
    3: "\u01ce\u01d2\u011b\u01d0\u01d4\u01da\u01da",
    4: "\u00e0\u00f2\u00e8\u00ec\u00f9\u01dc\u01dc",
}

def decode_pinyin(s):
    s = s.lower()
    r = ""
    t = ""
    for c in s:
        if c >= 'a' and c <= 'z':
            t += c
        elif c == ':':
            assert t[-1] == 'u'
            t = t[:-1] + "\u00fc"
        else:
            if c >= '0' and c <= '5':
                tone = int(c) % 5
                if tone != 0:
                    m = re.search("[aoeiuv\u00fc]+", t)
                    if m is None:
                        t += c
                    elif len(m.group(0)) == 1:
                        t = t[:m.start(0)] + PinyinToneMark[tone][PinyinToneMark[0].index(m.group(0))] + t[m.end(0):]
                    else:
                        if 'a' in t:
                            t = t.replace("a", PinyinToneMark[tone][0])
                        elif 'o' in t:
                            t = t.replace("o", PinyinToneMark[tone][1])
                        elif 'e' in t:
                            t = t.replace("e", PinyinToneMark[tone][2])
                        elif t.endswith("ui"):
                            t = t.replace("i", PinyinToneMark[tone][3])
                        elif t.endswith("iu"):
                            t = t.replace("u", PinyinToneMark[tone][4])
                        else:
                            t += "!"
            r += t
            t = ""
    r += t
    return r

def replaceLatex(obj):
    pinyin = obj.group(1)
    ret = ""
    for p in pinyin.split(" "):
        ret += decode_pinyin(p) + " "
    ret = ret[:-1]
    return ret

def fixNote(note):
    print(note["Pinyin"])
    newPin = re.sub("\\\\p{([^}]*)}", replaceLatex, note["Pinyin"])
    newPin = newPin.replace("[latex]", "")
    newPin = newPin.replace("[/latex]", "")
    print(newPin)
    note["Pinyin"] = newPin
    note.flush()

def main():
    for nid in col.findNotes("note:Basic"):
        note = col.getNote(nid)
        fixNote(note)

    col.save()
    col.close()

if __name__ == "__main__":
    main()
