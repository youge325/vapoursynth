加载插件
==========

.. function::   LoadPlugin(string path, bint altsearchpath = False)
   :module: std

   加载一个原生 VapourSynth 插件。如果成功，加载的插件函数将位于其自己的命名空间中。

   如果已加载具有相同标识符或命名空间的插件，将返回错误。这是为了防止命名冲突或同时加载同一插件的多个版本。
   
   插件通常以非常特定的搜索顺序加载依赖项。设置 *altsearchpath* 会修改此行为，因此也包含 PATH 中的 dll。

   注意Python的转义字符，以下写法将失败：

      LoadPlugin(path='c:\plugins\filter.dll')

   正确的写法：
   
      LoadPlugin(path='c:/plugins/filter.dll')
      LoadPlugin(path=r'c:\plugins\filter.dll')
      LoadPlugin(path='c:\\plugins\\filter.dll')
