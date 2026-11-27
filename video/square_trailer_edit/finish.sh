#!/bin/bash
# blend sub-frames -> finishing pass (bloom, halation, lens softness, grain) -> H.264 with the stereo master (1080x1920 canvas)
# bloom thresholds here are set for bright daylight footage (higher threshold, lower opacity than the dark call edit) so skies keep their detail
OUT=${1:-out.mp4}; CRF=${CRF:-19}; GRAIN=${GRAIN:-5}
NF=$(python3 -c "import json;print(json.load(open('data.json'))['total'])")
python3 blend.py 0 $NF
POST="format=gbrp,colorchannelmixer=rr=1.0472:rg=-0.0429:rb=-0.0043:gr=-0.0128:gg=1.0171:gb=-0.0043:br=-0.0128:bg=-0.0429:bb=1.0557,split=3[base][b1][b2];[b1]curves=all='0/0 0.72/0 0.9/0.35 1/1',gblur=sigma=18:steps=2[bl1];[b2]curves=all='0/0 0.8/0 1/1',gblur=sigma=56:steps=2,colorchannelmixer=rr=1:gg=0.86:bb=0.6[bl2];[base][bl1]blend=all_mode=screen:all_opacity=0.26[m1];[m1][bl2]blend=all_mode=screen:all_opacity=0.20[m2];[m2]rgbashift=rh=-1:bh=1:edge=smear,gblur=sigma=0.5,noise=alls=${GRAIN}:allf=t,scale=1080:1920:in_range=pc:out_range=tv:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=yuv420p[v]"
ffmpeg -v error -y -framerate 30 -i out/%05d.png -i mix.wav -filter_complex "[0:v]$POST" -map "[v]" -map 1:a -c:v libx264 -preset slow -crf $CRF -profile:v high -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -r 30 -c:a aac -b:a 256k -movflags +faststart -shortest "$OUT"
ffprobe -v error -show_entries format=duration,size,bit_rate:stream=codec_name,width,height,r_frame_rate,channels,color_space -of compact "$OUT"
