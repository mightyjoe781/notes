from PIL import Image, ImageDraw, ImageFont

width = 500
height = 500
text_color = (255, 255, 255)  # white
background_color = (0, 0, 0)

# Load IBM Plex Mono font with larger font size
font_size = 300
font = ImageFont.truetype("/Users/smk/Library/Fonts/IBMPlexMono-MediumItalic.ttf", font_size)


# Create a new image
image = Image.new("RGB", (width, height), background_color)
draw = ImageDraw.Draw(image)

text = "S"

left, top, right, bottom = font.getbbox(text)  # Use font.textsize()
text_width = right - left
# bounding box is not same as the font size
offset = 180
text_height = bottom - top + offset
x = (width - text_width) / 2
y = (height - text_height) / 2

draw.text((x, y), text, font=font, fill=text_color)


# Display the image
# image.show()

# Save the image
image.save("public/logos/pfp.png")


