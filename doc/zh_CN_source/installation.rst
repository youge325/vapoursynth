安装与编译
========================

通用安装
####################

推荐通过 pip 安装 VapourSynth。目前 Windows、Linux 和 macOS 都提供二进制 wheel。

1. 安装 Python 3.12 或更高版本
2. 运行 ``pip install vapoursynth``
3. 运行 ``vapoursynth config``
4. （仅 Windows）如果提示，请更新 Visual Studio 2015-2026 Redistributable

Windows 可选步骤：

5. 运行 ``vapoursynth register-install`` 设置 VSSCRIPT_PATH 环境变量，以便其他应用找到该库
6. 运行 ``vapoursynth register-legacy-install`` 将安装信息写入注册表，使不了解 R74 及后续版本的应用仍可工作
7. 运行 ``vapoursynth register-vfw`` 注册 VFW 模块

请注意，借助这些命令，你可以在虚拟环境中方便地切换多个安装实例。

macOS、Linux 等平台的可选步骤：

5. 设置 VSSCRIPT_PATH 环境变量，以便其他应用找到该库；可通过 ``vapoursynth get-vsscript`` 获取路径

至此安装完成。如果你想使用 VSRepo，可直接运行 ``pip install vsrepo`` 安装。

完成第二步后，你可以打开 Python 命令行并输入以下内容进行测试::

   from vapoursynth import core
   print(str(core))

在最后一行按回车后，你应该看到版本号以及描述实例化 Core 对象时所用选项的几行信息。实际上，这些行应该与 ``vspipe --version`` 的输出结果相同。

Windows 安装器
******************

前提条件
-------------

首先下载并安装以下前置依赖：
   * `Python 64 bit version <http://www.python.org/>`_ -- 支持 Python 3.12 及其后续版本，包括 3.13 和 3.14。

安装
------------

直接运行 `VapourSynth installer <https://github.com/vapoursynth/vapoursynth/releases>`_。

安装器会执行通用安装步骤，并提供一些附加选项。

Windows 便携版
****************

下载并运行自动脚本 *Install-Portable-VapourSynth-RXX.ps1*。
它会自动下载并配置嵌入式 Python、pip、VapourSynth 和 VSRepo，默认安装到名为 *vapoursynth-portable* 的子目录。
你也可以向脚本传参，以指定 Python 版本或启用无人值守模式。

请注意，Python 设计上会将当前路径硬编码进 *Scripts* 目录中的 exe 文件，从严格意义上说这会影响可移植性。为缓解该问题，
便携安装脚本会删除这些 exe，并在便携目录根部提供一组 bat 文件（vspipe.bat、vsrepo.bat、pip.bat）以降低使用成本。
你仍可通过 ``python -m <module> <arguments>`` 调用几乎所有 Python 模块。

非官方软件包
###################

请将所有打包问题报告给相应的维护者，不要在 VAPOURSYNTH 的缺陷跟踪器上报告！

多个包管理器中都有由第三方维护的 VapourSynth 软件包。下列来源通常会保持较新的版本。

macOS（旧称 OSX）
********************

Homebrew 上有由其他人维护的 VapourSynth 软件包，通常保持更新。

请将所有打包问题报告给相应的维护者，不要在 VAPOURSYNTH 的缺陷跟踪器上报告！

首先下载并安装前置依赖：
   * Xcode -- 可从 AppStore 获取
   * `Homebrew <http://brew.sh/>`_ -- 包管理器

在终端运行以下命令并等待完成::

   brew install vapoursynth

Debian（德比安）
****************

VapourSynth 软件包由 `deb-multimedia repository <https://www.deb-multimedia.org/>`_ 提供。
你需要先按其官方网站指南添加该仓库。

Fedora、CentOS 和 RHEL
***********************

Fedora 可直接从官方仓库安装 VapourSynth 软件包。
CentOS 和 RHEL 需要先安装 EPEL（Extra Packages for Enterprise Linux）仓库。

Gentoo（发行版）
****************

有一个 `unofficial Portage tree <https://github.com/4re/vapoursynth-portage>`_，包含与 VapourSynth 相关的 ebuild。
更多信息和使用说明请查看该 GitHub 链接。

