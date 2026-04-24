插件包装
****************

作为插件作者，建议并非常赞赏提供预编译的二进制文件作为 Python 轮。
VapourSynth 可以自动发现它们，Python 脚本或包可以可靠地依赖它们作为声明的依赖项。

本节介绍将插件打包和发布为轮子以及将其发布到 PyPI 所需的最少步骤。
还提供了模板和示例。

理论
==========

将插件打包为轮子并使其可以被 VapourSynth 发现可以简单地总结为
“压缩这个库并将其安装在这个位置。”

``.whl`` 文件可以非常粗略地描述为：其中的所有内容都被解压缩到 ``site-packages`` 中。
因此，VapourSynth 自动并递归地加载位于 ``<site-packages>/vapoursynth/plugins`` 中的所有本机插件。
因此，wheel 必须在此位置安装其本机文件。

在实践中
===========

一个非常简单的项目结构如下所示：

::

    path/to/your/project
    ├── src
    |  └── MyPlugin
    |     ├── myplugin.cpp
    |     └── myplugin.h
    ├── .gitattributes
    ├── .gitignore
    ├── LICENSE
    ├── hatch_build.py
    ├── meson.build
    ├── pyproject.toml
    └── README.md

在这个简单的项目中，我们使用 `Hatchling <https://hatch.pypa.io/latest/>`_ 作为 Python 构建后端。
自定义 Hatch 构建挂钩 (``hatch_build.py``) 调用 Meson 来编译本机插件，
然后将生成的二进制文件复制到 ``vapoursynth/plugins/`` 目录中。

该目录在 ``pyproject.toml`` 中声明，以便 Hatchling 将其包含在最终的轮子中。

运行 ``python -m build`` 时，``build`` 包读取 ``pyproject.toml`` 文件，解析元数据，
并让 Hatchling 创建源发行版 (sdist) 和轮子。

步骤
=====

假设您的项目已经完成并准备好部署，让我们创建 Python 项目结构。
多个构建前端，例如 `uv <https://docs.astral.sh/uv/>`_、`Poetry <https://python-poetry.org/>`_ 或 `pipx <https://pipx.pypa.io/stable/>`_
可以使这些步骤变得更容易或更快，但它们也需要额外的知识。
为了简单起见，我们在这里使用本机工具。

创建一个 `virtual environment <https://docs.python.org/3/library/venv.html>`_::

    python -m venv .venv

激活虚拟环境。在 Windows 上::

    .venv\Scripts\activate

在 Linux/macOS 上::

    source .venv/bin/activate

此时，您将需要编写 ``pyproject.toml`` 和自定义 Hatch 构建挂钩。

配置文件 ``pyproject.toml``：

.. code-block:: toml

    [build-system]
    requires = ["hatchling", "packaging", "meson"]
    build-backend = "hatchling.build"

    [project]
    name = "MyPlugin"
    version = "1.0"
    description = "MyPlugin description"
    requires-python = ">=3.12"
    readme = "README.md"
    license = "MIT"
    license-files = ["LICENSE"]
    authors = [{ name = "Name", email = "name@email.com" }]
    maintainers = [{ name = "YourName", email = "name@email.com" }]

    dependencies = ["vapoursynth>=74"]

    [tool.hatch.build.targets.wheel]
    include = ["vapoursynth/plugins"]
    artifacts = [
        "vapoursynth/plugins/*.dylib",
        "vapoursynth/plugins/*.so",
        "vapoursynth/plugins/*.dll",
    ]

    [tool.hatch.build.targets.wheel.hooks.custom]
    path = "hatch_build.py"

``include`` 指令告诉 Hatchling 将 ``vapoursynth/plugins/`` 目录打包到轮子中。
``artifacts`` 列表指定要包含哪些已编译的二进制扩展。
安装轮子后，这些文件最终位于 ``<site-packages>/vapoursynth/plugins/`` 中，VapourSynth 会在其中发现它们。

自定义 Hatch 构建挂钩 (``hatch_build.py``)：

