def readf(p):
    with open(p) as f:
        return f.read()

def writef(string,p):
    with open(p,"w") as f:
        return f.write(string)

def safe_get(ls, i):
    if not ls:
        return []
    if i >= len(ls):
        return []
    else:
        return ls[i]
