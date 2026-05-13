加载所有插件
==============

.. function::   LoadAllPlugins(string path)
   :module: std

   加载在指定 *path* 中找到所有原生 VapourSynth 插件。加载失败的插件将被静默跳过。

   注意Python的转义字符，以下写法将失败：

      LoadPlugin(path='c:\plugins')

   正确的写法：
   
      LoadPlugin(path='c:/plugins')
      LoadPlugin(path=r'c:\plugins')
      LoadPlugin(path='c:\\plugins\\')
