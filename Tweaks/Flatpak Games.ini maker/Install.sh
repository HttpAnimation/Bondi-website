mkdir Flatpak\ Games.ini\ maker
cd Flatpak\ Games.ini\ maker
mkdir Output
wget https://raw.githubusercontent.com/HttpAnimation/Bondi/main/Tweaks/Flatpak%20Games.ini%20maker/FlatpakGen.py
wget https://raw.githubusercontent.com/HttpAnimation/Bondi/main/Tweaks/Flatpak%20Games.ini%20maker/Games.ini
wget https://raw.githubusercontent.com/HttpAnimation/Bondi/main/Tweaks/Flatpak%20Games.ini%20maker/Install.sh
wget https://raw.githubusercontent.com/HttpAnimation/Bondi/main/Tweaks/Flatpak%20Games.ini%20maker/README.md
wget https://raw.githubusercontent.com/HttpAnimation/Bondi/main/Tweaks/Flatpak%20Games.ini%20maker/subsections.ini
rm Install.sh # You can comment this out to keep the main Install file / this one
echo "To run this tweak run in this terminal window"
echo "python3 FlatpakGen.py"