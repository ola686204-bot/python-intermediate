# ls        --- Mac/Linux: list files in current directory
# ls -la    --- include hidden files, show permissions and sizes
# ls -lh    --- human-readable file sizes (KB, MB)
# ls *.py   --- list only .py files
# dir       --- Windows: list files
# dir /a    --- include hidden files
# dir *.py  --- list only .py files

 The -l flag gives a detailed view with permissions, owner, size, and modification date. The -a flag shows hidden files (those starting with . on Mac/Linux).

# OpenPython lets you run Python directly in your browser while following structured lessons and interactive exercises.

Practise Python →

# cd — Change Directory
# cd projects/myapp    ---  go into a subdirectory
# cd ..                ---  go up one level
# cd ../..             ---  go up two levels
# cd ~                 ---  go to your home directory
# cd -                 ---  go back to the previous directory
# cd /                 ---  go to the root directory

On Windows:

# cd projects\myapp    --- go into a subdirectory
# cd ..                --- go up one level
# cd %USERPROFILE%     --- go to home directory
# Tip: Press Tab after typing the first few characters of a directory name to autocomplete. Press Tab twice to see all matching options.
# mkdir — Create a Directory
# mkdir my-project                --- create a single directory
# mkdir -p projects/myapp/tests   --- create nested directories at once
# mkdir my-project
# mkdir projects\myapp\tests
# The -p flag (Mac/Linux) creates parent directories automatically — no error if they already exist. On Windows, mkdir handles nested paths natively.
# rmdir / rm -rf — Delete a Directory
# rmdir empty-folder          ---  remove an empty directory
# rm -rf full-folder          ---  remove a directory and all its contents
# rmdir /s /q folder-name     ---  Windows: remove directory and contents
# Warning: rm -rf has no undo. There's no Recycle Bin for terminal deletions. Double-check before running it.

 File Commands:

# touch — Create an Empty File
# touch script.py       --- create a new empty file
# touch .env            --- create a hidden config file
# touch also updates the modification timestamp of an existing file. On Windows, there's no exact equivalent — use New-Item script.py in PowerShell or just open a text editor.


 cat / type — View File Contents
# cat requirements.txt    --- Mac/Linux: print file contents
# cat -n script.py        --- print with line numbers
# type requirements.txt   --- Windows: equivalent of cat
# For long files, use less requirements.txt instead — it paginates the output so you can scroll. Press q to exit less.


# cp — Copy a File or Directory
# cp source.py destination.py       --- copy a file
# cp -r source-folder/ destination/ --- copy a directory recursively
# cp *.py backup/                   --- copy all .py files to backup/

 Windows:

# copy source.py destination.py
# xcopy /s source-folder destination-folder
# mv — Move or Rename
# mv old-name.py new-name.py    --- rename a file
# mv script.py scripts/         --- move a file to a directory
# mv *.py src/                  --- move all .py files to src/

 Windows:
 
# rename old.py new.py  --- rename
# move old.py scripts\  --- move
# rm — Delete a File
# rm unwanted.py       ---  delete a file (no undo)
# rm *.pyc             ---  delete all .pyc files
# rm -i important.py   ---  prompt before deleting

 Windows:
