# mtgimg
![Example image](https://github.com/DFXLuna/mtgimg/blob/master/exampledraft.png "Example image")


Create stream ready decklists. Compatible with most decklists generated online including those by mtggoldfish.com

Usage: python3 mtgimg.py [-o \<outfile\>] [-f \<fontfile\>] [-s \<fontsize\>] [-v] \<infile\>

Example: python3 mtgimg.py -o Decklist.png -v decklist.txt

#### File format
\<x\> \<cardname\>

Example:

4 Fatal Push
1 Path to Exile
2 Thoughseize

#### Flags

* -o: Specify output file name other than default. Can handle most typical image formats.
* -f: Specify a custom font file other than Source Sans Pro. Can handle open type formats[.ttf]
* -s: Specify font size. 20 is default.
* -v: Enable verbose output.
