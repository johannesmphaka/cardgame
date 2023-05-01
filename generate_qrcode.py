import qrcode

url = "https://johannesmphaka-cardgame-app-r9w6ha.streamlit.app"
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill='black', back_color='white')
img.save('cardgame_code.png')