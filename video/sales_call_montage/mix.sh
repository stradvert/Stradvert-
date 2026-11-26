#!/bin/bash
# voice (mono, from cut.mov) + music + sfx -> stereo master. Music lows are left un-ducked (weight), mids duck under the voice.
TOTAL=$(python3 -c "import json;print(json.load(open('data.json'))['total']/30)")
MG=${MG:--7}; ML=${ML:-3}; SG=${SG:--3}; VG=${VG:-0}; TARGET=${TARGET:--15}
ffmpeg -v error -y -i cut.mov -vn -af "apad=whole_dur=$TOTAL,atrim=0:$TOTAL" -ar 48000 -ac 1 voice_raw.wav
ffmpeg -v error -y -i voice_raw.wav -af "acompressor=threshold=-24dB:ratio=2.2:attack=6:release=160:makeup=2.5,alimiter=limit=0.9:level=false" voice_c.wav
VL=$(ffmpeg -i voice_c.wav -af ebur128 -f null - 2>&1 | grep "I:" | tail -1 | awk '{print $2}')
VGAIN=$(python3 -c "print(round(-16.5-($VL)+($VG),2))")
ffmpeg -v error -y -i voice_c.wav -i music.wav -i sfx.wav -filter_complex "
[0:a]volume=${VGAIN}dB,asplit=3[v][k1][k2];
[v]pan=stereo|c0=c0|c1=c0[vs];
[1:a]volume=${MG}dB,asplit=2[m1][m2];
[m1]lowpass=f=160:p=2,lowpass=f=160:p=2,volume=${ML}dB[ml];
[m2]highpass=f=160:p=2,highpass=f=160:p=2[mh0];[mh0][k1]sidechaincompress=threshold=0.02:ratio=3.5:attack=18:release=420:makeup=1:knee=4[mh];
[2:a]volume=${SG}dB,asplit=2[s1][s2];
[s1]lowpass=f=200:p=2[sl];[s2]highpass=f=200:p=2[sh0];[sh0][k2]sidechaincompress=threshold=0.05:ratio=1.6:attack=10:release=220:makeup=1[sh];
[vs][ml][mh][sl][sh]amix=inputs=5:normalize=0:duration=longest,alimiter=limit=0.95:level=false:attack=5:release=120[a]" -map "[a]" -ar 48000 premaster.wav
PL=$(ffmpeg -i premaster.wav -af ebur128 -f null - 2>&1 | grep "I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(($TARGET)-($PL),2))")
ffmpeg -v error -y -i premaster.wav -af "volume=${G}dB,alimiter=limit=0.89:level=false:attack=5:release=120,atrim=0:$TOTAL" -ar 48000 mix.wav
echo "voice $VL LUFS (+$VGAIN dB), premaster $PL LUFS, master gain $G dB"; ffmpeg -i mix.wav -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|LRA:|Peak:" | tail -3
