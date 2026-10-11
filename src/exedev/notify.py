"""Push notifications to the VM owner's devices.

https://notify.int.exe.xyz/
"""

import json
import urllib.request

URL = "https://notify.int.exe.xyz/"


def send(title: str, body: str) -> None:
    request = urllib.request.Request(
        URL,
        data=json.dumps({"title": title, "body": body}).encode(),
        headers={"Content-Type": "application/json"},
    )
    urllib.request.urlopen(request).close()
