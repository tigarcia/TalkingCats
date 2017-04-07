The inputs here come from three open source math texts along with some questions/exercises that are separate from one of the texts. Their format is MathML, although the quality varies some. There is a little content MathML (e.g., col10614_1.3_complete/MathML/m18870-math07.mml) that was weeded out because we want a uniform target.

After a little cleanup, the inputs were then fed into MathPlayer to generate speech. The speech styles were various ClearSpeak styles (different runs were made with preferences such as speaking implied times turned on/off). Also, Simple speak's "learning disabilities" were used to generate verbose and terse output. These are the .txt files. The files use SAPI5 style XML cues to force the speech engine to pause, say letters correctly, etc.

From the various algebra books, only about 70% of the examples were unique. Changing the speech preferences and styles also generated a lot of duplication. These duplicates were removed and that is what the "...NoDuplicates..." versions are.

The MathML is canonicalized. This removes tags such as <semantics>, duplicate <mrow>s, <mspace>, etc. <mrow>s are also flattened so that the same speech will generate the same MathML. If there were more time, I probably would have gone for structured <mrow>s. Also, <mfenced> needs dealing with. There are almost certainly other cleanups that would be useful. The "redundant" top-level <math> tag is removed to make it easier on the neural net. Hence toplevel element is <mrow>, <mfrac>, etc.

Finally, .wav files were generated from these. Including these would consume hundreds of gigabytes. They are ommitted from githup but can be regenerated with Scripts/txtToWav.py.
