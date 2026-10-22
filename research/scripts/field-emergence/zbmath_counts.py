import json,os,time,threading,random,subprocess,urllib.parse
from concurrent.futures import ThreadPoolExecutor
WIN=[(1931,1949)]+[(y,y+9) for y in range(1950,2020,10)]+[(2020,2024)]
PAIRS=[("11","37"),("05","37"),("05","11"),("57","81"),("58","81"),("46","57"),("11","14"),("11","20"),("20","81"),("14","81"),
("30","60"),("60","81"),("05","20"),("14","51"),("14","52"),("05","14"),("35","60"),("05","94"),("05","68"),("05","55"),("55","58"),("17","81"),("37","94"),("32","35"),("11","22")]
SEC="00 01 03 05 06 08 11 12 13 14 15 16 17 18 20 22 26 28 30 31 32 33 34 35 37 39 40 41 42 43 44 45 46 47 49 51 52 53 54 55 57 58 60 62 65 68 70 74 76 78 80 81 82 83 85 86 90 91 92 93 94 97".split()
random.seed(11)
inv={s for p in PAIRS for s in p}
cand=[(a,b) for i,a in enumerate(sorted(inv)) for b in sorted(inv)[i+1:] if (a,b) not in PAIRS]
CTRL=random.sample(cand,10)
OUT="zbmath_counts.jsonl"
done={}
for l in open(OUT):
    r=json.loads(l)
    if r["n"] is not None: done[r["q"]]=r["n"]
qs=[]
for a,b in WIN:
    w=f"py:{a}-{b}"; qs.append(w)
for a,b in WIN:
    w=f"py:{a}-{b}"
    qs+=[f"cc:{s} cc:{t} {w}" for s,t in PAIRS+CTRL]
for a,b in WIN:
    w=f"py:{a}-{b}"
    qs+=[f"cc:{s} {w}" for s in sorted(inv)]
todo=[q for q in qs if q not in done]
json.dump({"pairs":PAIRS,"control":CTRL,"windows":WIN,"sections":sorted(inv)},open("zb_spike_meta.json","w"))
print(len(qs),"queries;",len(todo),"todo",flush=True)
def count(q):
    u="https://api.zbmath.org/v1/document/_search?page=0&results_per_page=1&search_string="+urllib.parse.quote(q)
    for k in range(5):
        p=subprocess.run(["curl","-s","--max-time","120",u],capture_output=True,text=True)
        try:
            st=json.loads(p.stdout)["status"]
            if st.get("nr_total_results") is not None: return st["nr_total_results"]
            if st.get("status_code")==404 and "No results" in str(st.get("internal_code","")): return 0
            time.sleep(4*(k+1))
        except Exception: time.sleep(4*(k+1))
    return None
lock=threading.Lock(); f=open(OUT,"a"); c=[0,0]
def work(q):
    n=count(q)
    with lock:
        f.write(json.dumps({"q":q,"n":n})+"\n"); f.flush(); c[0]+=1; c[1]+= n is None
        if c[0]%25==0: print(c,time.strftime("%H:%M:%S"),flush=True)
with ThreadPoolExecutor(4) as ex: list(ex.map(work,todo))
print("DONE",c,flush=True)
