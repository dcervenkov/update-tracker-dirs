#!/usr/bin/env python3
"""A utility for convenient setup of Tracker indexed directories.

This utility was made to simplify updating of directories that Tracker
indexes. Tracker is the main way Gnome Shell searches for files (you might
need to install Tracker first). Out of the box, it indexes only a couple of
files in your $HOME. To make it useful the user needs to manipulate GSettings
where Tracker stores it's configuration (by default).

To use it, create a configuration file named 'tracker-dirs' and fill it with
the directories you wish Tracker to index. Use the following example file:

[Recursive]

$HOME/foobar

[Single]

$HOME/foo/bar
$HOME/bar/bar
"""

import os
import subprocess
import sys

CONFIG_FILE = 'tracker-dirs'

def parse_config(config_file):
    """Parse a config file and return lists of directories.

    Tracker (and this config) has two types of modes for directories - single
    and recursive. We separate them and return two lists. Empty lines as well
    as lines starting with '#' are ignored.

    Returns:
        (list, list): List of 'single' directories and a list of 'recursive' directories.

    """
    single = []
    recursive = []

    with open(config_file, 'r') as f:
        for line in f:
            entry = line.strip()
            if entry == "" or entry[0] == "#":
                continue

            if entry[0] == "[" and entry[-1] == "]":
                section = entry[1:-1]
                continue

            if section == "Recursive":
                recursive.append(entry)
            elif section == "Single":
                single.append(entry)

    return single, recursive


def check_if_dirs_exist(dirs):
    """Check if directories exist, applying environment variable expansion.

    Args:
        dirs (str): Directories to be checked.

    Returns:
        int: Number of non-existing directories.

    """
    non_existing = []
    for directory in dirs:
        if not os.path.isdir(os.path.expandvars(directory)):
            non_existing.append(directory)

    if non_existing:
        print("ERROR: The following directories don't exist:")
        for directory in non_existing:
            print(directory)

    return len(non_existing)


def update_tracker_dirs(single, recursive):
    """Set up Tracker to index the supplied directories.

    Args:
        single (list): A list of strings (directory paths) to be indexed non-recursively
        recursive (list): A list of strings (directory paths) to be indexed recursively

    """
    single_string = "['" + "', '".join(single) + "']"
    recursive_string = "['" + "', '".join(recursive) + "']"

    return_code = subprocess.call(
        ['gsettings', 'set', 'org.freedesktop.Tracker.Miner.Files',
         'index-recursive-directories', recursive_string])
    if return_code != 0:
        print("An error occured while trying to set recursive directories!")
        sys.exit(1)

    return_code = subprocess.call(
        ['gsettings', 'set', 'org.freedesktop.Tracker.Miner.Files',
         'index-single-directories', single_string])
    if return_code != 0:
        print("An error occured while trying to set single directories!")
        sys.exit(2)

    print("Success! " + str(len(single + recursive)) +
          " directories placed under Tracker surveilance.")


def main():
    single, recursive = parse_config(CONFIG_FILE)
    if not check_if_dirs_exist(single + recursive):
        update_tracker_dirs(single, recursive)


main()
