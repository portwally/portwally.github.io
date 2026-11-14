#!/usr/bin/env bash
# Runs the two footer checks of .github/workflows/check-cross-links.yml locally,
# using the very same shell code (extracted from the workflow), so it can never
# drift from CI. Run from the repo root:  .github/check-footers.sh
set -u
cd "$(dirname "$0")/.."
WF=.github/workflows/check-cross-links.yml
export GITHUB_STEP_SUMMARY=/dev/null
rc=0
for step in "Verify Fire footer matches root index" "Report drift in every sub-app's footer"; do
  echo "=== $step"
  awk -v name="$step" '
    index($0, "- name: " name) { found=1; next }
    found && /run: \|/ { grab=1; next }
    grab { if ($0 ~ /^          / || $0 ~ /^$/) { sub(/^          /, ""); print } else exit }
  ' "$WF" > /tmp/footer-step.sh
  bash /tmp/footer-step.sh || rc=1
done
[ $rc -eq 0 ] && echo "ALL FOOTER CHECKS PASS" || echo "FOOTER CHECKS FAILED"
exit $rc
