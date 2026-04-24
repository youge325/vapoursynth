修剪
====

.. function::   Trim(vnode clip[, int first=0, int last, int length])
   :module: std

   Trim 返回仅包含参数 *first* 和 *last* 之间帧的剪辑，或从 *first* 开始的 *length* 帧的剪辑。Trim 是包含性的，因此 Trim(clip,first=3,last=3) 将返回一帧。既如果未指定 *last* 则也未指定 *length*，不会从剪辑结果删除帧。
   
   同时指定 *last* 和 *length* 被视为错误。同样，以不返回任何帧的方式调用 Trim 也是错误的， VapourSynth 不允许 0 因为帧片段。

   在Python中，std.Trim也可以通过 :ref:`切片 <pythonreference>` 调用。
