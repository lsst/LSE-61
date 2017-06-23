#!/usr/bin/env python3

import sys
import re

"""Read in the output from LSE-61-matrix.templ.txt template file and generate
a latex long table

When the command runs, a full document is sent to standard output that can
be compiled to verify the table cration, and two mapping files are written:
DMS2OSS.tex and OSS2DMS.tex. These output files are the rows for a latex
long table.
"""

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


def dumpdict(name1, name2, lut, reqtitles, fh=None, wrap=True):
    """Put dict of lists into longtable.
    name1 and name2 are the column names for table.
    name1 refers to the keys of lut and name2 to the values.
    reqtitles[] has the titles for each key in lut[].
    fh is the file handle to write the table to.
    Standard out is used if fh is None.
    wrap controls whether the table wrapper is included in the output
    or not. False, just writes the rows.
    """

    if fh is None:
        fh = sys.stdout

    if wrap:
        print(r"""
\setlength\LTleft{0pt}
\setlength\LTright{\fill}
\begin{small}
\begin{longtable}[]{|p{0.45\textwidth}|p{0.45\textwidth}@{}|}
""", file=fh)
        print(r"""\hline \textbf{%s} & \textbf{%s} \\ \hline""" %
              (name1, name2), file=fh)
        print(r"""\endhead

\hline \multicolumn{2}{r}{\emph{Continued on next page}} \\
\endfoot

\hline\hline
\endlastfoot

""", file=fh)

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
                print("{} &".format(basestr), file=fh)
                basestr = ""
                print(r"{} \\".format(reqtext(child)), file=fh)
        else:
            print(r"{} & \\".format(basestr), file=fh)
        print(r"\hline", file=fh)

    if wrap:
        print(r"""
\end{longtable}
\end{small}
""", file=fh)


print(r"""
\documentclass{article}
\usepackage{longtable}
\usepackage{geometry}
\geometry{textheight=8.5in,
          letterpaper,
          textwidth=6.5in,
          includeall,
          lmargin=1in,
          headheight=40pt,
          headsep=2em,
          marginparwidth=60pt,
          footskip=40pt}
\begin{document}
""")

passes = (("DMS", "OSS", dmsr2oss),
          ("OSS", "DMS", oss2dmsr))

for p in passes:
    # Write rows to the output file
    outfile = "{p[0]}2{p[1]}.tex".format(p=p)
    with open(outfile, "w") as outfh:
        dumpdict(*p, titles, fh=outfh, wrap=False)

    # Write to standard out
    dumpdict(*p, titles, fh=None, wrap=True)

print(r"""
\end{document}
""")
