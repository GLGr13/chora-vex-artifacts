#!/usr/bin/env bash
set -euo pipefail

REPO=/root/chora-vex-artifacts
SRC=/opt/chora-gate-v0.3
TMP=/tmp/chora_sync_stage

mkdir -p "$TMP"
test -d "$REPO/.git"

mkdir -p \
  "$REPO/docs" \
  "$REPO/docs/specs" \
  "$REPO/docs/architecture" \
  "$REPO/docs/tracker" \
  "$REPO/artifacts/specimen-capsules" \
  "$REPO/artifacts/reference-bundles" \
  "$REPO/artifacts/keys" \
  "$REPO/scripts"

cp -f "$SRC/docs/"*.md "$REPO/docs/" 2>/dev/null || true
cp -f "$SRC/tracker/STATUS.md" "$REPO/docs/tracker/STATUS.md" 2>/dev/null || true
cp -f "$SRC/tracker/progress.json" "$REPO/docs/tracker/progress.json" 2>/dev/null || true

if [ -f /tmp/capsule.json ]; then
  CAP_ID="$(jq -r '.capsule_id // empty' /tmp/capsule.json)"
  if [ -n "${CAP_ID}" ]; then
    cp -f /tmp/capsule.json "$REPO/artifacts/specimen-capsules/capsule_${CAP_ID}.json"
  fi
fi

if [ -f /tmp/chora_canonical_capsule_reference_20260319T0838Z.tar.gz ]; then
  cp -f /tmp/chora_canonical_capsule_reference_20260319T0838Z.tar.gz \
    "$REPO/artifacts/reference-bundles/"
fi

curl -s https://gate.choragate.network/public_key \
  > "$REPO/artifacts/keys/chora_dev_public_key.pem"

git -C "$REPO" add docs/ artifacts/ scripts/
git -C "$REPO" commit -m "Sync repo from VPS runtime state" || true
git -C "$REPO" push origin main
