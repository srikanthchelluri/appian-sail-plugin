**This project isn't actively maintained. It's intended for engineers at Appian and is likely outdated with some of the other tools engineers have available. I'm leaving this code up in case anyone finds this useful though.**

# Auto-complete for Appian SAIL

This repository contains source code and files to add auto-complete functionality for Appian SAIL in Sublime Text 3. It has a few parts and requires (just a little) setup. This won the *Best Process/Productivity* Indie Time award in July.

### Setup
1. Make sure you have SAIL syntax highlighting for Sublime Text 3 already (see Home for `sail.tmLanguage`).
2. Copy `sail.sublime-settings` and `sail.sublime-completions` into your Sublime Text 3 user directory (`[path to ST3]/Packages/User/`).
3. Run `snippet-generatory.py` and `internal-generator.py` from any directory.

### Breakdown

###### `sail.sublime-settings`
Defines and contains the trigger for auto-complete in SAIL.

###### `sail.sublime-completions`
Contains all "public" (to designers) functions in one JSON file. These are the functions which are in the documentation. They do **not** have parameter completion...yet (currently no plans for it, either).

###### `snippet_generator.py`
Parses system rules directly as long as your local Appian repo is located in the correct directory.

###### `internal_generator.py`
Parses internal Appian functions using resource files as long as your local Appian repo is located in the correct directory. Because of the loose nature that these functions are documented, these functions may not have fully accurate parameters.

Contact: [Srikanth Chelluri](mailto:sc5ba@virginia.edu), Mathew Jennings.
