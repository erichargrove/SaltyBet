# Salty Bet

A simple Python program for betting on fake wrestling matches with both command-line and GUI interfaces.

## Features

- **User Management**: Add users with starting WrestleBucks
- **Match Setup**: Support for various match types (One on One, Triple Threat, Fatal 4 Way, etc.)
- **Betting System**: Place bets on wrestlers with automatic payout calculation
- **Statistics Tracking**: Win/loss records and WrestleBucks balance for each user
- **Data Persistence**: Automatic saving/loading of user data
- **Bankruptcy Protection**: Users get random WrestleBucks when they go broke

## Design

Each user starts with $1000 (WrestleBucks). Input the wrestler names for the match, then ask which wrestler the user wants to bet on, and how much. After each user inputs their bet, the program asks who won. The user selects the winner, and the app pays out the bets (double the bet for winner, zero for loser). The application keeps track of each user's win/loss record, as well as their total amount of money.

## Files

- `SaltyBet.py` - Core backend logic and command-line interface
- `SaltyBetGUI.py` - GUI interface using tkinter
- `saltybet_users.json` - User data storage (automatically created)

## Usage

### GUI Version (Recommended)
```bash
python SaltyBetGUI.py
```

### Command Line Version
```bash
python SaltyBet.py
```

## Recent Updates

### File Path Fixes
- **Fixed permissions issues**: The application now automatically finds a writable location for the data file
- **Cross-platform compatibility**: Works correctly whether run from File Explorer, terminal, or IDE
- **Smart file location**: Prioritizes the project directory, falls back to user home directory if needed
- **Better error handling**: Clear error messages for file system issues

### GUI Improvements
- **Status bar**: Shows current data file location
- **Enhanced error handling**: Better user feedback for save/load operations
- **Improved user experience**: Warning messages when data can't be saved

## Data Storage

The application automatically saves user data to `saltybet_users.json` in the project directory. If the project directory is not writable, it will attempt to save to:
1. Project directory (preferred)
2. Current working directory
3. User's home directory
4. Temporary file in project directory

## Requirements

- Python 3.6+
- tkinter (usually included with Python)
- No additional dependencies required
