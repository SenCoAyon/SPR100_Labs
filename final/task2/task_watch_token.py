#!/usr/bin/env python3
from __future__ import annotations
import argparse as A,pathlib as B,sys as C
D="0123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnp";E=len(D)
def F(G:bytes)->str:return"".join(D[H]+D[I]for H,I in((J//E,J%E)for J in G))
def K(L:B.Path,M:int=2)->list[str]:
    with L.open("r",encoding="utf-8")as N:O=[P.strip()for P in N.readlines()if P.strip()]
    if not O:raise SystemExit("ERROR: watchdog log is empty.")
    return O[-M:]
def Q(R:B.Path,S:str)->str:
    T=K(R);U=R.stat().st_size;V=len(T);W="||".join(T)
    return F("|".join([f"student={S}",f"path={R}",f"log_size={U}",f"entries={V}",f"lines={W}"]).encode("utf-8"))
def X()->None:
    Y=A.ArgumentParser(description="Generate Task 2 token from watchdog log lines.")
    Y.add_argument("log_file",type=B.Path,help="Path to watchdog.log produced by your systemd user service.")
    Y.add_argument("student_number",type=str,help="Seneca student number (digits only).")
    Z=Y.parse_args()
    if not Z.student_number.isdigit():raise SystemExit("ERROR: student number must contain digits only.")
    a=Z.log_file.expanduser().resolve()
    if not a.exists():raise SystemExit(f"ERROR: {a} does not exist.")
    b=Q(a,Z.student_number);print(f"TASK2-TOKEN:{b}");print("Record this token alongside your Task 2 evidence in the answer sheet.")
if __name__=="__main__":
    try:X()
    except KeyboardInterrupt:C.exit("Aborted by user.")