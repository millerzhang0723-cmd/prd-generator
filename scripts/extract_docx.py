# -*- coding: utf-8 -*-
import zipfile
import sys
from xml.etree import ElementTree as ET


def docx_to_text(path: str) -> str:
    with zipfile.ZipFile(path, "r") as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    paras: list[str] = []
    for p in root.iter(ns + "p"):
        texts: list[str] = []
        for t in p.iter(ns + "t"):
            if t.text:
                texts.append(t.text)
            if t.tail:
                texts.append(t.tail)
        line = "".join(texts).strip()
        if line:
            paras.append(line)
    return "\n".join(paras)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print("===", p, "===")
        print(docx_to_text(p))
