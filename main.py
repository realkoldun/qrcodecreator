import telebot
import qrcode
from background import keep_alive
from PIL import Image
from pyzbar.pyzbar import decode

token = '5995007189:AAFu6lbWtfKwp2QwYlvCaAP7enU9u12QRDs'
filename = "qr.png"
err = "Не удалось расшифровать QR Code"
image = 'image.jpg'
qrCode = qrcode.QRCode(version=1, box_size=30, border=4)

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Hello, ept!')

@bot.message_handler(commands=['createqrcode'])
def create(message):
    bot.send_message(message.chat.id, 'Enter your txt')
    bot.register_next_step_handler(message, creating_qr)

def creating_qr(message):
    if message.text:
        qrCode.add_data(message.text)
        qrCode.make()
        img = qrCode.make_image()
        img.save(filename)
        bot.send_photo(message.chat.id, photo=open(filename, 'rb'))

@bot.message_handler(commands=['decryptqrcode'])
def decrypt(message):
    bot.send_message(message.chat.id, 'Upload a pic')
    bot.register_next_step_handler(message, decrypt_qr)

def decrypt_qr(message):
    if message.photo:
        bot.send_message(message.chat.id, f'ща')
        fileid = message.photo[-1].file_id
        file_info = bot.get_file(fileid)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(image, 'wb') as new_file:
            new_file.write(downloaded_file)
        if decode(Image.open(image)):
            datatxt = decode(Image.open(image))
            bot.send_message(message.chat.id, datatxt)
        else:
            bot.send_message(message.chat.id, err)

keep_alive()
bot.infinity_polling()
