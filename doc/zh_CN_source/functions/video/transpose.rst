转置
=========

.. function:: Transpose(vnode clip)
   :module: std

   以矩阵转置的方式翻转帧的内容。将其与 FlipVertical 或 FlipHorizontal 组合可实现左旋或右旋。连续调用 Transpose 两次等同于不做任何操作（但更慢）。

   下图展示了 Transpose 的效果::

                                 0   5  55
        0   1   1   2   3        1   8  89
        5   8  13  21  34   =>   1  13 144
       55  89 144 233 377        2  21 233
                                 3  34 377
