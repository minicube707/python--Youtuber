import qrcode
import os

import qrcode.constants

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)

img = qrcode.make("Hello World§ This is is Neuralnine")
img.save("qrcode.png")

qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=2)
qr.add_data("https://www.youtube.com")
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color = 'white')
img.save("qrcode advenced.png")