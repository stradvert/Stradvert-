# Sharp graded plates: bgs/ (no added blur) and bgm/ (mid blur for focus pulls). Location scenes get the 'view' look, interiors the 'int' look.
# usage: python3 prep_bgs.py [workers]
import numpy as np,cv2,json,os,sys
from multiprocessing import Pool
from grade import grade
for d in('bgs','bgm'):os.makedirs(d,exist_ok=True)
INT={'p62','stats','close'}
def one(a):
    f,look=a;name=f'{f+1:05d}'
    g=grade(cv2.cvtColor(cv2.imread(f'fr/{name}.jpg'),cv2.COLOR_BGR2RGB).astype(np.float32)/255,look)
    cv2.imwrite(f'bgs/{name}.jpg',cv2.cvtColor((g*255).astype(np.uint8),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,93])
    b=cv2.GaussianBlur(g,(0,0),5.0);cv2.imwrite(f'bgm/{name}.jpg',cv2.cvtColor((b*255).astype(np.uint8),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,90])
if __name__=='__main__':
    sj=json.load(open('scenes.json'));jobs=[(f,'int' if S['key'] in INT else 'view') for S in sj['scenes'] for f in range(S['f0'],S['f1'])]
    with Pool(int(sys.argv[1]) if len(sys.argv)>1 else 4) as p:p.map(one,jobs,chunksize=16)
    print('bgs done',len(jobs))
