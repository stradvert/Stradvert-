#!/bin/bash
# blend sub-frames -> finishing pass (bloom, halation, lens softness, grain) -> H.264 with the stereo master
OUT=${1:-/home/user/Stradvert-/video_out/sales_call_montage_premium_v3.mp4}; CRF=${CRF:-19}; GRAIN=${GRAIN:-5}
NF=$(python3 -c "import json;print(json.load(open('data.json'))['total'])")
python3 blend.py 0 $NF
POST="format=gbrp,split=3[base][b1][b2];[b1]curves=all='0/0 0.5/0 0.78/0.42 1/1',gblur=sigma=20:steps=2[bl1];[b2]curves=all='0/0 0.66/0 1/1',gblur=sigma=64:steps=2,colorchannelmixer=rr=1:gg=0.86:bb=0.6[bl2];[base][bl1]blend=all_mode=screen:all_opacity=0.40[m1];[m1][bl2]blend=all_mode=screen:all_opacity=0.30[m2];[m2]rgbashift=rh=-1:bh=1:edge=smear,gblur=sigma=0.5,noise=alls=${GRAIN}:allf=t,scale=1920:1080:in_range=pc:out_range=tv:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=yuv420p[v]"
ffmpeg -v error -y -framerate 30 -i out/%05d.png -i mix.wav -filter_complex "[0:v]$POST" -map "[v]" -map 1:a -c:v libx264 -preset slow -crf $CRF -profile:v high -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -r 30 -c:a aac -b:a 256k -movflags +faststart -shortest "$OUT"
ffprobe -v error -show_entries format=duration,size,bit_rate:stream=codec_name,width,height,r_frame_rate,channels,color_space -of compact "$OUT"
