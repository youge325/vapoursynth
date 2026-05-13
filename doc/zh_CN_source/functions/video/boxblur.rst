框模糊
=======

.. function:: BoxBlur(vnode clip[, int[] planes, int hradius = 1, int hpasses = 1, int vradius = 1, int vpasses = 1])
   :module: std

   执行边界模糊，即使对于增加的半径值也很快。使用多个 *passes* 可以降低成本地近似高斯模糊。*radius* 为 0 表示不进行处理。
