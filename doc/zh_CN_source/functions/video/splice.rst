拼接
======

.. function::   Splice(vnode[] clips[, bint mismatch=0])
   :module: std

   返回按给定顺序附加所有*剪辑* 的片段。

   拼接不同格式或维度的片段将被视为错误，除非 *mismatch* 为 true。

   在Python中，std.Splice也可以通过 :ref:`加法运算符 <pythonreference>` 调用。
