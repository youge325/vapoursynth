合并
=====

.. function::   Merge(vnode clipa, vnode clipb[, float[] weight = 0.5])
   :module: std

   使用指定的每个平面的*weight* m *clipa* 和 *clipb*。默认对所有平面使用 0.5 *weight*。*weight* 表示*clipa* 不变返回，为 1 表示*clipb* 不变返回。如果指定了单体*weight*，则则用于所有平面。如果给出两个权重，第二个值也将用于第三个平面。

   0-1 范围之外的值被视为错误。指定的权重数量多于剪辑中的平面数量也是错误的。剪辑必须具有相同的尺寸和格式。

   如何合并亮度：

      Merge(clipa=A, clipb=B, weight=[1, 0])

   如何合并色度：

      Merge(clipa=A, clipb=B, weight=[0, 1])

   两个片段的平均值：

      Merge(clipa=A, clipb=B)

   帧属性从 *clipa* 复制。
