空白音频
==========

.. function:: BlankAudio([anode clip, int[] channels=[FRONT_LEFT, FRONT_RIGHT], int bits=16, int sampletype=INTEGER, int samplerate=44100, int length=(10*samplerate), bint keep=0])
   :module: std

   生成一个新的空片段。这在编辑音频或测试时很有用。默认是一个 10 秒长的 44.1kHz 16 位碎片。BlankAudio 也可以从 *clip* 复制属性，而单独指定每个属性。如果同时设置了 *sampletype* 等参数和 *clip*，则 *sampletype* 优先。
   
   *channels* 参数是通道常量的列表。不允许指定相同的通道两次。
   
   目前可能的 *sampletype* 值为 INTEGER (0) 和 FLOAT (1)。

   如果设置了*keep*，每次请求都返回对同一帧的引用。否则每次都生成新帧。通常没有理由更改此设置。
