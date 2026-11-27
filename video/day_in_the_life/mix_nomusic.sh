#!/bin/bash
# No score: voice.wav (levelled per line) + amb.wav (natural sound, the bed) + sfx.wav -> mix.wav (stereo master).
# Loudness is set from the speech, so quiet stretches stay quiet instead of being pumped up. env: SG effects dB, AG natural sound dB, SPEECH target LUFS for the spoken parts
TOTAL=$(python3 -c "import json;print(json.load(open('data.json'))['total']/30)")
SG=${SG:--13.5}; AG=${AG:--6.5}; SPEECH=${SPEECH:--13.5}
ffmpeg -v error -y -i voice.wav -i amb.wav -i sfx.wav -filter_complex "
[0:a]apad=whole_dur=$TOTAL,acompressor=threshold=-22dB:ratio=2.2:attack=6:release=160:makeup=1,asplit=2[v][k];
[v]pan=stereo|c0=c0|c1=c0[vs];
[1:a]apad=whole_dur=$TOTAL,volume=${AG}dB,pan=stereo|c0=c0|c1=c0[as];
[2:a]volume=${SG}dB[s0];[s0][k]sidechaincompress=threshold=0.05:ratio=1.8:attack=10:release=220:makeup=1[sx];
[vs][as][sx]amix=inputs=3:normalize=0:duration=longest[a]" -map "[a]" -ar 48000 -t $TOTAL premaster.wav
G=$(python3 - <<'P'
import json,wave,numpy as np,subprocess,re
J=json.load(open('segs.json'));w=wave.open('premaster.wav');sr=w.getframerate();ch=w.getnchannels();a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).reshape(-1,ch)
parts=[a[int(v['t0']*sr):int(v['t1']*sr)] for v in J['voice']];x=np.concatenate(parts)
o=wave.open('speech_only.wav','w');o.setnchannels(ch);o.setsampwidth(2);o.setframerate(sr);o.writeframes(x.tobytes());o.close()
r=subprocess.run(['ffmpeg','-i','speech_only.wav','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
print(re.findall(r'I:\s+(-?[\d.]+) LUFS',r)[-1])
P
)
GAIN=$(python3 -c "print(round(($SPEECH)-($G),2))")
ffmpeg -v error -y -i premaster.wav -af "volume=${GAIN}dB,alimiter=limit=0.84:level=false:attack=5:release=120,atrim=0:$TOTAL" -ar 48000 mix.wav
echo "speech in premaster $G LUFS, master gain $GAIN dB"; ffmpeg -i mix.wav -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|LRA:|Peak:" | tail -3
