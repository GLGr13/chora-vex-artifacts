import fs from "fs";
import crypto from "crypto";
import canonicalize from "canonicalize";

const token = JSON.parse(fs.readFileSync("token.json", "utf8"));
const pubPem = fs.readFileSync("public_key_token.pem", "utf8");

const payloadBytes = Buffer.from(canonicalize(token.payload), "utf8");
const sig = Buffer.from(token.signature, "hex");

const ok = crypto.verify(null, payloadBytes, pubPem, sig);

if (!ok) {
  console.error("NODE: SIGNATURE INVALID");
  process.exit(1);
}

console.log("NODE: SIGNATURE VALID");