.. code-block:: python

    import shutil
    import subprocess
    import sys
    from pathlib import Path
    from typing import Any

    from hatchling.builders.hooks.plugin.interface import BuildHookInterface
    from packaging import tags


    class CustomHook(BuildHookInterface[Any]):
        """
        Custom build hook to compile the Meson project and package the resulting binaries.
        """

        source_dir = Path("build")
        target_dir = Path("vapoursynth/plugins")

        def initialize(self, version: str, build_data: dict[str, Any]) -> None:
            """
            Called before the build process starts.
            Sets build metadata and executes the Meson compilation.
            """
            # https://hatch.pypa.io/latest/plugins/builder/wheel/#build-data
            build_data["pure_python"] = False

            # Custom platform tagging logic:
            # We avoid the default 'infer_tag' (e.g., cp314-cp314-win_amd64) to prevent needing a separate wheel
            # for every Python version.
            # Since the compiled plugin only depends on the VapourSynth API and the OS/architecture,
            # we use a more generic tag: 'py3-none-<platform>'.
            #
            # NOTE:
            # For multi-platform distribution, this script should be run in a CI environment (like cibuildwheel)
            # or driven by environment variables to inject the appropriate platform tags.
            build_data["tag"] = f"py3-none-{next(tags.platform_tags())}"

            # Setup with vsenv
            # The ``--vsenv`` flag in the Meson setup command activates the Visual Studio environment on Windows,
            # which is required for MSVC-based compilation. On Linux and macOS, this flag is safely ignored.
            subprocess.run([sys.executable, "-m", "mesonbuild.mesonmain", "setup", "build", "--vsenv"], check=True)

            # Compile
            subprocess.run([sys.executable, "-m", "mesonbuild.mesonmain", "compile", "-C", "build"], check=True)

            # Ensure the target directory exists and copy the compiled binaries
            self.target_dir.mkdir(parents=True, exist_ok=True)
            for file_path in self.source_dir.glob("*"):
                if file_path.is_file() and file_path.suffix in [".dll", ".so", ".dylib"]:
                    shutil.copy2(file_path, self.target_dir)

        def finalize(self, version: str, build_data: dict[str, Any], artifact_path: str) -> None:
            """
            Called after the build process finishes.
            Cleans up temporary build artifacts.
            """
            shutil.rmtree(self.target_dir.parent, ignore_errors=True)

.. warning::

    平台标签逻辑（``py3-none-<platform>``）会生成与当前操作系统和架构绑定的 wheel。
    若要进行多平台分发，请使用 `cibuildwheel <https://cibuildwheel.pypa.io/en/stable/>`_ 这类 CI 工具，
    为每个目标平台分别构建 wheel。

支持的重要平台有：

- Windows 平台 ``x86_64``
- Linux 平台 ``x86_64``
- Linux 平台 ``aarch64``
- macOS 平台 ``x86_64``
- macOS 平台 ``arm64``

如果您的项目无法合理地为其中之一运送轮子，请清楚地记录该限制。

安装 ``build`` 包并构建 wheel::

    pip install build
    python -m build

生成的轮子将位于 ``dist/`` 目录中，准备分发。

当然，您可以通过添加分类器、关键字和 URL 来进一步自定义 ``pyproject.toml`` 元数据，
以及设置自动版本检测或包含您自己的 Python 包装器包。

发布到 PyPI
==================

轮子构建完成后，您可以将其发布到 `PyPI <https://pypi.org/>`_ ，以便用户可以使用 ``pip install MyPlugin`` 安装您的插件。

推荐的方法是通过 GitHub Actions 使用 `Trusted Publishing <https://docs.pypi.org/trusted-publishers/>`_，
这消除了手动管理 API 令牌的需要。
有关分步指南，请参阅 `PyPA publishing tutorial <https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives>`_。

如果你更倾向于手动发布，可以使用 `twine <https://twine.readthedocs.io/en/stable/>`_::

    pip install twine
    twine upload dist/*

系统将提示您输入 PyPI 凭据或 API 令牌。

使用 CI 自动化流程
==============================

`cibuildwheel <https://cibuildwheel.pypa.io/en/stable/>`_ 等工具可以极大地简化自动化流程，为所有三个平台提供轮子。

一些例子：

- 参考：`VapourSynth-EdgeMasks CI workflow <https://github.com/HolyWu/VapourSynth-EdgeMasks/blob/436651859e5a192e56304551686cfc75a5383c3b/.github/workflows/build.yml>`_
- 参考：`bestsource CI workflow <https://github.com/vapoursynth/bestsource/blob/e31fa7722706895109ae7a6b15fb3492e96402c0/.github/workflows/build.yml>`_

具体例子
=================

- `vs-package-poc <https://github.com/Ichunjo/vs-package-poc/tree/master>`_ — 多后端打包概念验证
- `VapourSynth-EdgeMasks <https://github.com/HolyWu/VapourSynth-EdgeMasks>`_ — 具有简单 CI 的真实插件
- `bestsource <https://github.com/vapoursynth/bestsource>`_ — 具有复杂 CI 的真实插件
