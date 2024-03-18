clean:
	- /bin/rm -f *-*.out

realclean: clean
	- /bin/rm -f accounting_short accounting_postprocessed.feather
