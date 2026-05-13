假设FPS
=========

.. function:: AssumeFPS(vnode clip[, vnode src, int fpsnum, int fpsden=1])
   :module: std

   返回帧率已更改的片段。这不会以任何方式修改帧，只修改其元数据。

   要分配的帧率可以从另一个片段 *src* 读取，或以有理数的形式通过 *fpsnum* 和 *fpsden* 给出。

   同时指定 *src* 和 *fpsnum* 是错误的。

   假设FPS用从新帧率计算出的帧持续时间覆盖帧属性``_DurationNum``和``_DurationDen``。
