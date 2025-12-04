# Plants vs. Zombies (Simplified, Pygame)

A minimal tower-defense game built with `pygame`. Place plants on a 5×9 lawn grid to generate sun, shoot peas, and block zombies. Survive the waves to win.

## Description
A lightweight Pygame demo of the classic tower-defense idea: manage resources (sun), place plants (Sunflower, Peashooter, WallNut), and defend lanes from advancing zombies. Designed for beginners and coursework demos, featuring clean OOP structure, simple visuals, and scalable wave difficulty.

## Features
- Grid-based lawn with clear placement and UI buttons
- Plants:
  - Sunflower: periodically generates sun
  - Peashooter: fires bullets at zombies in its row
  - WallNut: high HP blocker
- Zombies: lane-based movement, contact attacks, HP bars
- Sun system: falling suns and plant-generated suns, click to collect
- Waves: increasing difficulty with shorter spawn intervals
- Game states: HUD, win/lose overlay, restart with `R`

## Target Audience
- Beginners learning Python game loops, events, and OOP
- Course demos and small competition projects
- Pygame learners exploring drawing, collisions, timing
- Hobbyists prototyping tower-defense mechanics

## Getting Started (Windows)
- Requirements: `Python 3.8+`, `pygame`
- Install dependencies:
```bat
pip install pygame
```
- Run the game from this folder:
```bat
python 植物大战僵尸.py
```
- Controls: Click a plant button, then click a grid cell to place. Click suns to collect. Press `R` to restart, `Esc` or close window to exit.

## Gameplay Video
![2025-12-04T05_58_15 443Z-263826](https://github.com/user-attachments/assets/31cc1514-4c62-4139-a273-d09e18414b08)

## License
MIT

## Contributing
- Fork and create a feature branch.
- Keep code simple and consistent with existing style.
- Include brief docstrings for new classes/functions.
- Update README if you add plants, zombies, or gameplay features.
