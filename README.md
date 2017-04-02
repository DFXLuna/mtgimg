# mtgimg
Usage: python3 mtgimg.py [-o \<outfile\>] [-f \<fontfile\>] [-s \<fontsize\>] [-v] \<infile\>

Example: python3 mtgimg.py -o Decklist.png -v decklist.txt

#### infile format
<x> \<cardname\>

Example: 4 Fatal Push

#### Flags

* -o: Specify output file name other than default. Can handle most typical image formats.
* -f: Specify a custom font file other than Source Sans Pro. Can handle open type formats[.ttf]
* -s: Specify font size. 20 is default.
* -v: Enable verbose output.
