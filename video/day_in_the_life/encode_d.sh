#!/bin/bash
# out/%05d.jpg + mix.wav -> finished portrait mp4
OUT=${1:-out.mp4}
ffmpeg -v error -y -framerate 30 -i out/%05d.jpg -i mix.wav -vf "scale=1080:1920:in_range=pc:out_range=tv:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=yuv420p" -c:v libx264 -preset slow -crf ${CRF:-20} -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -r 30 -c:a aac -b:a 256k -movflags +faststart -shortest "$OUT"
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,channels -of compact "$OUT"
ffmpeg -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
