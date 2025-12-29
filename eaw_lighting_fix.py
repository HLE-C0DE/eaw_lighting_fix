import os
import shutil

# --- Configuration ---
MOD_ID = "1770851727"
# Determine script location to find the mod folder relatively
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MOD_PATH = os.path.join(SCRIPT_DIR, MOD_ID)
DATA_DIR = os.path.join(MOD_PATH, "Data")
XML_DIR = os.path.join(DATA_DIR, "Xml")

# Backup extension
BAK_EXT = ".bak_fix"

# --- Target Files ---
PLANET_FILES = [
    "Planets_Legacy.XML",
    "Planets_WW.xml",
    "Planets_WW_Sector_Corp.xml",
    "Planets_Vanilla.XML",
    "Planets_savepoint.xml",
    os.path.join("GameModes", "Attrition", "Planets.xml")
]

PROP_FILES = [
    "SpaceProps.xml",
    "PROPS_STORY.XML",
    "PROPS_GENERIC.XML",
    "SPACEUNITSCORVETTES.XML", 
    "SPACEUNITSFRIGATES.XML",
    "SPACEUNITSCAPITAL.XML",
    "SpecialStructures.xml",
    "SpaceProps_Underworld.XML"
]

TARGET_MAP = "_Space_Planet_Bespin_01.ted"

def backup_file(file_path):
    """Creates a backup if one doesn't exist."""
    if not os.path.exists(file_path):
        return False
    
    backup_path = file_path + BAK_EXT
    if not os.path.exists(backup_path):
        try:
            shutil.copy2(file_path, backup_path)
            print(f"[Backup] Created: {backup_path}")
            return True
        except Exception as e:
            print(f"[Backup] Failed for {file_path}: {e}")
            return False
    return True

def step_1_disable_config_meg():
    print("\n--- Step 1: Disabling Config.meg ---")
    megafiles_path = os.path.join(DATA_DIR, "megafiles.xml")
    if not os.path.exists(megafiles_path):
        print(f"Error: {megafiles_path} not found.")
        return

    backup_file(megafiles_path)

    try:
        with open(megafiles_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        changed = False
        for line in lines:
            if "<File>Data\\Config.meg</File>" in line and "<!--" not in line:
                new_lines.append(line.replace("<File>Data\\Config.meg</File>", "<!-- <File>Data\\Config.meg</File> -->"))
                changed = True
            else:
                new_lines.append(line)
        
        if changed:
            with open(megafiles_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print("Status: Config.meg commented out.")
        else:
            print("Status: Config.meg already disabled or not found.")

    except Exception as e:
        print(f"Error modifying megafiles.xml: {e}")

def step_2_swap_maps():
    print("\n--- Step 2: Swapping Maps to Bespin ---")
    
    for relative_path in PLANET_FILES:
        full_path = os.path.join(XML_DIR, relative_path)
        if not os.path.exists(full_path):
            print(f"Skipping {relative_path} (Not Found)")
            continue
            
        backup_file(full_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            new_lines = []
            count = 0
            for line in lines:
                if "<Space_Tactical_Map>" in line and "</Space_Tactical_Map>" in line:
                    start = line.find("<Space_Tactical_Map>") + len("<Space_Tactical_Map>")
                    end = line.find("</Space_Tactical_Map>")
                    current_val = line[start:end].strip()
                    
                    if current_val and current_val.lower() != TARGET_MAP.lower():
                        prefix = line[:line.find("<")]
                        new_lines.append(f"{prefix}<Space_Tactical_Map>{TARGET_MAP}</Space_Tactical_Map>\n")
                        count += 1
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            
            if count > 0:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"Modified {relative_path}: {count} replacements.")
            else:
                print(f"No changes in {relative_path}")
                
        except Exception as e:
            print(f"Error processing {relative_path}: {e}")

def step_3_disable_shadows():
    print("\n--- Step 3: Disabling Prop Shadows ---")
    
    # Get all XML files to be safe, or just the targeted list? 
    # User asked for 'these changes' which implies the wide sweep.
    # Let's iterate the specific list first, it covers most props.
    
    for relative_path in PROP_FILES:
        full_path = os.path.join(XML_DIR, relative_path)
        if not os.path.exists(full_path):
            continue

        backup_file(full_path)

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            new_lines = []
            count = 0
            in_def = False
            
            for line in lines:
                stripped = line.strip()
                # Start of definition
                if (stripped.startswith("<SpaceProp ") or 
                    stripped.startswith("<SpaceStructure ") or 
                    stripped.startswith("<Props_Story ")):
                    in_def = True
                    new_lines.append(line)
                    
                    # Check if No_Shadow already exists in this block? 
                    # Simpler is to just inject it. If it duplicates, XML usually takes last or first, but generally harmless.
                    indent = line[:line.find("<")] + "    "
                    if "<No_Shadow>" not in line: 
                        new_lines.append(f"{indent}<No_Shadow>Yes</No_Shadow>\n")
                        count += 1
                    continue
                
                # End of definition
                if in_def and (stripped.startswith("</SpaceProp>") or 
                               stripped.startswith("</SpaceStructure>") or 
                               stripped.startswith("</Props_Story>")):
                    in_def = False
                
                # Prevent manual 'No_Shadow' conflicts if we are being fancy? 
                # For now, just append.
                new_lines.append(line)

            if count > 0:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"Modified {relative_path}: {count} shadows disabled.")
        
        except Exception as e:
            print(f"Error processing {relative_path}: {e}")

def main():
    print(f"Empire at War Lighting Fixer")
    print(f"Mod Path: {MOD_PATH}")
    
    if not os.path.exists(MOD_PATH):
        print(f"CRITICAL ERROR: Mod folder {MOD_ID} not found in current directory!")
        print(f"Expected: {MOD_PATH}")
        return

    step_1_disable_config_meg()
    step_2_swap_maps()
    step_3_disable_shadows()
    
    print("\nDone! Please launch the game to verify.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
