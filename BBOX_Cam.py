# import requests
#
# # Substitua pelo IP do seu WLED
# WLED_IP = "http://wled-0238c8.local"
#
# def ligar_led():
#     url = f"{WLED_IP}/json/state"
#     payload = {"on": True}  # True para ligar, False para desligar
#     requests.post(url, json=payload)
#
# def desligar_led():
#     url = f"{WLED_IP}/json/state"
#     payload = {"on": False}
#     requests.post(url, json=payload)
#
# def setar_cor_vermelho():
#     url = f"{WLED_IP}/json/state"
#     payload = {
#         "on": True,
#         "bri": 128,  # Brilho (0-255)
#         "seg": [{"col": [[255, 0, 0]]}]  # Vermelho
#     }
#     requests.post(url, json=payload)
#
#
# while True:
#     print("1 - Ligar LED // 2 - Desligar LED // Else - Sair")
#     i = int(input())
#     if i == 1:
#         setar_cor_vermelho()
#     elif i == 2:
#         desligar_led()
#     else:
#         break

import asyncio
from wled import WLED

async def main():
    async with WLED("wled-0238c8.local") as led:  # Troque pelo IP do seu WLED
        await led.master(on=True)  # Liga o LED
        await led.master(brightness=128)  # Define brilho em 50%
        await asyncio.sleep(5)  # Espera 5 segundos
        await led.master(on=False)  # Desliga o LED

asyncio.run(main())

