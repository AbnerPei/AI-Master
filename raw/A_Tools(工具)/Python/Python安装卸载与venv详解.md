---
创建日期: 2026-06-08T05:27:00
tags:
  - python
  - venv
  - 环境管理
category:
  - 工具
  - Python
---

## macOS 下 Python 版本现状

`macOS` 自带了系统级 `Python`（通常是 `Python 2.7` 或较旧的 `Python 3.x`），但**强烈不建议直接使用或修改系统 Python**。系统 Python 是 `macOS` 内部工具链的依赖项，删除或升级它可能导致系统功能异常。

## Python 安装

### 方式一：官方安装包（推荐新手）

从 [python.org/downloads](https://www.python.org/downloads/) 下载 `.pkg` 安装包，双击按向导完成安装。

安装后，`Python` 被放置到 `/Library/Frameworks/Python.framework/`，可执行文件在 `/usr/local/bin/python3`。

### 方式二：Homebrew 安装（推荐开发者）

`Homebrew` 是 `macOS` 上最主流的包管理器，方便安装和版本切换。

```bash
# 安装最新版 Python
brew install python@3.12
```

安装后查看版本和路径：

```bash
python3 --version
which python3
# 输出类似: /opt/homebrew/bin/python3  (Apple Silicon)
# 或       /usr/local/bin/python3       (Intel)
```

### 方式三：pyenv 多版本管理（推荐进阶用户）

当你需要在多个 `Python` 版本之间切换时，`pyenv` 是最佳选择。

```bash
# 安装 pyenv
brew install pyenv

# 安装指定 Python 版本
pyenv install 3.11.9
pyenv install 3.12.3

# 查看可安装的版本
pyenv install --list

# 查看已安装的版本
pyenv versions

# 设置全局默认版本
pyenv global 3.12.3

# 为当前项目设置局部版本
cd /path/to/project
pyenv local 3.11.9
```

> **注意**：使用 `pyenv` 时，请确保将 `pyenv` 的 `shims` 路径加入 `PATH`。在你的 `~/.zshrc` 中添加：
>
> ```bash
> eval "$(pyenv init -)"
> ```

## Python 卸载

### 卸载 Homebrew 安装的 Python

```bash
# 查看通过 brew 安装的 Python
brew list | grep python

# 卸载
brew uninstall python@3.12

# 清理残留
brew cleanup
```

### 卸载官方安装包安装的 Python

```bash
# 1. 删除 Framework
sudo rm -rf /Library/Frameworks/Python.framework/Versions/3.12

# 2. 删除 Applications 中的 Python 应用
sudo rm -rf "/Applications/Python 3.12"

# 3. 删除 /usr/local/bin 下的符号链接
ls -l /usr/local/bin | grep '../Library/Frameworks/Python.framework/Versions/3.12' | awk '{print $NF}' | xargs -I {} sudo rm -f /usr/local/bin/{}
```

### 卸载 pyenv 安装的 Python

```bash
# 卸载某个版本
pyenv uninstall 3.11.9

# 完全卸载 pyenv（如果需要）
brew uninstall pyenv
rm -rf ~/.pyenv
```

> **再次强调**：不要卸载 `macOS` 系统自带的 Python。输入 `which python3` 如果返回 `/usr/bin/python3`，说明那是系统 Python，不要动它。

---

## venv 详解

### 什么是 venv？

`venv` 是 `Python` 标准库自带的**虚拟环境工具**（`Python 3.3+` 内置），无需额外安装。它的核心作用是：

> 为每个项目创建**隔离的 Python 运行环境**，让每个项目拥有独立的 `site-packages` 目录和 `Python` 解释器副本。

### 为什么需要 venv？

没有虚拟环境时，所有项目共用同一个全局 `site-packages`，会出现以下问题：

| 问题 | 说明 |
|------|------|
| **版本冲突** | 项目 A 需要 `requests==2.28.0`，项目 B 需要 `requests==2.32.0`，全局只能装一个版本 |
| **依赖污染** | 安装项目 A 的依赖时，无意中安装了项目 B 不需要的包，导致不可预测的行为 |
| **不可复现** | 在别人电脑上 `pip install -r requirements.txt` 时，全局已有包会产生干扰 |
| **权限问题** | 全局安装可能需要 `sudo`，存在安全风险 |

### 创建与使用 venv

```bash
# 1. 创建虚拟环境（在当前目录下生成 .venv 文件夹）
python3 -m venv .venv

# 2. 激活虚拟环境
source .venv/bin/activate
# 激活后，提示符前会显示 (.venv)

# 3. 在虚拟环境中安装依赖
pip install requests
pip install -r requirements.txt

# 4. 查看当前环境的包
pip list

# 5. 锁定依赖版本
pip freeze > requirements.txt

# 6. 退出虚拟环境
deactivate

# 7. 删除虚拟环境（直接删除目录即可）
rm -rf .venv
```

### .venv 命名约定

`venv` 创建的是虚拟环境目录，目录名可以是任意的：

```bash
python3 -m venv myenv      # 命名为 myenv
python3 -m venv venv       # 命名为 venv
python3 -m venv .venv      # 命名为 .venv（点开头=隐藏目录）
```

| 命名 | 说明 |
|------|------|
| `venv` | 显式目录名，`VS Code` / `PyCharm` 等 IDE 默认识别 |
| `.venv` | 隐藏目录（点开头），不会在 `ls` 中显示，更整洁；同样是 IDE 默认识别名 |
| 自定义名（如 `env`） | 需要手动在 IDE 中配置解释器路径 |

**推荐使用 `.venv`**，原因：
- 以 `.` 开头，作为隐藏目录，不干扰项目文件浏览
- `VS Code`、`PyCharm`、`Cursor` 等主流编辑器开箱即识别
- `.gitignore` 中常见默认规则 `*.venv*` 或 `.venv/` 可直接忽略

---

## 虚拟环境路径策略

针对你提到的两个路径：

### /Users/peijianbo/Documents/AbnerPei/Notes/Obsidian/StockMaster/venv

这是**项目内模式**：`venv` 目录放在项目根目录下。

```
StockMaster/
├── venv/          ← 虚拟环境
├── src/
├── requirements.txt
└── ...
```

优点：一目了然，环境和项目绑定，删除项目即可清理环境。

### /Users/peijianbo/.venvs

这是**集中式模式**：把所有项目的虚拟环境统一放到一个目录。

```
~/.venvs/
├── stockmaster/   ← StockMaster 项目的虚拟环境
├── myapp/         ← 另一个项目的虚拟环境
└── datascience/   ← 又一个项目的虚拟环境
```

优点：项目目录更干净，多个项目可以方便地查看有哪些虚拟环境。

### 两种模式对比

| 维度 | 项目内模式（`.venv`） | 集中式模式（`~/.venvs/`） |
|------|----------------------|--------------------------|
| **便携性** | 高，跟随项目 | 低，环境与项目在不同路径 |
| **整洁度** | 一般，项目目录多一个文件夹 | 好，项目目录干净 |
| **IDE 识别** | 自动识别 | 需手动配置解释器路径 |
| **删除项目** | 自动清理环境 | 需要手动清理对应环境 |
| **多项目共享** | 不方便 | 方便 |

**建议**：日常项目推荐使用项目内模式（`.venv`），简单、便携、IDE 友好。

---

## 虚拟环境能不能共用？

**技术上可以，但不建议。**

### 可以共用的场景

当多个项目**严格使用同一套依赖且版本锁定**时，可以共用：

```bash
# 创建共用的虚拟环境
python3 -m venv ~/.venvs/shared-env

# 安装共用依赖
~/.../shared-env/bin/pip install -r common-requirements.txt

# 多个项目激活同一个环境
source ~/.venvs/shared-env/bin/activate
```

### 不建议共用的原因

1. **依赖漂移**：项目 A 升级了一个包，项目 B 可能因此崩溃
2. **不可复现**：不再能直接从 `requirements.txt` 还原环境
3. **调试困难**：出问题时不确定是哪个项目的操作改变了环境

### 正确的"共用"方式：共享锁文件，不共享环境

真正的复用是**锁定依赖版本文件**，而不是直接共用 `site-packages`：

```bash
# 项目 A 锁定依赖
cd projectA
source .venv/bin/activate
pip freeze > requirements-locked.txt

# 项目 B 使用相同的锁文件创建独立环境
cd projectB
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../projectA/requirements-locked.txt
```

这样两个项目各自有独立的 `.venv`，但依赖完全一致，互不干扰。

---

## 最佳实践总结

1. **Python 本体**：用 `Homebrew` 或 `pyenv` 安装，不要动系统 Python
2. **每个项目一个 `.venv`**：放在项目根目录，用 `python3 -m venv .venv` 创建
3. **`.gitignore` 必须忽略**：确保 `.venv/` 已加入 `.gitignore`，不要把虚拟环境提交到版本库
4. **用 `requirements.txt` 传递依赖**：不同机器、不同项目之间通过锁文件同步依赖关系
5. **`deactivate` 退出**：切换项目时先退出当前虚拟环境，再激活新项目的环境
