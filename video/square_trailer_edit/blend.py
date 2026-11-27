import numpy as np,cv2,os,sys
from multiprocessing import Pool
os.makedirs('out',exist_ok=True)
def one(f):
    n=int(open(f'sub/{f:05d}.n').read());acc=None
    for i in range(n):
        im=cv2.imread(f'sub/{f:05d}_{i}.jpg').astype(np.float32);acc=im if acc is None else acc+im
    cv2.imwrite(f'out/{f:05d}.png',np.clip(acc/n+0.5,0,255).astype(np.uint8),[cv2.IMWRITE_PNG_COMPRESSION,1]);return n
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    with Pool(4) as p:r=p.map(one,range(a,b),chunksize=8)
    print('blended',len(r),'frames, avg samples',sum(r)/len(r))
