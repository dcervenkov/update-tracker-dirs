# update-tracker-dirs

This utility was made to simplify updating of directories that [Tracker](https://wiki.gnome.org/Projects/Tracker) indexes. Tracker is the main way Gnome Shell searches for files (you might need to install Tracker first). Out of the box, it indexes only a couple of files in your `$HOME`. To make it useful the user needs to manipulate GSettings where Tracker stores it's configuration (by default). 

## Usage

To be able to use Gnome Shell file search in the overview you just need to install Tracker,

```
sudo apt install tracker
```
and then setup the directories you want it to track. This is where this script comes in.

To use it, create a configuration file named `tracker-dirs` and fill it with the directories you wish Tracker to index. Tracker has two modes - *single* for directories that are to be indexed non-recursively and *recursive* for (gasp) recursive indexing. Let the following example config file guide you:

```
[Recursive]

$HOME/foobar

[Single]

$HOME/foo/bar
$HOME/bar/bar
```
Then just run the script and **log out**. The overlay search should work the next time you log in.

## Note

It might take a while for Tracker to index your directories. You can view the indexing status using
```
tracker status
```