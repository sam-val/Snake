from pathlib import *

game_folder = Path(__file__).parent.resolve()
image_folder = game_folder / 'Images'
sounds_folder = game_folder / 'Sounds'

print(sounds_folder)
