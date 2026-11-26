#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARCHIFY_SKILL_DIR="${ARCHIFY_SKILL_DIR:-${HOME}/.agents/skills/archify}"
ARCHIFY_BIN="${ARCHIFY_SKILL_DIR}/bin/archify.mjs"
EXPORT_SVG_BIN="${ARCHIFY_SKILL_DIR}/bin/export-svg.mjs"

if [[ ! -f "${ARCHIFY_BIN}" || ! -f "${EXPORT_SVG_BIN}" ]]; then
  echo "Archify skill not found under ${ARCHIFY_SKILL_DIR}" >&2
  exit 1
fi

if [[ -z "${ARCHIFY_CHROME:-}" ]]; then
  for candidate in google-chrome chromium chromium-browser; do
    if command -v "${candidate}" >/dev/null 2>&1; then
      ARCHIFY_CHROME="$(command -v "${candidate}")"
      break
    fi
  done
fi

if [[ -z "${ARCHIFY_CHROME:-}" ]]; then
  latest_pw_chrome="$(ls -1d "${HOME}"/.cache/ms-playwright/chromium-*/chrome-linux64/chrome 2>/dev/null | sort -V | tail -n 1 || true)"
  if [[ -n "${latest_pw_chrome}" && -x "${latest_pw_chrome}" ]]; then
    ARCHIFY_CHROME="${latest_pw_chrome}"
  fi
fi

if [[ -n "${ARCHIFY_CHROME:-}" ]]; then
  export ARCHIFY_CHROME
fi

cd "${REPO_ROOT}"

SPECS=(
  "architecture:workflow-overview"
  "architecture:intake-and-layers"
  "tree:herdr-hierarchy"
  "workflow:pr-ci-hitl-loop"
)

mkdir -p .archify assets
assets_dir="${REPO_ROOT}/assets"

for spec in "${SPECS[@]}"; do
  type="${spec%%:*}"
  stem="${spec#*:}"
  json_path="docs/diagrams/${stem}.${type}.json"
  html_path=".archify/${stem}.html"
  out_dir=".archify/render-${stem}"

  echo "Finalizing ${json_path} (${type})..."
  rm -rf "${REPO_ROOT}/.archify/${stem:?}.html" \
         "${REPO_ROOT}/.archify/${stem:?}.delivery.json" \
         "${REPO_ROOT}/.archify/${stem:?}.delivery-pending.json" \
         "${REPO_ROOT}/.archify/${stem:?}.browser-check.json" \
         "${REPO_ROOT}/.archify/${stem:?}.finalize.json" \
         "${REPO_ROOT}/.archify/${stem:?}.finalize-summary.json" \
         "${REPO_ROOT}/.archify/render-${stem:?}"

  node "${ARCHIFY_BIN}" finalize "${type}" "${json_path}" "${html_path}" \
    --out-dir "${out_dir}" \
    --quality showcase \
    --json >/dev/null

  for theme in dark light; do
    rm -f "${assets_dir:?}/${stem:?}-${theme:?}.svg"
    node "${EXPORT_SVG_BIN}" "${html_path}" "assets/${stem}-${theme}.svg" "${theme}"
  done
done
