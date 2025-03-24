import socket
import os
import json
import math


server_address = './rpc_server.sock'


def rpc_floor(x: float) -> int:
    return math.floor(x)

rpc_methods = {
    'floor': rpc_floor
}

def handle_request(req_str: str) -> dict:

    try:
        request = json.loads(req_str)
    except json.JSONDecodeError:
        return {
            'results': None,
            'error' : 'Invalid JSON',
            'id' : None
        }
    
    method = request.get("method")
    params = request.get("params", [])
    request_id = request.get("id")

    response = {
        "results": None,
        "error": None,
        "id": request_id
    }

    if method not in rpc_methods:
        response["error"] = f"Method '{method}' not found."
        return response

    try:
        func = rpc_methods[method]
        result = func(*params)
        response["results"] = result
    except Exception as e:
        response["error"] = str(e)

    return response

def main():
    if os.path.exists(server_address):
        os.remove(server_address)

    server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    server_sock.bind(server_address)

    print(f"[*] RPC Server (AF_UNIX + SOCK_DGRAM) listening on: {server_address}")
    
    try:
        while True:
            data, client_addr = server_sock.recvfrom(65535)
            if not data:
                continue
            response_dict = handle_request(data.decode("utf-8"))
            response_data = json.dumps(response_dict).encode("utf-8")
            server_sock.sendto(response_data, client_addr)
    finally:
        server_sock.close()
        if os.path.exists(server_address):
            os.remove(server_address)

if __name__ == "__main__":
    main()