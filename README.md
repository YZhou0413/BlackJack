### How to run the game code:
#### dependencies:
- python version: 3.13
- please run `pip3 install -r requirements.txt` to install external libraries
#### do this in the root folder in your terminal to start the game:
- for Unix system: `python3 -m blackjack`
- for Windows system: `py -m blackjack`
#### for in-game operations, please refer to the [rules](src/gui/pages/rules.md)


### repository structure:
```bash
root
├── blackjack # to mask the run command
│   └── __main__.py
├── src # game source code
│   ├── core # core game logic & modules
│   │   ├── cards.py # card module 
│   │   ├── game.py # game logic
│   │   ├── __init__.py
│   │   ├── login_panda.py # communicate between game and user database
│   │   └── player.py # in-game player module
│   ├── gui # UI
│   │   ├── game_ui # in-game UI
│   │   │   ├── buttons_stack.py # buttons in game
│   │   │   ├── card_ui.py # card display logic
│   │   │   ├── card_view.py # card display view
│   │   │   ├── game_table.py # game table ui
│   │   │   ├── __init__.py
│   │   │   ├── player_area.py # player side on the game table
│   │   │   └── test_dummys.py # test dummies
│   │   ├── __init__.py
│   │   ├── login # login ui
│   │   │   ├── __init__.py
│   │   │   ├── login_approve_dialog.py # create new user dialog
│   │   │   └── login.py # existing user login
│   │   ├── main.py # main window
│   │   ├── pages # widgets manager
│   │   │   ├── __init__.py
│   │   │   ├── menu.py # game menu widget
│   │   │   ├── place_bet.py # user place bet widget 
│   │   │   ├── rules_view.py # rule display widget
│   │   │   └── scoreboard.py # scoreboard display widget
│   │   ├── PNG-cards # cards asset
│   │   └── app-icon # app icon files
│   └──  __init__.py
└── test # test modules
    ├── conftest.py # test fixtures
    ├── test_game_unit.py 
    └── test_win_lose.py # test game logic
```
  
