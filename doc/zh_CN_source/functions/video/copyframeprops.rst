复制帧属性
==============

.. function:: CopyFrameProps(vnode clip, vnode prop_src[, string[] props])
   :module: std

   返回 *clip*，但所有帧属性替换为 *prop_src* 中对应剪辑的帧属性。注意，如果 *clip* 比 *prop_src* 长，则将使用源的最后一帧的属性。
   
   如果设置了 *props*，则只复制指定的属性。如果 *prop_src* 没有该属性，则该属性会被删除。在此模式下，*clip* 中的其他所有属性保持不变。
