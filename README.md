phprepl
=======

Simple REPL for php.

.    show current snippet
.c   clear last line
.ca  clear all
.r   run current snippet
.s   save snippet to a temporary file

[NOTES]    * Failed lines won't be saved in the snippet
           * Use <tab> to autocomplete function names
           * CTRL-D exits


Start the repl
--------------

Start via ./phprepl.py or the standalone ./phpreplsa.py

	$ ./phpreplsa.py 
	php [0] >> echo 2+2;
	==> Running /var/folders/K7/K7q1uIQgHGWYSScL9KPgu++++TI/-Tmp-/tmpynDodf 
	4 
	php [1] >> .c
	==> Cleared last line 
	php [2] >> $z = date("m.d.Y");
	==> Running /var/folders/K7/K7q1uIQgHGWYSScL9KPgu++++TI/-Tmp-/tmp6tLsVd 
	php [3] >> echo $z;
	==> Running /var/folders/K7/K7q1uIQgHGWYSScL9KPgu++++TI/-Tmp-/tmpBanlRd	
	02.23.2011 
	php [9] >> ^D
	
	$ 
