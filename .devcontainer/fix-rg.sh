#!/usr/bin/env bash
RG="$(command -v rg)" || exit 0

for root in "$HOME"/.vscode-server/bin/*; do
  [ -d "$root/node_modules" ] || continue
  for sub in "@vscode/ripgrep/bin" "vscode-ripgrep/bin"; do
    d="$root/node_modules/$sub"
    sudo mkdir -p "$d" && sudo ln -sf "$RG" "$d/rg"
  done
done

exit 0