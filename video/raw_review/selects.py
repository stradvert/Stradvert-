# Selects reel for review: raw clips in the given order, each labelled with its timecode in the raw.
# usage: python3 selects.py raw.mov clips.json out.mp4     clips.json = [[start_s, end_s, "LABEL"], ...]  (labels: no colons or quotes)
import json,os,subprocess,sys
src,clips,out=sys.argv[1],json.load(open(sys.argv[2])),sys.argv[3]
FONT=os.environ.get('FONT','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
tc=lambda s:f"{int(s//60)}:{int(s%60):02d}";os.makedirs('sel_clips',exist_ok=True);lst=[]
for i,(a,b,lab) in enumerate(clips):
    d=b-a;txt=f'{lab}   raw {tc(a)}'.replace(':','\\:')
    vf=(f"scale=720:1280:flags=lanczos,format=yuv420p,fade=t=in:st=0:d=0.12,fade=t=out:st={d-0.12:.2f}:d=0.12,"
        f"drawbox=x=0:y=0:w=iw:h=74:color=black@0.62:t=fill,drawtext=fontfile={FONT}:text='{txt}':x=24:y=24:fontsize=28:fontcolor=0xFCEF00")
    o=f'sel_clips/{i:03d}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{a:.2f}','-i',src,'-t',f'{d:.2f}','-vf',vf,'-af',f"loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:d=0.08,afade=t=out:st={d-0.1:.2f}:d=0.1",
                    '-r','30','-c:v','libx264','-preset','veryfast','-crf','23','-c:a','aac','-b:a','160k','-ar','48000','-ac','2',o],check=True);lst.append(f"file '{o}'")
open('sel_list.txt','w').write('\n'.join(lst)+'\n')
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','sel_list.txt','-c','copy','-movflags','+faststart',out],check=True)
print(len(clips),'clips, %.0fs'%sum(b-a for a,b,_ in clips))
