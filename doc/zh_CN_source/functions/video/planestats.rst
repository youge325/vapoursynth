平面统计
==========

.. function:: PlaneStats(vnode clipa[, vnode clipb, int plane=0, string prop='PlaneStats'])
   :module: std

   此函数计算指定 *plane* 中所有像素的简单、即时和平均归一化值，把这些值存储在名为 *prop*\ Min、*prop*\ Max 和 *prop*\ Average 的帧属性中。
   
   如果提供了 *clipb*，两个片段之间的绝对归一化差异也将存储在 *prop*\ Diff 中。
   
   归一化意味着无论输入格式如何，平均值和差异始终是 0 到 1 之间的浮点数。
