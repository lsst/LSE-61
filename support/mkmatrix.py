#!/usr/bin/env python3

import sys
import re

"""Read in the output from LSE-61-matrix.templ.txt template file and generate
a latex long table"""

make_doc = True
dmsr2oss = {}
oss2dmsr = {}
titles = {}

# Read in the specified file and fill dicts mapping requirements
with open(sys.argv[1], "r") as fh:
    for line in fh.readlines():
        line = line.rstrip()
        if line.startswith("DMS"):
            # Lines of form "DMS-REQ-???? Some text"
            # describe the title of the DMS requirement.
            # Lines of form "DMS-REQ-???? XXX-REQ-???? Some Text"
            # Show tracing and title of traced element
            if "OSS-REQ" in line or "LSR-REQ" in line:
                dms, refines, title = line.split(" ", maxsplit=2)
                title_key = refines
                if refines not in oss2dmsr:
                    oss2dmsr[refines] = []
                oss2dmsr[refines].append(dms)
                dmsr2oss[dms].append(refines)
            else:
                dms, title = line.split(" ", maxsplit=1)
                if title.startswith("DMS-REQ-"):
                    # We are not interested in DMS requirements derived
                    # from other DMS requirements
                    continue
                title_key = dms
                dmsr2oss[dms] = []
            titles[title_key] = title


def text2tex(title):
    """Latexify a string"""
    title = re.sub("&", r"\&", title)
    return title

def dumpdict(name1, name2, lut, reqtitles):
    """Put dict of lists into longtable.
    name1 and name2 are the column names for table.
    name1 refers to the keys of lut and name2 to the values.
    titles[] has the titles for each key in lut[].
    """

    print(r"""
\setlength\LTleft{0pt}
\setlength\LTright{\fill}
\begin{small}
\begin{longtable}[]{|p{0.45\textwidth}|p{0.45\textwidth}@{}|}
""")
    print(r"""\hline \textbf{%s} & \textbf{%s} \\ \hline""" % (name1, name2))
    print(r"""\endhead

\hline \multicolumn{2}{r}{\emph{Continued on next page}} \\
\endfoot

\hline\hline
\endlastfoot

""")

    def reqtext(reqid):
        return "{} {}".format(reqid, text2tex(reqtitles[reqid]))

    # Each table is done as
    # REQNUM Title & REQNUM title
    #              & REQNUM title
    for root in sorted(lut):
        basestr = reqtext(root)
        # sometimes there is no tracing
        if lut[root]:
            for child in lut[root]:
                print("{} &".format(basestr))
                basestr = ""
                print(r"{} \\".format(reqtext(child)))
        else:
            print(r"{} & \\".format(basestr))
        print(r"\hline")

    print(r"""
\end{longtable}
\end{small}
""")

if make_doc:
    print(r"""
\documentclass{article}
\usepackage{longtable}
\begin{document}
""")

# Write out the tables
dumpdict("DMS", "OSS", dmsr2oss, titles)
dumpdict("OSS", "DMS", oss2dmsr, titles)

if make_doc:
    print(r"""
\end{document}
""")
