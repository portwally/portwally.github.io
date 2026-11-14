#!/bin/sh
# render.sh: the box's faces (box.html) to front.jpg, back.jpg, spine.jpg
# and top.jpg, with headless Chrome and sips
cd "$(dirname "$0")" || exit 1
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
shot() {   # face width height
  "$CHROME" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --window-size=$2,$3 --virtual-time-budget=6000 --screenshot="$PWD/$1.png" "file://$PWD/box.html?face=$1" 2>/dev/null
  sips -s format jpeg -s formatOptions 84 "$1.png" --out "$1.jpg" > /dev/null && rm "$1.png"
}
shot front 900 1180
shot back 900 1180
shot spine 170 1180
shot top 900 170
