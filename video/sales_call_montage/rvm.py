import onnxruntime as ort,numpy as np,json,sys,time,os
from PIL import Image
model=sys.argv[1];dr=float(sys.argv[2]);only=sys.argv[3].split(',') if len(sys.argv)>3 and sys.argv[3]!='all' else None;outdir=sys.argv[4] if len(sys.argv)>4 else 'al'
so=ort.SessionOptions();so.intra_op_num_threads=4
sess=ort.InferenceSession(model,so,providers=['CPUExecutionProvider'])
sc=json.load(open('scenes.json'));os.makedirs(outdir,exist_ok=True)
t0=time.time();n=0
for S in sc['scenes']:
    if only and S['key'] not in only:continue
    rec=[np.zeros([1,1,1,1],dtype=np.float32)]*4
    # warm up recurrent state on the first frame (run it 3x) so the first matte is stable
    frames=list(range(S['f0'],S['f1']))
    seq=[frames[0]]*3+frames
    for j,f in enumerate(seq):
        im=np.asarray(Image.open(f'fr/{f+1:05d}.jpg').convert('RGB'),dtype=np.float32)/255
        src=im.transpose(2,0,1)[None]
        fgr,pha,*rec=sess.run(None,{'src':src,'r1i':rec[0],'r2i':rec[1],'r3i':rec[2],'r4i':rec[3],'downsample_ratio':np.array([dr],dtype=np.float32)})
        if j>=3:
            a=(np.clip(pha[0,0],0,1)*255).astype(np.uint8);Image.fromarray(a).save(f'{outdir}/{f+1:05d}.png',compress_level=1);n+=1
    print(S['key'],round(time.time()-t0,1),'s',n,'frames',flush=True)
