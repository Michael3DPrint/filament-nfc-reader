#!/bin/sh
# Definition of done for this repository. Exit 0 only when every step ran and passed.
# A step that cannot run is a failure, never a pass.
set -eu
cd "$(dirname "$0")/.."

echo "== standards (docs, ledger, line limit, secrets)"
python3 -I scripts/check_standards.py

echo "== README names keys, not line numbers"
if grep -nEi '\blines? [0-9]' README.md hardware/case/README.md docs/*.md; then
  echo "FAIL: cite a key or a search string instead of a line number (line numbers go stale)"; exit 1
fi

echo "== every API path in the firmware is in docs/API.md"
missing=0
for path in $(grep -o '/api/v1/[A-Za-z0-9_/-]*' esphome/filament-selector.yaml | sed 's:/*$::' | sort -u); do
  if ! grep -qF -- "$path" docs/API.md; then echo "FAIL: $path is used by the firmware but not in docs/API.md"; missing=1; fi
done
[ "$missing" = 0 ] || exit 1

echo "== every result message and CHANGE ME key in the firmware is in the README"
python3 -I - <<'PY'
import re, sys
yaml = open("esphome/filament-selector.yaml").read()
readme = open("README.md").read()
problems = []
for m in sorted(set(re.findall(r'"((?:Lookup failed|Assign failed|Assigned to|Unknown tag)[^"]*)"', yaml))):
    msg = m.split("\\n")[0].rstrip(" :")
    if msg and msg not in readme:
        problems.append(f"message '{msg}' is shown by the firmware but missing from the README message table")
for line in yaml.splitlines():
    if "CHANGE ME" in line:
        key = re.match(r"\s*([A-Za-z_]+):", line)
        if key and f"`{key.group(1)}`" not in readme:
            problems.append(f"CHANGE ME key '{key.group(1)}' is missing from the README")
if problems:
    print("\n".join("FAIL: " + p for p in problems)); sys.exit(1)
PY

echo "== secrets.yaml is not tracked"
if git ls-files --error-unmatch esphome/secrets.yaml >/dev/null 2>&1; then
  echo "FAIL: esphome/secrets.yaml is tracked"; exit 1
fi

echo "== esphome config (offline validation, dummy secrets)"
ESPHOME_CMD="${ESPHOME_BIN:-$(command -v esphome || true)}"
if [ -z "$ESPHOME_CMD" ]; then
  echo "FAIL: esphome not found (install it, or set ESPHOME_BIN). Not run is not clean."; exit 1
fi
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cp esphome/filament-selector.yaml "$tmp/"
cat > "$tmp/secrets.yaml" <<SEC
wifi_ssid: "dummy-network"
wifi_password: "dummy-password-123"
api_encryption_key: "$(python3 -I -c 'import base64;print(base64.b64encode(bytes(range(32))).decode())')"
ap_password: "dummy-fallback-123"
bambuddy_api_key: "dummy-key"
SEC
(cd "$tmp" && "$ESPHOME_CMD" config filament-selector.yaml > /dev/null)
echo "All checks passed."