Arch Linux（发行版）
*********************

`VapourSynth-related packages <https://www.archlinux.org/packages/?q=vapoursynth>`_ 由 Community 仓库提供。

Nix 和 NixOS
*************
``vapoursynth`` 在 nixpkgs 中可用，可通过 ``nixpkgs#vapoursynth`` 或 ``nixpkgs#python3Packages.vapoursynth`` 获取（当前仅在 unstable 分支可用）。请注意该 derivation 在 macOS 上不能正常工作。

VapourSynth 的发布版本不会回移到当前稳定分支。要获取最新版本请使用 unstable 分支。

自行编译
#####################

Windows 编译
*******************

在 Windows 上准备构建环境
------------------------------------------

所有项目和脚本都假设使用默认安装路径，如果你更改了路径，请准备好调整许多设置

所需软件：

* 需要 `Visual Studio 2026 <https://visualstudio.microsoft.com/vs/>`_
* 还需要 `64bit <https://www.python.org/>`_ Python 3.14.x（msvc 项目假定你按“所有用户”方式安装了 Python）
* 需要 `InnoSetup <http://www.jrsoftware.org/isdl.php>`_ 来创建安装程序（假设使用默认安装路径）

准备工作
----------------

* 克隆 VapourSynth
* 运行 ``install_deps.bat``

如果你已经安装 VapourSynth，这会把依赖放到正确位置。或者你也可以手动完成每一步：

* 克隆 VapourSynth 仓库
* 将 zimg 克隆到 VapourSynth 目录 (``git clone https://github.com/sekrit-twc/zimg --recurse-submodules``)
* 将 libp2p 克隆到 VapourSynth 目录 (``git clone https://github.com/sekrit-twc/libp2p``)

编译
-----------

* 运行 ``compile_all.bat``。

Linux、OS X 及其他平台编译
**********************************

需要以下依赖：

* Meson 1.3.0 或更高版本
* ninja-build（Ninja 构建工具）
* pkg-config（包配置工具）
* GCC 或 Clang，且版本需支持 C++17
* `zimg <https://github.com/sekrit-twc/zimg>`_ 图像处理库
* Python 3.12 或更高版本
* 在 Python 3 环境中安装 Cython 3.1.x 或更高版本
* 用于文档的 Sphinx（可选）

编译
-----------

* 克隆 VapourSynth 仓库

进入 VapourSynth 目录并运行以下命令进行编译与安装::

   python -m build --wheel

然后你可以安装 dist 目录下生成的 wheel。

或者你也可以不克隆仓库，直接让 pip 从 GitHub 安装::

   pip install git+https://github.com/vapoursynth/vapoursynth.git

文档可通过其自带的 Makefile 构建::

   $ make -C doc/ html

可以使用标准程序 ``cp`` 安装文档。

插件和脚本
###################

如果你在寻找插件和脚本，最完整的列表之一可以在 `vsdb.top <http://vsdb.top/>`_ 找到。

使用 VSRepo 安装
**********************

在 Windows 上，你可以使用自带的 vsrepo.py 来安装和升级插件和脚本。

直接运行 ``vsrepo install <namespace or identifier>`` 即可安装。

若需要查看已知插件和脚本列表，可运行 ``vsrepo available`` 或访问 `vsdb.top <http://vsdb.top/>`_。

更多信息请访问 `vsrepo's repository <https://github.com/vapoursynth/vsrepo>`_

手动安装
*******************

你可以将插件 (``.dll``) 和脚本 (``.py``) 放在你认为方便的位置。

对于插件，你可以使用 ``std.LoadPlugin`` 函数加载。还有一个插件自动加载机制来节省时间，详见下方。

对于脚本，你应将相对路径添加到 ``python<your_python_version>._pth``，然后即可在脚本中直接导入。

插件自动加载
******************

VapourSynth 会自动递归加载位于 ``<site-packages>/vapoursynth/plugins`` 的所有原生插件。自动加载行为与手动加载基本一致，唯一例外是
加载插件时遇到的错误会被静默忽略。

你也可以通过设置 VAPOURSYNTH_EXTRA_PLUGIN_PATH 环境变量来追加插件路径。该路径会在默认插件路径之后加载。