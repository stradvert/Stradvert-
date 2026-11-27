#!/bin/bash
# out/%05d.jpg + voice (audio of cut.mov) + music.wav + sfx.wav  ->  finished portrait mp4
# usage: ./encode.sh /path/to/output.mp4     env: MUSIC (dB, default -11), SFX (dB, default -8), TARGET (LUFS, default -14), RNN (rnnoise model, optional)
OUT=${1:-out.mp4}; MUSIC=${MUSIC:--11}; SFX=${SFX:--8}; TARGET=${TARGET:--14}
TOTAL=$(python3 -c "import json;print(json.load(open('data.json'))['total']/30)")
DN=""; [ -n "$RNN" ] && DN="arnndn=m=${RNN}:mix=0.9,"
ffmpeg -v error -y -i cut.mov -vn -af "aresample=48000,pan=mono|c0=0.5*c0+0.5*c1,highpass=f=85,${DN}equalizer=f=300:t=q:w=1.0:g=-2.5,equalizer=f=4200:t=q:w=1.2:g=2.5,equalizer=f=9500:t=h:w=4000:g=1.5,deesser=i=0.25,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=140:makeup=2,apad=whole_dur=$TOTAL,atrim=0:$TOTAL" voice.wav
ffmpeg -v error -y -i voice.wav -i music.wav -i sfx.wav -filter_complex "
[0:a]asplit=2[v][k];
[1:a]volume=${MUSIC}dB[m0];[m0][k]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400:makeup=1[m];
[2:a]volume=${SFX}dB[s];
[v][m][s]amix=inputs=3:normalize=0:duration=longest,alimiter=limit=0.95:level=false[a]" -map "[a]" -ar 48000 premaster.wav
PL=$(ffmpeg -i premaster.wav -af ebur128 -f null - 2>&1 | grep "I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(($TARGET)-($PL),2))")
ffmpeg -v error -y -i premaster.wav -af "volume=${G}dB,alimiter=limit=0.89:level=false,atrim=0:$TOTAL" -ar 48000 mix.wav
ffmpeg -v error -y -framerate 30 -i out/%05d.jpg -i mix.wav -vf "scale=1080:1920:in_range=pc:out_range=tv:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=yuv420p" -c:v libx264 -preset slow -crf 18 -profile:v high -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -r 30 -c:a aac -b:a 192k -ac 2 -movflags +faststart -shortest "$OUT"
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate -of compact "$OUT"
ffmpeg -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
