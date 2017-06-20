# LSE-61: LSST Data Management System Requirements

Baselined versions of this document can be obtained from DocuShare at <https://ls.st/LSE-61>.

This repository hosts reports from the LSE-61 MagicDraw model in LaTeX format.

To generate a new version of the document from the model:

* Upload the template file from the `support/` directory to MagicDraw using the _Report Wizard_.
* Select the `LSE-61: Data Management System Requirements` part of the model within the _Report Wizard_.
* Generate a `LSE-61.tex` file.
* The output from MagicDraw requires some processing before it can be built using LaTeX. This mainly includes converting HTML elements to LaTeX equivalents.
  Run the following command to do these fixes:
```bash
$ ./support/fixup.py /wherever/LSE-61.tex > LSE-61.tex
```

The resultant file should be buildable at this point.
Check that it builds before committing it.
The document requires the [lsst-texmf](https://lsst-texmf.lsst.io) LaTeX classes are available.

The document title, author, date, document handle, and change record are defined in the file `metadata.tex`.
This allows you to specify these outside of the generic MagicDraw template file.
