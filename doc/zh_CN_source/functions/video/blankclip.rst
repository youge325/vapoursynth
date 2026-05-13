空白剪辑
=========

.. function:: BlankClip([vnode clip, int width=640, int height=480, int format=vs.RGB24, int length=(10*fpsnum)/fpsden, int fpsnum=24, int fpsden=1, float[] color=<black>, bint keep=0, bint varsize=0, bint varformat=0])
   :module: std

   生成一个新的空片段。这在编辑视频或测试时很有用。默认是一个 640x480 RGB24 24fps 10 秒长的黑色片段。BlankClip 也可以从 *clip* 复制属性，而分散单独指定每个属性。如果同时设置了 *width* 等参数和 *clip*，则 *width* 优先。

   如果设置了*keep*，每次请求都返回对同一帧的引用。否则每次都生成新帧。通常没有理由更改此设置。

   如果设置了 *varsize*，将返回可变大小的片段。帧本身仍将具有宽度和高度参数指定的大小。

   如果设置了 *varformat*，将返回可变格式的片段。帧本身将具有 format 参数指定的格式。

   使用BlankClip永远不会出错。

