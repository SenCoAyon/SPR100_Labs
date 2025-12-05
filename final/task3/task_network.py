#!/usr/bin/env python3
from __future__ import annotations
import argparse as a,http.client as b,random as c,ssl as d,sys as e,time as f
from urllib.parse import urlparse as g
h="0123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnp";i=len(h);j="SPR100-Final/1.0"
k=tuple("".join(chr(l)for l in m)for m in((104,116,116,112,115,58,47,47,101,120,97,109,112,108,101,46,99,111,109,47),(104,116,116,112,115,58,47,47,101,120,97,109,112,108,101,46,111,114,103,47),(104,116,116,112,115,58,47,47,119,119,119,46,103,111,111,103,108,101,46,99,111,109),(104,116,116,112,115,58,47,47,119,119,119,46,115,101,110,101,99,97,112,111,108,121,116,101,99,104,110,105,99,46,99,97),(104,116,116,112,115,58,47,47,119,119,119,46,101,120,97,109,112,108,101,46,110,101,116)))
def l(m:bytes)->str:return"".join(h[n]+h[o]for n,o in((p//i,p%i)for p in m))
def q(r:str)->tuple[str,int,str,bytes]:
    s=g(r);t=d.create_default_context();u=b.HTTPSConnection(s.netloc,timeout=15,context=t);u.putrequest("GET",s.path or "/");u.putheader("User-Agent",j);u.endheaders();v=u.getresponse();w=v.read();x,y=u.sock.getpeername();u.close();return r,y,x,w
def z(aa:str,ab:str,ac:str,ad:bytes)->str:return l("|".join([f"student={aa}",f"url={ab}",f"endpoint={ac}",f"bytes={len(ad)}",f"preview={ad[:32]!r}"]).encode("utf-8"))
def ae()->None:
    af=a.ArgumentParser(description="Generate deterministic HTTPS traffic plus a grading token.");af.add_argument("--student-number",required=True,help="Seneca student number (digits only).");ag=af.parse_args()
    if not ag.student_number.isdigit():raise SystemExit("ERROR: student number must contain digits only.")
    print("[Task 3] Initiating HTTPS request...");ah=c.choice(k);ai,aj,ak,al=q(ah);am=z(ag.student_number,ai,ak,al);print("[Task 3] Traffic generation complete.");print("Use tshark/wireshark to inspect the capture and extract the required details.");print(f"TASK3-TOKEN:{am}");f.sleep(0.5)
if __name__=="__main__":
    try:ae()
    except KeyboardInterrupt:e.exit("Aborted by user.")

