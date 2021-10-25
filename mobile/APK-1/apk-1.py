bytes2 = "5FQ5AaBGbqLGfYwjaRAuWGdDvyjbX5nH".encode()
 
bArr2 = [i for i in range(256)]
i2 = 0
i3 = 0
for i in range(256):
    i3 = ((bytes2[i2] & 255) + (bArr2[i] & 255) + i3) & 255
    b2 = bArr2[i]
    bArr2[i] = bArr2[i3]
    bArr2[i3] = b2
    i2 = (i2 + 1) % len(bytes2)
 
bArr = [81, 256-13, 84, 256-110, 72, 77, 256-96, 77, 32, 256-115, 256-75, 256-38, 256-97, 69, 256-64, 49, 8, 256-27, 56, 114, 256-68, 256-82, 76, 256-106, 256-34]
i5=16
i6=0
i7=0
token = []
for i in range(25):
    i6 = (i6 + 1) & 255
    i7 = ((bArr2[i6] & 255) + i7) & 255
    b3 = bArr2[i6]
    bArr2[i6] = bArr2[i7]
    bArr2[i7] = b3
    for j in range(256):
        if (bArr2[((bArr2[i6] & 255) + (bArr2[i7] & 255)) & 255] ^ j) == bArr[i]:
            token.append(j)
print(bytes(token).decode())
