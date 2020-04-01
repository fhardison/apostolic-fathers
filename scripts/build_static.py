#!/usr/bin/env python3

from roman_numerals import convert_to_numeral


WORK_LIST = [
    "001-i_clement",
    "002-ii_clement",
    "003-ignatius-ephesians",
    "004-ignatius-magnesians",
    "005-ignatius-trallians",
    "006-ignatius-romans",
    "007-ignatius-philadelphians",
    "008-ignatius-smyrnaeans",
    "009-ignatius-polycarp",
    "010-polycarp-philippians",
    "011-didache",
    "012-barnabas",
    "013-shepherd",
    "014-martyrdom",
    "015-diognetus",
]

TITLES = {
    "001": "The First Epistle of Clement",
    "002": "The Second Epistle of Clement",
    "003": "Ignatius to the Ephesians",
    "004": "Ignatius to the Magnesians",
    "005": "Ignatius to the Trallians",
    "006": "Ignatius to the Romans",
    "007": "Ignatius to the Philadelphians",
    "008": "Ignatius to the Smyrnaeans",
    "009": "Ignatius to Polycarp",
    "010": "Polycarp to the Philippians",
    "011": "The Didache",
    "012": "The Epistle of Barnabas",
    "013": "The Shepherd of Hermas",
    "014": "The Martyrdom of Polycarp",
    "015": "The Epistle to Diognetus",
}


for WORK in WORK_LIST:
    print(WORK)
    SRC = f"../texts/{WORK}.txt"
    DEST = f"../docs/{WORK}.html"

    TITLE = TITLES[WORK[:3]]

    HEADER = f"""\
    <!DOCTYPE html>
    <html lang="grc">
    <head>
    <title>{TITLE}</title>
    <meta charset="utf-8">
    <meta name="viewport"  content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/alpheios-components@latest/dist/style/style-components.min.css"/>
    <link href="https://fonts.googleapis.com/css?family=Noto+Serif:400,700&amp;subset=greek,greek-ext" rel="stylesheet">
    <link href="style.css" rel="stylesheet">
    </head>
    <body>
      <div class="container alpheios-enabled" lang="grc"">
      <nav>&#x2191; <a href="./">Open Apostolic Fathers</a></nav>
      <h1 lang="en">{TITLE}</h1>
    """

    FOOTER = """\
      </div>
        <script type="text/javascript">
          document.addEventListener("DOMContentLoaded", function(event) {
            import ("https://cdn.jsdelivr.net/npm/alpheios-embedded@latest/dist/alpheios-embedded.min.js").then(embedLib => {
              window.AlpheiosEmbed.importDependencies({
                mode: 'cdn'
              }).then(Embedded => {
                new Embedded({
                  clientId: 'greek_leaners_text_project'
                }).activate();
              }).catch(e => {
                console.error(`Import of Alpheios embedded library dependencies failed: ${e}`)
              })
            }).catch(e => {
              console.error(`Import of Alpheios Embedded library failed: ${e}`)
            })
          });
        </script>
    </body>
    </html>
    """

    with open(SRC) as f:
        with open(DEST, "w") as g:
            prev_section = None
            prev_chapter = None
            print(HEADER, file=g)
            for line in f:
                parts = line.strip().split(maxsplit=1)
                ref = parts[0].split(".")
                if len(ref) == 2:
                    section = None
                    chapter, verse = ref
                else:
                    section, chapter, verse = ref
                if prev_section != section:
                    if prev_section is not None:
                        print("   </div>""", file=g)
                        print("   </div>""", file=g)
                    print("""   <div class="section">""", file=g)
                    prev_section = section
                    prev_chapter = None
                if prev_chapter != chapter:
                    if prev_chapter is not None:
                        if prev_chapter == "0":
                            if section is None:
                                print("""    </div>""", file=g)
                        else:
                            print("""    </div>""", file=g)
                    if chapter == "0":
                        if section is None:
                            print("""    <div class="preamble">""", file=g)
                    else:
                        if chapter == "SB":
                            print("""    <div class="subscription">""", file=g)
                        elif chapter == "EP":
                            print("""    <div class="epilogue">""", file=g)
                        else:
                            print("""    <div class="chapter">""", file=g)
                            print(f"""      <h3 class="chapter_ref">{convert_to_numeral(int(chapter))}</h3>""", file=g)
                    prev_chapter = chapter
                if chapter == "0" and verse == "0":
                    print(f"""    <h2 class="section_title">{parts[1]}</h2>""", file=g)
                else:
                    if chapter == "EP" and verse == "0":
                        print(f"""<h3 class="epilogue_title">{parts[1]}</h3>""", file=g)
                    else:
                        if verse != "1":
                            print(f"""      <span class="verse_ref">{verse}</span>""", end="&nbsp;", file=g)
                        print(parts[1], file=g)
            print("""    </div>""", file=g)
            if section is not None:
                print("""    </div>""", file=g)
            print(FOOTER, file=g)
