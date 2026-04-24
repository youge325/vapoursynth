删除框架属性
================

.. function:: RemoveFrameProps(vnode clip[, string props[]])
   :module: std

   返回 *clip*，但删除 *props* 中指定的所有帧属性。如果 *props* 未设置，则删除所有帧属性。

   注意 *props* 接受通配（符* 和 ?），这非常有用，例如如果您清除由污染物污染物设置的属性，它们因为通常有出口，如 VFM\* 或 _\* 可快捷方式来仅清除内部保留属性（色度学、时间、场结构）。
   