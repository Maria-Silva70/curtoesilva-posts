set -e
D=(2.6 3.6 3.6 3.6 3.8 4.8)
F=0.4
args=""; fc=""
for i in 0 1 2 3 4 5; do
  n=$((i+1)); d=${D[$i]}; fr=$(python3 -c "print(int($d*30))")
  args="$args -i $n.jpg"
  fc="$fc[$i:v]split[a$i][b$i];"
  fc="$fc[b$i]crop=1080:1272:0:0,scale=2160:-1,zoompan=z='1+0.04*on/$fr':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$fr:s=1080x1272:fps=30[fg$i];"
  fc="$fc[a$i]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:2,eq=brightness=-0.25,loop=loop=$fr:size=1,fps=30,trim=end_frame=$fr[bg$i];"
  fc="$fc[bg$i][fg$i]overlay=0:300,format=yuv420p,setsar=1,setpts=PTS-STARTPTS[v$i];"
done
prev=v0; off=0
for i in 1 2 3 4 5; do
  off=$(python3 -c "print(round($off+${D[$((i-1))]}-$F,3))")
  fc="$fc[$prev][v$i]xfade=transition=fade:duration=$F:offset=$off[x$i];"; prev=x$i
done
fc="${fc%;}"
ffmpeg -v error -y $args -filter_complex "$fc" -map "[$prev]" -r 30 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -movflags +faststart /home/claude/tmp/serie-ep1-reel.mp4