* del unwanted.py
# del *.pyc
# Python Workflow Commands
# Running Scripts
# python3 script.py                      # Mac/Linux
# python3 script.py arg1 arg2            # with arguments
# python script.py                       # Windows (Python 3 installation)
# py script.py                           # Windows (using py launcher)
# py -3.11 script.py                     # Windows (specific version)
# For the full breakdown, see How to Run a Python File (.py).
# 
# Version and Path Checks
# python3 --version          # check Python version
# which python3              # Mac/Linux: show full path to python3
# where python               # Windows: show full path to python
# python3 -c "import sys; print(sys.path)"  # show module search path
# pip — Package Management
# pip3 install requests                    # install a package
# pip3 install requests==2.31.0            # specific version
# pip3 install -r requirements.txt        # install from file
# pip3 uninstall requests                  # remove a package
# pip3 list                                # list all installed packages
# pip3 show requests                       # details about a package
# pip3 freeze > requirements.txt          # export current environment
# pip3 install --upgrade pip              # upgrade pip itself
# On Windows, use pip instead of pip3. For reliability, use python3 -m pip to ensure you're using the pip that belongs to your current Python. For the full pip reference, see Python Commands: The Essential Terminal Reference.
# 
# Virtual Environments
# python3 -m venv venv                  # create a virtual environment
# source venv/bin/activate              # Mac/Linux: activate
# venv\Scripts\activate                 # Windows: activate
# deactivate                            # deactivate (any OS)
# After activating, the prompt shows (venv) and Python/pip commands use the environment's isolated packages. For a complete guide, see Python Virtual Environments and pip Guide.
# 
# Searching and Finding
# grep — Search File Contents
# grep "import requests" script.py      # find a pattern in one file
# grep -r "def main" .                   # search recursively in all files
# grep -rn "TODO" .                      # show line numbers
# grep -ri "error" logs/                 # case-insensitive search
# grep -l "import pandas" *.py           # show only filenames with matches
# grep -v "test" requirements.txt        # lines NOT containing "test"
# Windows (PowerShell):
# 
# Select-String "import requests" script.py
# Get-ChildItem -Recurse | Select-String "def main"
# Or use findstr in Command Prompt:
# 
# findstr /s /i "error" *.py
# find — Search for Files
# find . -name "*.py"                     # find all .py files
# find . -name "*.pyc" -delete            # find and delete all .pyc files
# find . -type d -name "__pycache__"      # find all __pycache__ directories
# find . -mtime -1                        # files modified in the last day
# Windows PowerShell:
# 
# Get-ChildItem -Recurse -Filter "*.py"
# Get-ChildItem -Recurse -Include "*.pyc" | Remove-Item
# Process Control
# Ctrl + C — Stop a Running Script
# The most important keyboard shortcut in the terminal. Press Ctrl + C to send a KeyboardInterrupt signal to whatever is running. This works for Python scripts, long-running commands, and accidentally-started processes.
# 
# Ctrl + Z — Suspend
# Suspends the running process without killing it. The process is paused in the background. Use fg to bring it back to the foreground or bg to let it run in the background.
# 
# & — Run in Background
# python3 server.py &       # run in background, get prompt back immediately
# jobs, fg, bg
# jobs         # list background and suspended jobs
# fg           # bring the most recent job to foreground
# fg %2        # bring job #2 to foreground
# bg %1        # resume job #1 in the background
# kill — Terminate a Process
# ps aux | grep python3     # find Python processes
# kill 12345                # terminate process by PID
# kill -9 12345             # force kill (if regular kill didn't work)
# pkill -f script.py        # kill by script name
# Windows:
# 
# tasklist | findstr python    # find Python processes
# taskkill /PID 12345          # terminate by PID
# taskkill /F /IM python.exe   # force kill all Python processes
# I/O Redirection and Pipes
# > and >> — Output Redirection
# python3 script.py > output.txt          # save stdout to file (overwrite)
# python3 script.py >> log.txt            # append stdout to file
# python3 script.py 2> errors.txt        # save stderr to file
# python3 script.py > out.txt 2>&1       # save both stdout and stderr
# python3 script.py > /dev/null 2>&1     # discard all output
# | — Pipes
# Connect the output of one command to the input of another:
# 
# python3 -m pip list | grep requests      # check if requests is installed
# cat log.txt | grep "ERROR" | wc -l      # count error lines
# ls -la | sort -k5 -n                    # sort files by size
# python3 script.py | tee output.txt      # print to terminal AND save to file
# < — Input Redirection
# python3 script.py < input.txt           # feed a file as stdin
# Environment and Configuration
# export / set — Environment Variables
# export FLASK_ENV=development            # Mac/Linux: set an env var
# export DATABASE_URL="postgresql://..."  # set for current session
# printenv FLASK_ENV                      # check a specific variable
# env                                     # list all environment variables
# Windows:
# 
# set FLASK_ENV=development               # set for current session
# set FLASK_ENV                           # check a specific variable
# set                                     # list all variables
# which / where — Find Executables
# which python3           # Mac/Linux: full path to python3
# which pip3              # full path to pip3
# where python            # Windows: full path to python
# where pip               # Windows: full path to pip
# History and Shortcuts
# These aren't commands but make the terminal dramatically faster:
# 
# Shortcut	Effect
# ↑ / ↓	Cycle through command history
# Tab	Autocomplete file/directory name
# Tab Tab	Show all completions
# Ctrl + R	Search command history
# Ctrl + L	Clear the terminal (same as clear)
# Ctrl + A	Jump to beginning of line
# Ctrl + E	Jump to end of line
# Ctrl + W	Delete the previous word
# Ctrl + C	Stop current command
# Ctrl + D	Exit the shell (or signal EOF)
# Ctrl + R is particularly useful — it searches your entire command history by substring. Type part of a past command and press Ctrl + R repeatedly to cycle through matches.
# 
# Mac/Linux vs Windows Quick Reference
# Task	Mac/Linux	Windows (cmd)	Windows (PowerShell)
# Show directory	pwd	cd	pwd
# List files	ls -la	dir	ls
# Change directory	cd folder	cd folder	cd folder
# Create directory	mkdir folder	mkdir folder	mkdir folder
# Delete file	rm file	del file	rm file
# Copy file	cp src dst	copy src dst	cp src dst
# Move/rename	mv src dst	move src dst	mv src dst
# Print file	cat file	type file	cat file
# Find in files	grep -r pattern .	findstr /s pattern *.py	Select-String -Recurse pattern
# Run Python	python3 script.py	python script.py	python script.py
# Activate venv	source venv/bin/activate	venv\Scripts\activate	venv\Scripts\Activate.ps1
# Common Mistakes
# Typing rm -rf without verifying the path. This permanently deletes everything at that path. Always print the path first or use ls -la path to confirm what you're about to delete.
# 
# Forgetting to activate a virtual environment. If you install packages and they don't show up when running your script, you're probably running without the environment activated. Check with which python3.
# 
# Using absolute paths in scripts shared across machines. /home/alice/projects/data.csv works on Alice's machine but fails everywhere else. Use relative paths or Path(__file__).parent.
# 
# Closing the terminal while a script is still running. The script is killed immediately. For scripts that should survive terminal closure, use nohup python3 script.py & (Mac/Linux) or run as a background service.
# 
# Not using Tab completion. Typing full paths and filenames manually is slow and error-prone. Press Tab liberally.
# 
# Troubleshooting
# "command not found" — Either the command isn't installed, or it isn't in PATH. Check with which command_name. For Python: install Python and add it to PATH.
# 
# "Permission denied" on a file operation — Your user account doesn't have access. Use chmod 644 filename (Mac/Linux) to change permissions, or prefix the command with sudo (if you have sudo privileges and understand the implications).
# 
# Output keeps scrolling and I can't stop it — Press Ctrl + C to stop the process, or q if it's a pager like less or man.
# 
# Previous commands filling my screen — Run clear or press Ctrl + L to clear the terminal display.
# 
# Tab completion not working — You may need bash-completion installed. On Mac: brew install bash-completion. On Ubuntu: sudo apt install bash-completion.
# 
# Frequently Asked Questions
# What's the fastest way to learn terminal commands?
# 
# Use them for real tasks. Start by navigating to project folders with cd instead of a GUI, and running Python scripts with python3 instead of clicking an IDE button. Each time you need something done, look up the command, run it, and you'll remember it next time.
# 
# Are these commands the same on every Linux distribution?
# 
# Core commands like ls, cd, mkdir, rm, and grep are standard across all Linux distributions and Mac. The differences appear in package managers (apt vs dnf vs pacman) and some system-specific tools.
# 
# How do I clear the terminal?
# 
# Type clear and press Enter, or press Ctrl + L. The terminal scrollback history is still accessible by scrolling up.
# 
# How do I run a command that requires root/admin access?
# 
# On Mac/Linux, prefix with sudo: sudo apt install python3. You'll be prompted for your password. On Windows, open the terminal "as Administrator" (right-click the shortcut → Run as administrator).
# 
# Can I run terminal commands from Python?
# 
# Yes — use subprocess.run(). See Python Run Shell Command: subprocess and os.system for the full guide.
# 
# How do I search through my command history?
# 
# Press Ctrl + R and type part of the command you're looking for. Press Ctrl + R again to cycle through older matches. Press Enter to run the found command.
# 
# What's the difference between Ctrl + C and Ctrl + Z?
# 
# Ctrl + C terminates the running process completely. Ctrl + Z suspends it (pauses it in the background). Suspended jobs can be resumed with fg (foreground) or bg (background).
# 
# How do I see a command's documentation?
# 
# man command_name (Mac/Linux) opens the manual page. Press q to exit. Or use command_name --help for a shorter summary. On Windows, command_name /?? shows help for most built-in commands.
# 
# Related Reading
# How to Open Terminal on Any OS — get a terminal open before using these commands
# How to Run a Python File (.py) — run Python scripts from the terminal
# Python Commands: The CLI Reference — Python-specific terminal commands in depth
# Python Run Shell Command: subprocess — call terminal commands from within Python code
# How to Run a Bash Script — automate sequences of terminal commands
# Python Virtual Environments and pip Guide — manage packages with terminal commands
# Official References
# GNU Coreutils Manual — authoritative reference for ls, mkdir, cp, mv, rm, cat, and more
# Bash Reference Manual — complete bash command and scripting reference
# PowerShell Documentation — Windows PowerShell command reference
# Summary
# Terminal commands are the backbone of a Python developer's workflow. Navigation (cd, ls, pwd), file management (cp, mv, rm), and Python workflow (python3, pip3, venv) are what you'll use every day.
# 
# The fastest way to get comfortable is to use the terminal for real tasks rather than relying on GUI tools. Start with cd and ls to navigate, python3 script.py to run scripts, and pip3 install to manage packages. The rest comes naturally as you need it.
# 
# One habit that changes everything: use Tab for autocomplete constantly, and Ctrl + R to search command history. Between those two shortcuts, you'll rarely have to type a long command or path from scratch.
# 
# Build a real project using this concept.
# 
# Reading is a great start — writing the code yourself is how it actually sticks. Keep going with a free, interactive course.
# 
# Complete Interactive Python Exercises →
# Written by
# 
# OpenPython Team
# 
# The OpenPython editorial team writes Python tutorials, guides, and programming resources for developers at every level. Each article is reviewed for technical accuracy before publication.
# 
# Discussion
# Sign in to join the discussion.
# 
# No comments yet. Be the first to start the discussion!
# 
# More Articles
# Understand SQL Table Relationships Before You Write a JOIN
# 10 min read
# by OpenPython Team
# Learn Python on a phone or tablet with browser code practice
# Can You Learn Python on a Phone or Tablet? What Works Best
# 17 min read
# by OpenPython Team
# SQL NULL vs Zero vs Empty Text: What Each Value Means
# 7 min read
# by OpenPython Team
# All Articles
# Take the Python Course
# Start Your Python Journey
# 200+ interactive lessons across Python, data, web, and more. 100% free.
# 
# Start Free Course
# Keep building
# 
# Your next line starts here.
# Start learning free
# →
# OpenPython icon
# OpenPython
# Free Python programming education for everyone. Learn to code with interactive lessons and hands-on exercises.
# 
# support@openpython.org
# Join our Discord
# Learn
# All Courses
# Learn Python
# Python Playground
# Python Tools
# Resources
# All Resources
# Python Cheat Sheet
# HTML & CSS Cheat Sheet
# Coding Roadmap
# Python Errors Guide
# For Teacher
# Company
# About Us
# Contact
# Privacy Policy
# Terms of Service
# Refund Policy
# Disclaimer
# Cookie Settings
# © 2026 OpenPython. All rights reserved. Free Python education for everyone.
# 
# Join the community on Discord
# 
