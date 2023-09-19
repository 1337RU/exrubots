import random
import colorama
from colorama import Fore, Back, Style
import ecdsa
import base58
import requests
from Crypto.Hash import keccak
from telegram import Bot
import schedule
import time

def keccak256(data):
    hasher = keccak.new(digest_bits=256)
    hasher.update(data)
    return hasher.digest()

def get_signing_key(raw_priv):
    return ecdsa.SigningKey.from_string(raw_priv, curve=ecdsa.SECP256k1)

def verifying_key_to_addr(key):
    pub_key = key.to_string()
    primitive_adder = b"\x41" + keccak256(pub_key)[-20:]
    Addr = base58.b58encode_check(primitive_adder)
    return Addr

def send_message_to_telegram(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=chat_id, text=message)

def generate_and_send_results():
    count = 0
    print(Fore.CYAN + "Please Wait..." + Style.RESET_ALL)
    while True:
        raw = bytes(random.sample(range(0, 256), 32))
        key = get_signing_key(raw)
        Wallet = verifying_key_to_addr(key.get_verifying_key()).decode()
        HexAdd = base58.b58encode_check(Wallet.encode()).hex()
        publickey = key.get_verifying_key().to_string().hex()
        privatekey = raw.hex()

        count += 1
        message = f"{count} | {privatekey} | {Wallet}"

        send_message_to_telegram(bot_token, chat_id, message)

        f = open("trxKey.txt", "a")
        f.write(privatekey+'\n')
        f.close()
        f1 = open("trxAdd.txt", "a")
        f1.write(Wallet+'\n')
        f1.close()

        time.sleep(600)

if __name__ == "__main__":
    bot_token = "5838447661:AAHzdxt0gooFuRiI12-rsnKx40hOt9LChIs"  # Замените на токен вашего телеграм-бота
    chat_id = "5108542147"  # Замените на ID чата, куда нужно отправлять сообщения

    schedule.every(10).minutes.do(generate_and_send_results)

    while True:
        schedule.run_pending()
        time.sleep(1)
