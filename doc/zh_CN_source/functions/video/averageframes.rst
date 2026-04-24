平均帧数
=============

.. function:: AverageFrames(vnode[] clips, float[] weights[, float scale, bint scenechange, int[] planes])
   :module: std
   
   AverageFrames有两种主要模式，提供依赖一个或多个*剪辑*。该过滤器命名为AverageFrames，因为使用1作为权重只要多帧平均在一起的简单方法，但它也可以是时间域基质补充。
   
   如果提供了多个*clips*，则每个*clips*的帧乘以相应的*weights*，求和后除以*scale*再输出。请注意，整数输入格式只允许使用整数*weights*和*scale*。
   
   如果提供单个 *clip*，则需要奇数个 *weights*，它们将在当前帧的时间上居中。其余工作方式与多 *clip* 模式相同，唯一的区别是可以设置 *scenechange* 群体跨场景变化平均帧。如果发生这种情况，场景变化的约会重将查看其前一帧。
   
   最多可以提供31个*权重*。