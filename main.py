import asyncio
import json
import os

import pyinotify
from aiomqtt import Client
from aiomqtt.error import MqttConnectError
from dotenv import load_dotenv

from async_debouncer import AsyncDebouncer
from event_handler import EventHandler
from logger import Logger

load_dotenv()
logger = Logger.setup_logger()


async def notification_callback(mqtt_client, topic):
    async def handle_settled_value(value: bool):
        logger.info(f"Settled value: {value}")
        await mqtt_client.publish(topic, json.dumps({"state": "on" if value else "off"}), qos=1)

    return handle_settled_value


async def main(loop):
    username = os.getenv('MQTT_USERNAME')
    password = os.getenv('MQTT_PASSWORD')
    host = os.getenv('MQTT_HOST')
    async with Client(client_id='webcam_ha_sensor', hostname=host, username=username, password=password) as mqtt_client:
        topic = "homeassistant/binary_sensor/webcam_ha_sensor"
        callback = await notification_callback(mqtt_client, topic)
        await callback(False)
        debouncer = AsyncDebouncer(settle_time=0.5, callback=callback)
        watch_manager = pyinotify.WatchManager()
        mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_OPEN
        handler = EventHandler(debouncer, loop, mqtt_client, topic)
        notifier = pyinotify.AsyncioNotifier(watch_manager, loop, default_proc_fun=handler)

        watch_manager.add_watch('/dev', mask, rec=True)

        try:
            logger.info("Watching for file changes...")
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping watch.")
        finally:
            await callback(False)
            notifier.stop()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
    except MqttConnectError as ex:
        logger.error("A MqttConnectError occurred, check that MQTT has been correctly configured via the MQTT_HOST, " \
                     "MQTT_USERNAME, MQTT_PASSWORD environment variables.")
        logger.error(ex, exc_info=True)
    except KeyboardInterrupt:
        pass
