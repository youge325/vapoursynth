设置框架属性
=============

.. function:: SetFrameProps(vnode clip, ...)
   :module: std

   将指定的值作为帧属性添加到 *clip* 的每一帧。如果已存在具有相同键的帧属性，将会被替换。

   例如，设置场序为顶场优先：

      clip = c.std.SetFrameProps(clip, _FieldBased=2)
