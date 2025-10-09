import asyncio
from bleak import BleakClient, BleakScanner

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

async def main():
    print("Scanning...")
    devices = await BleakScanner.discover(timeout=10.0)
    target = next((d for d in devices if d.name and "NanoESP32-BLE" in d.name), None)
    if not target:
        print("Device not found.")
        return

    async with BleakClient(target.address) as client:
        print("Connected to", target.name)

        def handle_notify(sender, data):
            print("ESP32 ->", data.decode(errors='ignore'))

        await client.start_notify(CHAR_UUID, handle_notify)

        while True:
            msg = input("Python -> ESP32: ")
            if msg.lower() in ["exit", "quit"]:
                break
            await client.write_gatt_char(CHAR_UUID, msg.encode(), response=False)


asyncio.run(main())
