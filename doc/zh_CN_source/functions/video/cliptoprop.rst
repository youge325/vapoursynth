剪辑到道具
==========

.. function:: ClipToProp(vnode clip, vnode mclip[, string prop='_Alpha'])
   :module: std

   将 *mclip* 的每一帧作为名为 *prop* 的帧属性存储在 *clip* 中。这主要用于将蒙版/alpha 片段附加到另一个片段上，以便编辑操作同时选取两者。与大多数滤波器其他不同，输出长度称为 *mclip* 的第二个参数。

   如果附加的 *mclip* 不代表 alpha 通道，你应该将 *prop* 设置为其他值。

   这就是 PropToClip() 的逆操作。
