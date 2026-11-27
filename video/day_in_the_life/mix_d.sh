#!/bin/bash
# voice.wav (mono, levelled per line) + amb.wav (natural sound, low) + music.wav + sfx.wav -> mix.wav (stereo master)
# Music lows stay up, music mids duck under the voice. env: MG music dB, SG effects dB, AG ambience dB, TARGET LUFS
TOTAL=$(python3 -c "import json;print(json.load(open('data.json'))['total']/30)")
MG=${MG:--9}; SG=${SG:--4}; AG=${AG:-0}; VG=${VG:-3}; TARGET=${TARGET:--14}
ffmpeg -v error -y -i voice.wav -i amb.wav -i music.wav -i sfx.wav -filter_complex "
[0:a]apad=whole_dur=$TOTAL,acompressor=threshold=-22dB:ratio=2.2:attack=6:release=160:makeup=1,volume=${VG}dB,asplit=3[v][k1][k2];
[v]pan=stereo|c0=c0|c1=c0[vs];
[1:a]apad=whole_dur=$TOTAL,volume=${AG}dB,pan=stereo|c0=c0|c1=c0[as];
[2:a]volume=${MG}dB,asplit=2[m1][m2];
[m1]lowpass=f=150:p=2,lowpass=f=150:p=2[ml];
[m2]highpass=f=150:p=2,highpass=f=150:p=2[mh0];[mh0][k1]sidechaincompress=threshold=0.015:ratio=4:attack=15:release=380:makeup=1:knee=4[mh];
[3:a]volume=${SG}dB[s0];[s0][k2]sidechaincompress=threshold=0.05:ratio=1.8:attack=10:release=220:makeup=1[sx];
[vs][as][ml][mh][sx]amix=inputs=5:normalize=0:duration=longest,alimiter=limit=0.95:level=false:attack=5:release=120[a]" -map "[a]" -ar 48000 -t $TOTAL premaster.wav
PL=$(ffmpeg -i premaster.wav -af ebur128 -f null - 2>&1 | grep "I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(($TARGET)-($PL),2))")
ffmpeg -v error -y -i premaster.wav -af "volume=${G}dB,alimiter=limit=0.84:level=false:attack=5:release=120,atrim=0:$TOTAL" -ar 48000 mix.wav
echo "premaster $PL LUFS, master gain $G dB"; ffmpeg -i mix.wav -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|LRA:|Peak:" | tail -3
