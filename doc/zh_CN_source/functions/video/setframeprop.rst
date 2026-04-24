设置框架属性
============

.. function:: SetFrameProp(vnode clip, string prop[, int[] intval, float[] floatval, string[] data])
   :module: std

   为 *clip* 中的每一帧添加帧属性。

   如果帧中已存在名为 *prop* 的属性，将会被覆写。

   添加的属性类型取决于使用 *intval*、*floatval* 还是 *data* 参数。

   例如，设置场序为顶场优先：

      clip = c.std.SetFrameProp(clip, prop="_FieldBased", intval=2)
