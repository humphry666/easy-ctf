## AreYouRich
# 商业转载请联系作者获得授权，非商业转载请注明出处。
# For commercial use, please contact the author for authorization. For non-commercial use, please indicate the source.
# 协议(License)：署名-非商业性使用-相同方式共享 4.0 国际 (CC BY-NC-SA 4.0)
# 作者(Author)：Wankko Ree
# 链接(URL)：https://www.wkr.moe/ctf/648.html
# 来源(Source)：Wankko Ree's Blog

打开apk看了下，主activity就三段代码看起来比较重要。



大概意思就是有个f896a后面应该有用，然后o/p分别对应账号密码，账号每位异或个34再拼接个@001就是密码。

然后一个看起来能当全局变量用的token规则就是账号+密码+时间戳，中间用下划线隔一下。

接着去看user的activity。



其中获取flag的条件就是余额大于那个499999999，然后输出flag的话是个用初始化对象的时候的str变量参与另一个内置数组的异或拿到的，大致逻辑可见上图。

然后看下面初始化时的余额生成算法。



刚才那个a对象初始化时候的str变量跟了下是之前的token，所以flag其实是token相关且唯一相关的，那么就看token的合法逻辑是个啥了，而这里正好i5就是余额累加器，其中的条件成立则翻倍，不成立就加个随机数，所以既然要在有限次里得到499999999，那就让条件一直成立呗。而这里看了下，条件实际上的可控变量只有bytes，跟上去发现就是token，所以这里的成立逻辑正好可以用来生成token。

理一下思路，就是构造token，使得余额生成时一直翻倍，达到499999999以上，然后去拿flag，或者用token直接构造flag。

而token实际上只用到了前25位，因为循环变量int min = Math.min(bytes.length, bArr.length);跟一下变量来源就会发现实际上就是比较token和f897b度谁更小，那自然是f897b小，所以正好与最后的时间戳无关，只与前面的账号10+下划线1+密码14有关。

那就可以写脚本了，主要就是把各种不可控的所需数据咋生成的给复制过来，然后爆破一下token每位的情况。




得到账号密码，然后flag生成懒得再继续写脚本了，所以就去app里拿吧。

