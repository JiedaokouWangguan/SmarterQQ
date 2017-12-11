
def hash2(uin, ptvfwebqq):
    ptb = [0,0,0,0]
    for i in range(0, len(ptvfwebqq)):
        ptbIndex = i%4
        ptb[ptbIndex] ^= ord(ptvfwebqq[i])

    salt = ["EC", "OK"]
    uinByte = [0,0,0,0]
    uinByte[0] = (((uin >> 24) & 0xFF) ^ ord(salt[0][0]))
    uinByte[1] = (((uin >> 16) & 0xFF) ^ ord(salt[0][1]))
    uinByte[2] = (((uin >> 8) & 0xFF) ^ ord(salt[1][0]))
    uinByte[3] = ((uin & 0xFF) ^ ord(salt[1][1]))
    result = [0,0,0,0,0,0,0,0]
    for i in range(0,8):
        if i % 2 == 0:
            result[i] = ptb[i>>1]
        else:
            result[i] = uinByte[i>>1]
    return byte2hex(result)


def byte2hex(bytes):
    hex = hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    buf = ""
    for i in range(0, len(bytes)):
        buf += hex[(bytes[i] >> 4) & 0xF]
        buf += hex[bytes[i] & 0xF]
    return buf

def hash33(s):
    e = 0
    i = 0
    n = len(s)
    while n > i:
        e += (e << 5) + ord(s[i])
        i += 1
    return 2147483647 & e