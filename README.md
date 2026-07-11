# Movie Subtitles Words Extractor

Movie Subtitles Words Extractor is free and open source software.

Homepage: https://github.com/MykolaMorhun/movie-subtitles-words-extractor

## Table of contents

- [About the app](#about-the-app)
  - [What the app does](#what-the-app-does)
  - [Reasoning why it was created](#reasoning)
  - [Which languages are supported](#which-languages-are-supported)
  - [License](#license)
- [Installation and building](#installation-and-building)
  - [How to install](#how-to-install)
    - [Download from releases](#download-a-binary-from-releases)
    - [Run as script](#running-the-app-script-locally)
    - [Build standalone binary](#building-binary-locally)
  - [How to uninstall](#how-to-uninstall)
- [Usage Scenarios and Tips](#usage-scenarios-and-tips)
  - [Single movie](#single-movie)
  - [Whole season](#whole-season)
  - [All seasons](#all-seasons)
  - [Processing arbitrary text files](#processing-arbitrary-text-files)
  - [Excluding already known vocabulary](#excluding-already-known-vocabulary)
  - [Watching tips](#watching-tips)
  - [Where to get subtitles?](#where-to-get-subtitles-for-your-movie)
- [Detailed documentation](#detailed-documentation)
- [Troubleshooting](#troubleshooting)

## About the app

### What the app does

In short, it converts a movie subtitles `srt` files into a text file with alphabetically sorted unique words.
Also, it has other features like excluding words, statistics, etc.

To understand the purpose of the app, see [reasoning](#reasoning) on why it was created.

### Reasoning

The aim of the application is to help people to understand foreign language by watching movies.

For many people who learn a foreign language, it might be hard to understand native speakers and the barrier in some cases could be quite high.
While reading and writing could be on a quite decent level, understanding speech (especially in non training environments) might be challenging.
A safe and nice option is to watch movies in the language you learn.
However, if a person struggles to understand speech, just watching a movie won't be very efficient.
A classic helper here is the movie subtitles.
Seems, it should work pretty nice, but there is a big trap.
Many people, wanting to recheck if they got a phrase right, look at the subtitles and then just start reading them.
It happens imperceptibly.
For many people, if you pay attention, you might be able to catch yourself on reading most of the time.
Reading subtitles while watching is also a learning technique, but if the primary goal is to understand the speech, it could become a false friend.
If you really want to train your listening skills, the best approach is to turn off the subtitles!
But now, how to learn?
With subtitles on, it's possible to learn a new word, but how to be without them?
Even with the subtitles on, there is no guarantee that all words is known to the person.
The solution here is to learn all words which are used in the movie before watching it.
How can one do that?
Right, by reading the subtitles and learn everything you don't know.
While technically it works, there is still a problem: it spoils the movie.
Do you really want to know the whole plot and how it ends before watching?
For some people it might be ok, but for many such a spoiler is no go.
And to solve this last problem this app is coming.
It takes all words from the movie subtitles (so you won't miss a word and can be well prepared), deduplicates and sorts them alphabetically (so no spoilers included).
Also, it has a nice feature to exclude known words, so you don't have to read over known to you vocabulary every time.
Please read through [usage scenarios](#usage-scenarios-and-tips) to better understand how the app could be useful to you.

### Which languages are supported

Originally, the app was designed for English, but theoretically it should work with any other language.

Depending on your operation system and settings, for some files with non English language, you might need to set correct encoding in the application settings.

### License

The application source code is licensed under `GNU General Public License` version 2 or any newer.

## Installation and building

### How to install

There are a few ways to install the app:
 1. [Download a binary from releases](#download-a-binary-from-releases)
 2. [Clone this repository and run the app](#running-the-app-script-locally)
 3. [Build binary locally](#building-binary-locally)

#### Download a binary from releases

Go to the app [homepage](https://github.com/https://github.com/MykolaMorhun/movie-subtitles-words-extractor) on GitHub, navigate to the [releases](https://github.com/https://github.com/MykolaMorhun/movie-subtitles-words-extractor/releases) section and download the latest version for your system.

#### Running the app script locally

If you have `python` installed, you can run the app script locally.
Note, `python 3.9` or newer is required.
No external dependencies needed.

1. Get the source code.
You can clone app source repository
```
git clone https://github.com/https://github.com/MykolaMorhun/movie-subtitles-words-extractor
```
or just [download zip archive](https://github.com/https://github.com/MykolaMorhun/movie-subtitles-words-extractor/archive/refs/heads/main.zip) at the right top of the page and unpack it into a directory.

2. When the source is downloaded, run the app script:
```
python main.py
```

### Building binary locally

This section is mostly for developers and technical people.
It will be easier to just [download the app from releases](#download-a-binary-from-releases) or [run it as a python script](#running-the-app-script-locally).

You can check the GitHub workflows in this repository on how to do it for your platform.

### How to uninstall

Just delete the binary or source repository directory, that's it.

## Usage Scenarios and tips

- [Single movie](#single-movie)
- [Whole season](#whole-season)
- [All seasons](#all-seasons)
- [Processing arbitrary text files](#processing-arbitrary-text-files)
- [Excluding already known vocabulary](#excluding-already-known-vocabulary)
- [Watching tips](#watching-tips)
- [Where to get subtitles?](#where-to-get-subtitles-for-your-movie)

### Single movie

1. In the top frame named `Include words from files`, click `Add Files` button.
1. Select the subtitles file. Note, on some systems (mostly Linux) the scroll is horizontal.
1. Click `Process and Save` button and select the destination file. Alternatively, click `Preview` to look at the result or edit it.

### Whole season

It's assumed that you have a directory with subtitles file for each episode, for example:
```
|--season02
   |--s02e01.srt
   |--s02e02.srt
   |--s02e03.srt
   ...
```

1. In the top frame named `Include words from files`, click `Add Directory` button and select the folder with your subtitles files in the appeared dialog window (`season02` in the example above). Note, to select a folder you need to enter (not just select) the folder and click `OK` button. Look at `Selection` field of the dialog to see which folder will be used.
1. Click `Process and Save` button and select the destination file. Alternatively, click `Preview` to look at the result or edit it.

Note, the subtitles files can have arbitrary name, but extension must be `.srt`.
Additionally, see [how to include any text files](#processing-arbitrary-text-files).

### All seasons

It's assumed that you have a directory that contains sub directories with subtitles file for each episode, for example:
```
|--TV Show
   |--season01
   |  |--s01e01.srt
   |  |--s01e02.srt
   |  |--s01e03.srt
   |  ...
   |--season02
   |  |--s02e01.srt
   |  |--s02e02.srt
   |  |--s02e03.srt
   |  ...
   ...
   |--season10
      |--s10e01.srt
      |--s10e02.srt
      |--s10e03.srt
      ...
```

1. Ensure you have `Search recursively in directories` enabled in settings.
1. In the top frame named `Include words from files`, click `Add Directory` button and select the directory that contains sub directoris (`TV Show` in the example above). Note, to select a folder you need to enter (not just select) the folder and click `OK` button. Look at `Selection` field of the dialog to see which folder will be used.
1. Click `Process and Save` button and select the destination file.

### Processing arbitrary text files

The application allows including or excluding words from any text file.
By default, the application searches for files with `srt` and `txt` extensions.
This could be changed in the selection dialog.
Just select `*.*` mask for `Files of type` in the open file dialog and then select any text file.
Also, it's possible to create a custom mask in the settings, see `additional file filter` option.

Note, if you use `Add Directory` button, the only way to change the mask is via settings, see `directory files filter` option.

If the app fails with `Failed to process <file>: ... can't decode byte`, see [Troubleshooting](#failed-to-process-file-codec-cant-decode-byte).

### Excluding already known vocabulary

It's assumed that you already have a text file with known to you words.
A word per line is preferred, for example:
```
a
the
he
tree
...
```
and it's saved to `known-words.txt` (or any other text file).

1. In the top frame named `Include words from files`, click `Add Files` button and select your subtitles file(s).
1. In the bottom frame named `Exclude words from files`, click `Add Files` button and select file(s) with already known to you words.
1. Click `Process and Save` button and select the destination file. The resulting file will not contain words from files in the exclude section. Alternatively, click `Preview` to look at the result or edit it.

Note, to avoid adding the same exclude file every time, go to settings and set `automatically add exclude file` option.

### Watching tips

- It's recommended to work with the unknown words list before watching.
- Learn not only unknown to you words translation, but the pronunciation as well.
- A word could have different meanings, especially if it's part of an idiom or used with phrasal verbs, etc.
- Don't stress too much if you are struggling to remember a few words, you can still watch the movie and understand almost everything.
- Learn your video player hotkeys, especially for turning on / off subtitles and rewinding (some players allow to rewind different amount of time depending on the hotkey used).
- If you failed to understand a phrase, just rewind.
- For some people it's better to rewind a few / dozen seconds before a problematic phrase.
- If several rewinds didn't help, turn on subtitles, rewind, watch and read the phrase, turn off subtitles, rewind one more time. Alternatively, look up the place in the subtitles file directly.

### Where to get subtitles for your movie

There are many web sites with free subtitles.
A few examples:
 - [opensubtitles.org](https://www.opensubtitles.org)
 - [sub-scene.com](https://sub-scene.com/)
 - [addic7ed.com](https://www.addic7ed.com/)
 - [downsub.com](https://downsub.com/)
 - [tvsubtitles.net](https://www.tvsubtitles.net/)

Very often just searching `<Movie name> subtitles` in a web search engine works.

Some sites allow downloading subtitles for the whole TV series season.

## Detailed documentation

- [Main window](#main-window)
  - [Select files widget](#select-files-widget)
  - [Open files dialog](#open-files-dialog)
  - [Open directory dialog](#open-directory-dialog)
  - [Main window buttons bar](#main-window-buttons-bar)
- [Results editor window](#results-editor-window)
- [Stats window](#stats-window)
- [Settings window](#settings-window)

### Main window

When the application is started, the main window appears.
It contains:
 - Main menu from which [Settings window](#settings-window) can be opened.
 - Include and exclude words from [select files widgets](#select-files-widget) in the main area.
 - [Button bar](#main-window-buttons-bar) in the bottom.

#### Select files widget

Select files widget allows to choose files to process.
It has list of already included files (might be empty) and buttons bar at the bottom:
 - `Add files` opens [files dialog](#open-files-dialog) that allows to select one or more files that should be added to the files list.
 - `Add directory` opens [directory dialog](#open-directory-dialog) that allows to choose directory to add files from.
 - `Remove file` removes selected file from the list, files on disk are not affected.
 - `Clear` removes all files from the list, files on disk are not affected.

#### Open files dialog

Open files dialog allows to select one or more files.
To better filter files, change `Files of type` and pick required file mask.
Note, you can define your own mask in settings be setting `Additional file filter`.
If current directory contains many files or other directories, you need to scroll.
On some systems (mostly Linux) the scroll is horizontal.

#### Open directory dialog

Open directory dialog allows to choose a directory.
To select a directory enter into it and click `OK` (just selecting a directory from the list is not enough).
To check which directory is going to be selected check the `Selection` field.
To change which files should be added into the list, change the `Directory file filter` in the settings.
To allow searching in all sub directories of selected directory enable `Search recursively in directories` in the settings.

#### Main window buttons bar

 - `Process and Save` processes the files and asks user for a file into which the result must be saved.
 - `Preview` processes the files and opens [Results editor window](#results-editor-window) dialog where user can check and edit the result before saving.
 - `Stats` processes the files and opens [Stats window](#stats-window) dialog where statistic about the result is available.
 - `Clear` removes all items from both include words and exclude words lists, files on disk are not affected.

### Results editor window

Results editor window allows to check the resulting list of words and edit them before saving.
Editor font size can be changed in the settings.

Buttons have the following actions:
 - `Save to file` asks user for a file into which the text from the edit area will be saved.
 - `Copy to clipboard` copies text from the edit area into the system clipboard, so the user can paste it into another program, e.g. a word processor, a text editor, email, etc.
 - `Close` closes the editor window and returns user to the main window.

### Stats window

Stats window displays statistic for the resulting words.
The window title has total number of words in the result.
The main area contains table with two columns:
 - `Word` that contains list of unique words in the result.
 - `Count` displays number of occurrences of the word in the source file(s).

By clicking at the columns name, it's possible to sort the table.

### Settings window

To open the settings window, from the main menu of the [Main window](#main-window) click on `Program` -> `Settings`.

The settings window contains of following settings sections:
 - [Files section](#files-settings-group)
 - [Interface section](#interface-settings-group)

and the [bottom bar](#settings-window-bottom-bar).

#### Files settings group

The `Files` group contains settings related to files selecting and processing.
Available options are:
 - `Default working directory` if enabled, the chosen directory will be shown in [open files](#open-files-dialog) or [open directory](#open-directory-dialog) dialogs.
    Could useful when subtitles (and other files to process) stored separately from the application.
    If disabled, the directory from which the application was run is shown.
 - `Automatically add exclude file` if enabled, allows to choose a file which will be added automatically to the exclude list at every application start.
    Nothing happens if disabled, even if a file is selected.
 - `Enable file size limit` if enabled, applies limit to file size to process.
    If a file has size bigger than allowed in `Max file size`, the application will refuse to process files with corresponding error.
    This is done to prevent processing of potentially wrong files.
    An attempt to process a huge file on machine with low RAM could slow down or even hang the system.
 - `Max file size` sets the maximum allowed file size in megabytes.
    If a file exceeds the value, the application will refuse to process files with corresponding error.
    Applies only if `Enable file size limit` is enabled.
 - `Fallback text encoding` defines back up text encoding if system default failed with given file.
    Note, you can input the encoding freely.
    The [full list](https://docs.python.org/3.9/library/codecs.html#standard-encodings) could be found in python docs.
    A wrong value will cause errors until fixed in the settings.
 - `Additional file filter` allows to create new item in `Files of type` file mask list in [open files dialog](#open-files-dialog).
    Example values: `*.txt *.adoc`, `*.py`
 - `Directory files filter` allows to define which file mask by which files are selected in [open directory dialog](#open-directory-dialog).
    Example values: `*.srt *.txt`, `*.srt`, `*.txt *.adoc`
 - `Search recursively in directories` if enabled, looks for files in all sub directories of selected directory in [open directory dialog](#open-directory-dialog).
   If disable, looks only in the selected directory ignoring all sub directories.
 - `Enable directories search file limit` if enabled, stops when reaches the file number limit while selecting files in [open directory dialog](#open-directory-dialog).
   This options help to prevent adding to much files by mistake.
 - `Directories search file limit` sets the limit for how many files [open directory dialog](#open-directory-dialog) can add to the list.
   Applies only when `Enable directories search file limit` is enabled.

#### Interface settings group

The `Interface` gruop contains settings related to user interface of the application.
Available options are:
 - `Theme` defines which interface theme to use.
    It's possible to see the theme preview by just picking one from the list.
    Note, themes might differ depending on the operation system and its version.
 - `Remember windows size` if enabled, remembers size of each window so user can adjust the size according to their preference.
    If disabled, every time a window is opened it has default predefined size.
    `Auto-save` must be enabled to remember changes to windows size automatically.
    Alternatively, one can disable `Auto-save`, set desired windows size and save settings manually, creating new default sizes.
 - `Remember order in Stats` if enabled, remembers the way of sorting in the table in the [statistics window](#stats-window).
 - `Editor font size` allows to change font size of the [results editor window](#results-editor-window).

#### Settings window bottom bar

Settings window bottom bar has the following controls:
 - `Auto-save` checkbox, if enabled, always saves settings into file at application exit.
 - `Cancel` button closes the window ignoring all changes.
 - `Reset` button restores default values for all settings (but doesn't apply them).
 - `Save` button closes the window, applies the changes and permanently saves the settings into `spsettings,ini` file.
 - `Apply` button closes the window and applies the settings for the current session only.
    The changes will not be saved after application exit, unless `Auto-save` is enabled.
    It's a safe way to try out some settings.

## Troubleshooting

#### Failed to process file codec can't decode byte

When try to process file(s), the app shows the following error:
`Failed to process ... codec can't decode byte ...`

It could mean one of the following:
  - The text file has different from the system default encoding.
    Try to change the `fallback text encoding` in the settings.
    (try `utf-8` and `cp1252` first).
    Check [full list of encodings](https://docs.python.org/3.9/library/codecs.html#standard-encodings).
    Note, you can type any string as encoding name, but a wrong value will cause errors until fixed in the settings.
    Alternatively, convert the file into your operation system default encoding.
  - The file is a binary file and not a text file.

#### Failed to process file unknown encoding

When try to process file(s), the app shows the following error:
`Failed to process ... file: unknown encoding: ...`

You've set a wrong `fallback text encoding` in the settings.
Correct it or reset settings to defaults.

#### How to reset settings to defaults

Delete `spsettings.ini` file.

Also, it's possible via [settings window](#settings-window).
