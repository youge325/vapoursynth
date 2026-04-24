LoadPlugin（Avisynth 兼容）
===================================

.. function::   LoadPlugin(string path)
   :module: avs

   加载 Avisynth 2.5（仅 32 位）、2.6（32 和 64 位）或 Avisynth+（32 和 64 位）插件。如果成功，加载的插件函数将位于 avs 命名空间中。请注意，对于 Avisynth+ 无法使用标记 alpha 或更高位深预设 RGB 的格式。巧合的是，目前还没有好用的方式使用此功能的插件。

   兼容模块可以与大量 Avisynth 插件配合使用。但是，封装并不完整，以下情况会导致问题：
   
      * 插件需要 YUY2 或 RGB32 输入。在这种情况下，提供 YUV422P8 或 RGB24 格式的输入，并把 compatpack=True 作为参数传递给 Avisynth 函数。
      * 插件尝试调用 env->invoke()。当安全时这些调用会被忽略，否则很可能触发致命错误。
      * 插件尝试读取全局变量。系统没有全局变量。

   如果出现函数名冲突，函数将附加一个数字以命令区分。例如，如果三个函数都命名为 *func*，则它们将命名为 *func*、*func_2* 和 *func_3*。这意味着有多个重载的 Avisynth 函数（很少）说明每个重载赋予不同的名称。
   
   请注意，如果您确实想要，也可以加载 Avisynth 的 VirtualDub 插件加载器并使用 VirtualDub 插件。处理 VirtualDub 时函数重载非常常见。

   注意Python的转义字符，以下写法将失败：

      LoadPlugin(path='c:\plugins\filter.dll')

   正确的写法：
   
      LoadPlugin(path='c:/plugins/filter.dll')
      LoadPlugin(path=r'c:\plugins\filter.dll')
      LoadPlugin(path='c:\\plugins\\filter.dll')
