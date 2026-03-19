import fs from "fs";
import crypto from "crypto";

const token = JSON.parse(fs.readFileSync("token.json", "utf8"));
const payload = token.payload;
const signature = Buffer.from(token.signature, "hex");

const canonical = JSON.stringify(
  Object.keys(payload).sort().reduce((o, k) => (o[k] = payload[k], o), {}),
);

const pubKey = crypto.createPublicKey(fs.readFileSync("public_key_token.pem"));

const ok = crypto.verify(
  null,
  Buffer.from(canonical, "utf8"),
  pubKey,
  signature
);

console.log(ok ? "NODE: SIGNATURE VALID" : "NODE: SIGNATURE INVALID");
