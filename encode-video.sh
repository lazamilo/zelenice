#!/bin/sh
# Trims each source clip in source/video (sorted by name) to 3.4s and encodes
# H.264 1080p MP4 with fast-start into site/assets/video/hero-N.mp4.
# Uses macOS's built-in avconvert (no ffmpeg needed).
# Usage: sh encode-video.sh [start-seconds]   (default start 1.0s into each clip)
cd "$(dirname "$0")" || exit 1
START="${1:-1.0}"
mkdir -p site/assets/video
n=1
for f in source/video/*; do
  [ -f "$f" ] || continue
  out="site/assets/video/hero-$n.mp4"
  echo "[$n] $f -> $out"
  avconvert --source "$f" --preset Preset1920x1080 --output "$out" --start "$START" --duration 3.4 --replace
  n=$((n + 1))
done
ls -lh site/assets/video
