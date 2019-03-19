def txt_read():
    Col = []
    Row = []
    path = 'WikiData.txt'
    with open(path) as f:
        for line in f:
            if not line:
                pass
            a,b = line.split()
            a = int(a)
            b = int(b)
            Col.append(a)
            Row.append(b)
    return Col, Row

