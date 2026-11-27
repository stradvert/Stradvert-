# Cut list -> parts, cut.mov (picture + cleaned mono voice) and scenes.json. Edit S for each video: (scene key, [(start, end) in source seconds, ...]).
# Cut points snap to the quietest instant nearby so words are not clipped. Needs raw.mp4, dn16.wav (16k mono, denoised) and the rnnoise model.
import os,json,subprocess,wave,numpy as np
M=os.environ.get('MODELS','models')+'/'
os.makedirs('parts',exist_ok=True)
def run(*a):subprocess.run(list(a),check=True)
w=wave.open('dn16.wav');X=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768;SR=16000
def snap(t,win=0.045):
    best=None
    for d in np.arange(-win,win+0.001,0.005):
        c=t+d;s=X[int((c-0.012)*SR):int((c+0.012)*SR)];e=float(np.sqrt((s**2).mean()))
        if best is None or e<best[0]:best=(e,c)
    return round(float(best[1]),3)
S=[('hook',[(4.27,7.97)]),('reason',[(8.12,14.06)]),('proof',[(14.08,18.07),(19.31,20.36)]),('pave',[(20.95,22.64),(24.50,27.12)]),
('ugc',[(33.72,37.42),(38.50,40.94)]),('aiview',[(178.02,184.78)]),('rain',[(186.84,187.92),(195.62,197.12)]),('p62',[(330.48,337.60)]),
('stats',[(395.32,396.50),(396.52,400.84),(419.26,421.52)]),('close',[(427.44,429.02),(435.85,439.56)])]
RAF=f"aresample=48000,pan=mono|c0=0.5*c0+0.5*c1,highpass=f=85,arnndn=m={M}bd.rnnn:mix=0.9,equalizer=f=280:t=q:w=1.0:g=-2,equalizer=f=4200:t=q:w=1.2:g=2.5,equalizer=f=9500:t=h:w=4000:g=1.5,deesser=i=0.25,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=140:makeup=2"
files=[];scenes=[];fcount=0;k=0
for key,segs in S:
    st=fcount;shots=[]
    for si,(s,e) in enumerate(segs):
        s,e=snap(s),snap(e);d=e-s;wav=f'parts/{k:02d}.wav';mov=f'parts/{k:02d}.mov'
        run('ffmpeg','-v','error','-y','-ss',f'{s:.3f}','-t',f'{d:.3f}','-i','raw.mp4','-vn','-af',RAF,'-ar','48000','-c:a','pcm_s16le',wav)
        run('ffmpeg','-v','error','-y','-ss',f'{s:.3f}','-t',f'{d:.3f}','-i','raw.mp4','-an','-vf','fps=30,setsar=1','-c:v','libx264','-crf','10','-preset','fast','-pix_fmt','yuv420p',mov)
        n=int(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=nb_read_frames','-of','csv=p=0',mov],capture_output=True,text=True).stdout.strip())
        shots.append([fcount,fcount+n]);files.append({'mov':mov,'wav':wav,'n':n,'ad':d,'src':[s,e],'key':key});fcount+=n;k+=1
    scenes.append({'key':key,'f0':st,'f1':fcount,'shots':shots})
json.dump({'scenes':scenes,'files':files,'nf':fcount},open('scenes.json','w'),indent=1)
ins=[];fc=[]
for i,f in enumerate(files):
    ins+=['-i',f['mov'],'-i',f['wav']];L=f['n']/30;ad=min(f['ad'],L)
    fc.append(f"[{2*i}:v]setpts=PTS-STARTPTS[v{i}];[{2*i+1}:a]afade=t=in:d=0.012,afade=t=out:st={max(0,ad-0.02):.3f}:d=0.018,apad=whole_dur={L:.5f},atrim=0:{L:.5f},asetpts=PTS-STARTPTS[a{i}]")
fc.append(''.join(f'[v{i}][a{i}]' for i in range(len(files)))+f'concat=n={len(files)}:v=1:a=1[v][a]')
run(*(['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(fc),'-map','[v]','-map','[a]','-c:v','libx264','-crf','10','-preset','fast','-pix_fmt','yuv420p','-c:a','pcm_s16le','cut.mov']))
for s in scenes:print(f"{s['key']:8s} {s['f0']/30:6.2f} {s['f1']/30:6.2f}  ({(s['f1']-s['f0'])/30:.2f}s) shots {[ (a,b) for a,b in s['shots']]}")
print('total',fcount,fcount/30)
