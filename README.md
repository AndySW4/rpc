# RPC over Unix Domain Sockets practice program

**Server (Python)**:
- Listens on `./rpc_server.sock`.
- Expects JSON requests: `{ "method": "floor", "params": [3.7], "id": 1 }`.
- Calls `math.floor` for the `floor` method and returns JSON responses.

**Client (Node.js)**:
- Sends a JSON request via `./rpc_client.sock` using `unix-dgram`.
- Receives and logs the JSON response.

## Usage

1. **Server**:  
   ```bash
   python RPC.py
   ```
2. **Client**:  
   ```bash
   node RPC_client.js
   ```
