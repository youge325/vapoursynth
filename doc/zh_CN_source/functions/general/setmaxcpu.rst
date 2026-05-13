设置最大 CPU 指令集
====================

.. function::   SetMaxCPU(string cpu)
   :module: std

   此函数仅用于测试和调试目的，设置优化函数使用的最大指令集。
   
   x86 可用值："avx2"、"sse2"、"none"
   
   其他平台可用值："none"
   
   默认情况下使用所有支持的 CPU 特性。