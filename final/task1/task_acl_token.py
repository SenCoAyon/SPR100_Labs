#!/usr/bin/env python3
from __future__ import annotations
import argparse as A,hashlib as B,pathlib as C,subprocess as D,sys as E
F="0123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnp";G=len(F)
def H(I:bytes)->str:return"".join(F[J]+F[K]for J,K in((L//G,L%G)for L in I))
def M(N:C.Path)->str:
    try:O=D.run(["getfacl","-p",str(N)],check=True,capture_output=True,text=True)
    except FileNotFoundError as P:raise SystemExit("ERROR: getfacl is not available. Install the 'acl' package first.")from P
    except D.CalledProcessError as Q:raise SystemExit(f"ERROR: getfacl failed: {Q.stderr.strip()}")from Q
    R=[S.strip()for S in O.stdout.splitlines()if S.strip()and not S.startswith("#")]
    if not R:raise SystemExit("ERROR: getfacl returned no ACL entries.")
    return"|".join(R)
def T(U:C.Path)->str:
    V=B.sha256()
    with U.open("rb")as W:
        for X in iter(lambda:W.read(8192),b""):V.update(X)
    return V.hexdigest()
def Y(Z:C.Path,a:str)->str:
    b=Z.stat()
    try:
        import pwd as c,grp as d
    except ImportError as e:raise SystemExit("ERROR: pwd/grp modules are required on Linux/Unix.")from e
    f=c.getpwuid(b.st_uid).pw_name;g=d.getgrgid(b.st_gid).gr_name;h=oct(b.st_mode&0o777);i=b.st_size
    return H("|".join([f"student={a}",f"path={Z}",f"owner={f}",f"group={g}",f"mode={h}",f"size={i}",f"acl={M(Z)}",f"file_sha256={T(Z)}"]).encode("utf-8"))
def j()->None:
    k=A.ArgumentParser(description="Generate Task 1 token from file metadata and ACL.")
    k.add_argument("target",type=C.Path,help="Path to the protected file (e.g., ~/SPR100_Labs/final/task1/vault.log)")
    k.add_argument("student_number",type=str,help="Seneca student number (digits only).")
    l=k.parse_args()
    if not l.student_number.isdigit():raise SystemExit("ERROR: student number must contain digits only.")
    m=l.target.expanduser().resolve()
    if not m.exists():raise SystemExit(f"ERROR: {m} does not exist.")
    n=Y(m,l.student_number);print(f"TASK1-TOKEN:{n}");print("Keep this token with your other Task 1 observations in the answer sheet.")
if __name__=="__main__":
    try:j()
    except KeyboardInterrupt:E.exit("Aborted by user.")