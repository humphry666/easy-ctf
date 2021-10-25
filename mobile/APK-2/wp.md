##  designEachStep
# 商业转载请联系作者获得授权，非商业转载请注明出处。
# For commercial use, please contact the author for authorization. For non-commercial use, please indicate the source.
# 协议(License)：署名-非商业性使用-相同方式共享 4.0 国际 (CC BY-NC-SA 4.0)
# 作者(Author)：Wankko Ree
# 链接(URL)：https://www.wkr.moe/ctf/648.html
# 来源(Source)：Wankko Ree's Blog

这题jadx不认代码，当时懵逼了一下。



然后想起来有个叫gda的工具吹得挺牛逼的，就去试了下，没想到真的可以用，不过代码依旧有点问题，有时候代码前后逻辑矛盾的，所以还得靠像用ida那样猜。





主要的逻辑都在第二张图那个类里（因为图一确实没啥东西）。

大概看了一下，没咋看懂（java的流式读写的代码太狗屎了），不过刚开始应该是读取data.bin然后解一下gzip压缩。



所以就写脚本解个gzip试试。
```
import gzip
 
with open('data.bin', 'rb') as f:
    data = gzip.decompress(f.read())
print(data)
```

似乎前面几位有成为flag的趋势。

然后回去看代码，应该是解压后的前八位单独取出来，后面剩下的用前八位解一次DES/ECB/PKCS5Padding，至于为什么是用这个模式，因为DES的话是上面String str = "DES";定义的，拼在加密工具类初始化里了cInstance1 = Cipher.getInstance(str);，然后ECB/PKCS5Padding是javax.crypto.Cipher在解DES的默认模式（不指定的话）。



所以改进一下脚本看看能不能成功解码。
```
import gzip
from Crypto.Cipher import DES
 
with open('data.bin', 'rb') as f:
    data = gzip.decompress(f.read())
part1 = data[:8]
print(part1)  # DE5_c0mp
data = data[8:]
 
des = DES.new(part1, DES.MODE_ECB)
data = des.decrypt(data)
print(data)
```

不过看不出啥东西，至少没报错就是好事，接着去看代码。



似乎又是解了个类似于压缩一样的东西，查了下inflater.inflate就是python里的zlib.decompress，所以那就去解一下看看呗。



又是一个看起来能成为flag的开头。

然后下面接着看代码，又是解一次des，用的密钥就是刚出来的那个前八位。



所以再改改脚本看看。
```
import gzip
from Crypto.Cipher import DES
import zlib
 
with open('data.bin', 'rb') as f:
    data = gzip.decompress(f.read())
part1 = data[:8]
print(part1)  # DE5_c0mp
data = data[8:]
 
des = DES.new(part1, DES.MODE_ECB)
data = des.decrypt(data)
data = zlib.decompress(data)
part2 = data[:8]
print(part2)  # r355_m@y
data = data[8:]
des = DES.new(part2, DES.MODE_ECB)
data = des.decrypt(data)
print(data)
```

然后看网上有些文章说python解des出来可能会有奇奇怪怪的填充头尾，所以图上的0xff都是没必要的，去真正的开头看看有啥。



好家伙我感觉flag都要出来了，因为刚开始要求输入的就是24位，之前两次8位已经出来了，这次能当明文的有9位，那就都拿去app里试试。

于是在输入DE5_c0mpr355_m@y_c0nfu53的时候成功拿到flag。
