# Changelog

## [1.2.1]
### Fixed
- Release action

## [1.2.0]
### Added
- Added option to _index_ command to specify which columns to use as data source
- Supporting DCS Scratchpad steerpoint with multiple coordinate formats
- Supporting DCS Scratchpad steerpoint with elevation only in feet
- Added possibility to load aerodrome information using # command in scratchpad file
- Building zipapp / executable archive

### Changed
- Moved from PIP to Poetry
- Moved resource files into packages and using importlib

### Removed
- No longer building Windows executable

## [1.1.1] - 2021-11-19
### Changed
- Updated README with instruction correct instruction for running this version of the application

## [1.1.0] - 2021-11-19
### Added
- Support for delimited text file import
- Added coordinates for aerodromes on the Caucasus, Syria, Mariana, Nevada and Persian Gulf maps. Data from Minsky's excellent kneeboard files: https://www.digitalcombatsimulator.com/en/files/3312200/

### Changed
- File option for scratchpad command is now positional

### Fixed
- Index value was not converted to string when using index command

## [1.0.1] - 2021-11-07
### Fixed
- Erroneous use of class value

## [1.0.0] - 2021-11-07

### Added
- Driver for F-16
- Support for CombatFlite mission plan excel export
- Support for Excel coordinates import
- Support for DCS Scratchpad coordinates import
- Support for Aerodromes excel coordinates import
- Bingo command for DCS Scratchpad data file

### Changed
- Using Python argparse to parse commandline arguments
