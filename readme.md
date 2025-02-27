# Jump to Window NVDA Add-on #

This add-on allows NVDA users to quickly jump to windows by searching for text in their titles or console content.

## Features

* Quickly focus windows by searching for text in their titles
* Search console windows for specific text content
* Support for regular expressions in searches
* Simple keyboard shortcut (NVDA+\) to activate the search dialog

## Usage

1. Press NVDA+\ to open the search dialog
2. Type the text or regular expression you want to search for
3. Press Enter to search
4. If a matching window is found, it will be brought to the foreground and focused

This package is based on the NVDA add-on template for development, building, distribution and localization.
For details about NVDA add-on development, please see the [NVDA Add-on Development Guide](https://github.com/nvdaaddons/DevGuide/wiki/NVDA-Add-on-Development-Guide).
The NVDA add-on development/discussion list [is here](https://nvda-addons.groups.io/g/nvda-addons)

Copyright (C) 2012-2021 NVDA Add-on team contributors.
Copyright (C) 2023-2025 Jump to Window add-on contributors.

This package is distributed under the terms of the GNU General Public License, version 2 or later. Please see the file COPYING.txt for further details.

## Technical Information

This add-on works by:
1. Searching through all desktop windows for matching titles
2. If no title matches, searching through console windows for matching text
3. Focusing the first matching window found

## Development

To build the add-on from source:

1. Clone the repository
2. Open a command prompt and navigate to the repository folder
3. Run `scons` to build the add-on
4. The built add-on will be placed in the current directory

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This package is distributed under the terms of the GNU General Public License, version 2 or later.
