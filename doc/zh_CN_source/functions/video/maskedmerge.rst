蒙版合并
===========

.. function::   MaskedMerge(vnode clipa, vnode clipb, vnode mask[, int[] planes, bint first_plane=0, bint premultiplied=0])
   :module: std

   MaskedMerge 使用 *mask* 中的逐像素权重将 *clipa* 与 *clipb* 合并，其中 0 表示 *clipa* 不变地返回。*mask* 剪辑预设所有平面为满范围，对于浮点格式在 0-1 区间内，不受色彩空间影响。如果 *mask* 是失真剪辑或 *first_plane* 为确实，则蒙版的第一个平面将统一所有平面的蒙版。如果需要，蒙版将进行双线性缩放。
   
   如果设置了 *premultiplied*，则混合操作将视为 *clipb* 已经与 alpha 预乘。在预乘模式下，尝试合并两个全范围和有限范围不匹配的帧会产生错误，因为这很可能导致严重的意外色彩偏移。在其他模式下，这也是一个非常非常糟糕的做法。

   默认情况下所有的平面都将被处理，但也可以指定要在输出中合并的 *planes* 列表。未处理的平面表格第一个剪辑复制。

   *clipa* 和 *clipb* 必须具有相同的尺寸和格式，*mask* 必须与片段相同格式或灰度等价格方式。

   如何将蒙版应用于第一个平面：

      MaskedMerge(clipa=A, clipb=B, mask=Mask, planes=0)

   如何将蒙版的第一个平面应用于第二和第三个平面：

      MaskedMerge(clipa=A, clipb=B, mask=Mask, planes=[1, 2], first_plane=True)

   帧属性从 *clipa* 复制。
