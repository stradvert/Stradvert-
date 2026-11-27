#!/bin/bash
# voice.wav (mono, levelled per line, natural sound included) + music.wav + sfx.wav -> mix.wav
# Music lows stay up, music mids duck under the voice; effects duck a little. env: MG music dB, SG effects dB, VG voice dB, TARGET LUFS
TOTAL=$(python3 -c "import json;print(json.load(open('data.json'))['total']/30)")
MG=${MG:--12}; SG=${SG:--6}; VG=${VG:-2}; TARGET=${TARGET:--14}
ffmpeg -v error -y -i voice.wav -i music.wav -i sfx.wav -filter_complex "
[0:a]apad=whole_dur=$TOTAL,volume=${VG}dB,asplit=3[v][k1][k2];
[v]pan=stereo|c0=c0|c1=c0[vs];
[1:a]volume=${MG}dB,asplit=2[m1][m2];
[m1]lowpass=f=160:p=2,lowpass=f=160:p=2[ml];
[m2]highpass=f=160:p=2,highpass=f=160:p=2[mh0];[mh0][k1]sidechaincompress=threshold=0.02:ratio=5:attack=12:release=300:makeup=1:knee=4[mh];
[2:a]volume=${SG}dB[s0];[s0][k2]sidechaincompress=threshold=0.06:ratio=1.6:attack=8:release=200:makeup=1[sx];
[vs][ml][mh][sx]amix=inputs=4:normalize=0:duration=longest,alimiter=limit=0.95:level=false:attack=4:release=100[a]" -map "[a]" -ar 48000 -t $TOTAL premaster.wav
PL=$(ffmpeg -i premaster.wav -af ebur128 -f null - 2>&1 | grep "I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(($TARGET)-($PL),2))")
ffmpeg -v error -y -i premaster.wav -af "volume=${G}dB,alimiter=limit=0.76:level=false:attack=4:release=100,atrim=0:$TOTAL" -ar 48000 mix.wav
echo "premaster $PL LUFS, master gain $G dB"; ffmpeg -i mix.wav -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|LRA:|Peak:" | tail -3
