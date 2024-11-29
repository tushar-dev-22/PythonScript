import asyncio
import logging
import websockets
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Setup logging
logging.basicConfig(level=logging.DEBUG)

def get_evosessionid():
    driver_path = "/home/developer/Desktop/chromedriver-linux64/chromedriver"  
    
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Use Service to specify the path to ChromeDriver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://a8r.evo-games.com/")
        print("Please log in manually in the browser...")

        time.sleep(60)  
        
        cookies = driver.get_cookies()
        evosessionid = None

        print(f"All Cookies: {cookies}") 

        # Look for the EVOSESSIONID cookie
        for cookie in cookies:
            if cookie['name'] == 'EVOSESSIONID':
                print('here in the code')
                evosessionid = cookie['value']

                print(evosessionid,'--------------id')
                break

        if evosessionid:
            print(f"EVOSESSIONID: {evosessionid}")
        else:
            print("EVOSESSIONID not found.")
        
        return evosessionid

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

evosessionid = get_evosessionid()

# Constants
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
et = evosessionid

async def ping_server(websocket):
    """
    Send a WebSocket ping every 30 seconds to keep the connection alive.
    """
    while True:
        await asyncio.sleep(30)
        try:
            logging.debug("Sending WebSocket ping.")
            await websocket.ping()
        except websockets.ConnectionClosed:
            logging.error("Connection closed during ping.")
            break

async def connect_to_websocket():
    websocket_url = f"wss://a8r.evo-games.com/public/lobby/socket/v2/r7fi6s7bhypackls?messageFormat=json&device=Desktop&EVOSESSIONID={et}&client_version=6.20241031.15158.46131-76f9419919"

    headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "Upgrade",
        "Cookie": f"lang=en; locale=en-GB; EVOSESSIONID={et}",
        "Host": "a8r.evo-games.com",
        "Origin": "https://a8r.evo-games.com",
        "Pragma": "no-cache",
        "Sec-GPC": "1",
        "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
        "Sec-WebSocket-Key": "1ZPjloGTra4f8yYQnWOzHA==",
        "Sec-WebSocket-Version": "13",
        "Upgrade": "websocket",
        "User-Agent": ua
    }

    # headers = {
    #     "User-Agent": ua,
    #     "Cookie": f"lang=en; locale=en-GB; EVOSESSIONID={et}",
    #     "Origin": "https://a8r.evo-games.com",
    #     "Upgrade": "websocket"
    # }

    while True:
        try:
            async with websockets.connect(websocket_url, extra_headers=headers) as websocket:
                logging.info("Connected to WebSocket")

                asyncio.create_task(ping_server(websocket))

                # Initial messages to send
                messages = [
                    {"id": "h6da5v4752", "type": "lobby.initLobby", "args": {"version": 2, "features": ["opensAt", "multipleHero", "shortThumbnails", "skipInfosPublished"]}},
                    {"id": "min4yeqevb", "type": "lobby.appEvent", "args": {"type": "CLIENT_SOCKET_CONNECTION_ESTABLISHED", "value": {"userAgent": ua, "currency": "$", "channel": "PCMac", "gameType": "lobby", "inGame": True, "orientation": "landscape", "reconnectionCount": 0}}},
                ]

                for message in messages:
                    logging.debug(f"Sent: {json.dumps(message)}")
                    await websocket.send(json.dumps(message))
                    response = await websocket.recv()
                    logging.debug(f"Received: {response}")

                while True:
                    response = await websocket.recv()
                    try:
                        data = json.loads(response)
                        logging.debug(f"Received: {json.dumps(data, indent=2)}")
                        # Add your event handling logic here

                    except json.JSONDecodeError:
                        logging.error("Failed to decode WebSocket message: %s", response)
                        continue
                    except KeyError as e:
                        logging.error("KeyError while processing WebSocket message: %s", str(e))
                        continue

        except websockets.exceptions.ConnectionClosedError as e:
            logging.error(f"WebSocket closed with error: {e}")
        except websockets.exceptions.WebSocketException as ws_e:
            logging.error(f"WebSocket connection exception occurred: {ws_e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        logging.info("Reconnecting in 5 seconds...")
        await asyncio.sleep(5)

asyncio.run(connect_to_websocket())
