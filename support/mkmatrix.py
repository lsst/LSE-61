#!/usr/bin/env python3

import sys

"""Read in the output from LSE-61-matrix.templ.txt template file and generate
a latex long table"""

dmsr2oss = {}
oss2dmsr = {}

# Read in the specified file and fill dicts mapping requirements
with open(sys.argv[1], "r") as fh:
    for line in fh.readlines():
        line = line.rstrip()
        if line.startswith("DMS"):
            dms, refines = line.split(" ", 2)
            if dms not in dmsr2oss:
                dmsr2oss[dms] = []
            if refines.startswith("OSS") or refines.startswith("LSR"):
                if refines not in oss2dmsr:
                    oss2dmsr[refines] = []
                oss2dmsr[refines].append(dms)
                dmsr2oss[dms].append(refines)

def dumpdict(name1, name2, lut):
    """Put dict of lists into longtable.
    name1 and name2 are the column names for table.
    name1 refers to the keys of lut and name2 to the values.
    """

    print(r"""
\setlength\LTleft{0pt}
\setlength\LTright{\fill}
\begin{small}
\begin{longtable}[]{|lp{0.8\textwidth}@{}|}
""")
    print(r"""\hline \textbf{%s} & \textbf{%s} \\ \hline""" % (name1, name2))
    print(r"""\endhead

\hline \multicolumn{2}{r}{\emph{Continued on next page}} \\
\endfoot

\hline\hline
\endlastfoot

""")

    for root in sorted(lut):
        print("{} &".format(root))
        print(r"{} \\".format(", ".join(lut[root])))

    print(r"""\hline
\end{longtable}
\end{small}
""")

# Write out the tables
dumpdict("DMS", "OSS", dmsr2oss)
dumpdict("OSS", "DMS", oss2dmsr)
