双层编织
===========

.. function:: DoubleWeave(vnode clip[, bint tff])
   :module: std

   将交错场的片段中的场重新编织在一起。

   由于 VapourSynth 内部对场序不够弱概念，可能需要设置 *tff*。将 *tff* 设置为 true 表示顶场优先，false 表示底场优先。注意，如果存在 ``_Field`` 帧属性且组合有效，则其优先于 *tff*。

   DoubleWeave 的输出帧数与输入相同。必须将 DoubleWeave 与 SelectEvery 一起使用才能撤消 SeparateFields 的效果::

      sep = core.std.SeparateFields(source)
      ...
      woven = core.std.DoubleWeave(sep)
      woven = core.std.SelectEvery(woven, 2, 0)

   ``_Field`` 帧属性被删除，``_FieldBased`` 相应设置。
