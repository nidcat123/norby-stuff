#!/usr/bin/python

import sys
import base64
import json
from io import BytesIO
from norby_binary import NorbyBinary


def bytes2list(d):
    for key in d:
        if isinstance(d[key], bytes):
            d[key] = list(d[key])


def get_header(norby_packet):
    packet = norby_packet.header.__dict__.copy()
    del packet["_io"]
    del packet["_parent"]
    del packet["_root"]
    bytes2list(packet)
    return packet


def get_payload(norby_packet):
    if isinstance(norby_packet.payload, bytes):
        raw = {"raw": norby_packet.payload}
        bytes2list(raw)
        return raw

    packet = norby_packet.payload.__dict__.copy()
    del packet["_io"]
    del packet["_parent"]
    del packet["_root"]
    bytes2list(packet)
    return packet


def decode(packet_base64):
    base64_bytes = packet_base64.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    packet_io = BytesIO(message_bytes)
    return NorbyBinary(packet_io)


def main(argv):
    if len(argv) < 1:
        print('{"error": "Invalid arguments"}')
        return 1

    try:
        norby_packet = decode(argv[0])
    except Exception as e:
        print('{"error":"' + str(e) + '"}')
        return 1

    parsed_packet = {
        "header": get_header(norby_packet),
        "payload": get_payload(norby_packet)
    }
    if "raw" in parsed_packet["payload"]:
        parsed_packet["telemetry"] = False
    else:
        parsed_packet["telemetry"] = True

    print(json.dumps(parsed_packet))
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
