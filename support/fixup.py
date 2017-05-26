#!/usr/bin/env python3

import re
import sys
import html

"""
Fix the contents of the TeX file created by MagicDraw using the requirements
LaTeX template file to allow it to work with LaTeX.
"""

# Common regexes


# Read in the specified file and write the updated version to standard out
with open(sys.argv[1], "r") as fh:
    in_table = False
    in_list = False
    for line in fh.readlines():
        line = line.rstrip()

        # Remove html pre wrappers. They can be ignored
        line = re.sub(r"<html><pre>", "", line)
        line = re.sub(r"</pre></html>", "", line)

        # standalone open and close tags can be ignored
        skip_line = False
        for t in ("html", "head", "style", "body", "b"):
            if skip_line:
                break
            if re.search(r"^\s*<{}>\s*$".format(t), line):
                skip_line = True
                break
            if re.search(r"^\s*</{}>\s*$".format(t), line):
                skip_line = True
                break

        # Style is irrelevant here
        if re.search(r"padding:\d+px", line):
            skip_line = True

        # This line is not needed
        if skip_line:
            continue

        # Remove pre tags
        line = re.sub(r"<pre>", "", line)
        line = re.sub(r"</pre>", "", line)

        # A </b> at the start of a line can probably be removed
        line = re.sub(r"^</b>", "", line)

        # Fix the title to remove the document ref from the title. The Latex
        # style handles the document ref itself and it should not be part
        # of the title
        if "title" in line:
            line = re.sub(r"L\w\w\-\d+: ", "", line)

        # Handle <ol> and <ul> tags
        line = re.sub("<ol>", r"\\begin{enumerate}", line)
        line = re.sub("</ol>", r"\\end{enumerate}", line)
        line = re.sub("<ul>", r"\\begin{itemize}", line)
        line = re.sub("</ul>", r"\\end{itemize}", line)

        # Replace & with \& if this is a section (to void table confusion)
        # May be easier to change to "and" in rth model
        if re.search(r"section\{.* & ", line):
            line = re.sub(r" & ", r" \& ", line)

        # Handle style tabs for bold and italic
        tags = {"b": "textbf", "i": "textit", "li": "item"}
        for t in tags:
            line = re.sub(r"<{0}>(.*?)</{0}>".format(t),
                          r"\\{}{{\1}}".format(tags[t]), line)

        # HTML Entity replacement
        line = html.unescape(line)

        # Parameter names need some help to be hyphenated properly
        # if they are too long for the table. We look for case changes
        # and hint to latex. The template makes this easy by using
        # \paramname{} to tell us which are names
        name = re.search(r"paramname{([A-Za-z0-9]+)}", line)
        if name:
            param = name.group(1)
            outparam = param[0]
            was_upper = outparam.isupper()
            for c in param[1:]:
                is_upper = c.isupper()
                if is_upper and not was_upper:
                    outparam += r"\-"
                was_upper = is_upper
                outparam += c
            line = re.sub(param, outparam, line)

        # Units in long tables need to be told how to split
        prefix = re.match(r"(milli)\w+$", line)
        if prefix:
            si = prefix.group(1)
            line = re.sub(r"^"+si, si+r"\-", line)

        # Now that the line is fixed up, look for list
        if re.match(r"\s*\* ", line):
            if not in_table:
                in_table = True
                print("\\begin{itemize}")
            line = re.sub(r"^\s*\*", r"\item", line)
        elif in_table and re.match(r"^\s*$", line):
            in_table = False
            print("\\end{itemize}")

        print(line)
