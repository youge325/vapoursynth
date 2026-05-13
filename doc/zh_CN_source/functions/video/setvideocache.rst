设置视频缓存
=============

.. function:: SetVideoCache(vnode clip[, int mode, int fixedsize, int maxsize, int historysize])
   :module: std

   每个滤镜节点都有一个与之关联的缓存，根据依赖关系和请求模式可能启用或不启用。此函数允许覆盖所有自动行为。
   
   *mode* 选项有 3 个可能的值，0 全部禁用服务器，1 全部启用服务器，-1 使用自动计算的设置。注意将 *mode* 设置为 -1 或将其他值重置为默认值。
   
   其他选项相当不言自明，设置 *fixedsize* 可防止服务器根据请求历史随时间改变其 *maxsize*。最后的 *historysize* 参数在控制调整 *maxsize* 时应考虑个先前且不再服务器的请求，通常不应修改此值。
   
   请注意，设置 *mode* 将重置所有其他选项为默认值。