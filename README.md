# app_mvr
app_mvr is a python script to move Synology applications between volumes. The script is built using the commands/knowledge found [here](http://www.mcleanit.ca/blog/synology-move-application-volumes/).

Why did I make this script when there's only five lines of code to begin with? Because I needed to move all of the applications on /volume1 and I'm "lazy" and didn't feel like typing the same five lines for all of the applications on the volume (hence my --all option.)

To install just upload the script to somewhere on the synology and run `sudo python /path/to/app_mvr.py <args>`.

	Usage: sudo python app_mvr.py --app TextEditor --from /volume1 --to /volume2
		--app	<APP>	The apps name found in the @appstore directory.
		--all			Alternative to --app. Moves all applications on the source volume.
		--from	<VOL>	The volume the app is currently installed on.
		--to	<VOL>	The destination volume you want the app installed on.