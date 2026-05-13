分离字段
==============

.. function:: SeparateFields(vnode clip[, bint tff, bint modify_duration=True])
   :module: std

   返回场分离并交错的片段。

   *tff* 参数仅在未为帧设置场顺序时有效。将 *tff* 设置为 true 表示顶场优先，false 表示底场优先。

   如果设置了*modify_duration*，则输出片段的帧率是输入片段的两倍。帧持续时间也会减半。

   ``_FieldBased`` 帧属性被删除。添加 ``_Field`` 帧属性。
   
   如果在 ``_FieldBased`` 或 *tff* 中未指定顺序，将返回错误。
