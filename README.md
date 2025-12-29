# EAW Lighting Fixer

**Target Mod:** [STEAM-1770851727] Empire at War Remake: Clone Wars
**Focus:** Space Skirmish Maps (Visuals)

## Overview
This utility standardizes lighting and backgrounds across Space Skirmish maps to fix visual inconsistencies (e.g., lighting from below). It replaces map backgrounds with the "Bespin" preset and disables object shadows to prevent rendering artifacts.

## Features
*   **Map Standardization**: Forces all targeted Space Skirmish maps to use the Bespin environment (Background/Lighting).
*   **Shadow Removal**: Disables `<No_Shadow>` on props and structures to prevent "light cuts" or rendering errors between ships and the background.
*   **Config Disable**: Comments out `Config.meg` in `megafiles.xml` to ensure loose XML files are loaded.

## Usage
1.  Ensure the script `eaw_lighting_fix.py` is located in the workshop content folder (`.../content/32470`).
2.  Run the script:
    ```bash
    python eaw_lighting_fix.py
    ```
3.  Launch the game to verify changes.

*Note: The script creates `.bak_fix` backups of modified files.*
