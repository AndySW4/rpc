const dgram = require('unix-dgram');
const fs = require('fs');

const server_address = "./rpc_server.sock";
const client_address = "./rpc_client.sock";

if (fs.existsSync(client_address)) {
  fs.unlinkSync(client_address);
}

const client = dgram.createSocket('unix_dgram');
client.bind(client_address);

const request = {
  method: "floor",
  params: [3.7],
  id: 1
};

const message = Buffer.from(JSON.stringify(request));

client.on('message', (msg, rinfo) => {
  console.log(`[*] Received response: ${msg.toString()}`);
  try {
    const resp = JSON.parse(msg.toString());
    if (resp.error) {
      console.error("[!] RPC Error:", resp.error);
    } else {
      console.log(`[+] RPC Result for id=${resp.id}:`, resp.results);
    }
  } catch (e) {
    console.error("[!] Failed to parse response:", e);
  }
  client.close();
});

client.on('error', (err) => {
  console.error("[!] Client Socket Error:", err);
  client.close();
});

client.send(message, 0, message.length, server_address, (err) => {
  if (err) {
    console.error("[!] Error sending:", err);
    client.close();
  } else {
    console.log("[*] Message sent to server");
  }
});
