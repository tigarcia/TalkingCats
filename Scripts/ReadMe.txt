These are the scripts (shell and python) used for the hackathon. Some are redundent and many are far from polished (e.g., paths to files are hard-coded into the script). As Rory said at the time, "this is a hackathon, not a 'good-code-athon").

Probably the more important ones are (in the order to use them):
eliminate-duplicates.py -- removes the duplicate .txt and .mml files
CleanMathML.py -- canonicalizes the MathML files.
txtToWav.py -- converts .txt files to .wav files
mathml_fixer.py -- cleans up the resulting MathML from the neural net as best it can by adding matching end tags and removing junk at the end.
