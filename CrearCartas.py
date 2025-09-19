from PIL import Image, ImageDraw, ImageFont
import os

output_folder = "cards"
os.makedirs(output_folder, exist_ok=True)

suits = {
    '♠': ('S', 'black'),
    '♥': ('H', 'red'),
    '♦': ('D', 'red'),
    '♣': ('C', 'black')}

values = {
    'A': 'Ace',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '10': '10',
    'J': 'Jack',
    'Q': 'Queen',
    'K': 'King'}

width, height = 200, 300

try:
    font = ImageFont.truetype("arial.ttf", 40)
except IOError:
    font = ImageFont.load_default()

for val_short, val_full in values.items():
    for suit_symbol, (suit_letter, color) in suits.items():
        img = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0, 0), (width-1, height-1)], outline="black", width=4)

        text = f"{val_short}{suit_symbol}"
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((width - w) / 2, (height - h) / 2), text, fill=color, font=font)

        filename = f"{val_short}{suit_letter}.png"
        img.save(os.path.join(output_folder, filename))

print("Cartas generadas en la carpeta 'cards'")
