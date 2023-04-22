# PACS Tester
PACS Tester 是一个用于生成和发送 DICOM 序列到 PACS 系统的小工具。该工具使用 Python 和 PyQt5 编写，可以在 Windows、Mac 和 Linux 系统上运行。

**本文件和environment.yml文件均为GPT4生成,如有错误请自行更正**

## 文件结构
以下是项目的文件结构：
```bash
.
├── source_data          # 存放参考数据
├── test_data            # 存放生成的数据，用于发送给 PACS 系统
├── ui                   # 存放 PyQt 的 UI 内容，包括 DICOMApp 类
├── utils                # 存放 DICOMManager，DICOMSender 和其他功能性工具
└── main.py              # 入口
└── README.md            # 项目说明文档

```
## 主要功能
PACS Tester 主要有以下功能：

1. 生成 DICOM 序列：根据输入的参考数据，生成指定数量的 DICOM 序列并保存到输出目录中。
2. 发送 DICOM 序列：将生成的 DICOM 序列发送到指定的 PACS 系统(同时发送所有生成的序列)。
3. 删除生成的 DICOM 序列：从输出目录中删除已生成的 DICOM 序列。
4. 日志记录：在操作过程中记录日志，便于跟踪和调试。
## 如何使用
1. 克隆或下载此仓库到本地。
2. 在项目根目录下安装所需依赖：conda env create -f environment.yml。
3. 运行 python main.py --gui, 启动GUI模式.
4. 在 GUI 中，选择参考数据所在的文件夹（source_data）和输出数据的文件夹（test_data）。
5. 指定生成的 DICOM 序列数量，然后点击 "Generate DICOM" 按钮生成 DICOM 序列。
6. 输入 PACS 系统的相关信息（AE title、主机名、端口号等），然后点击 "Send DICOM" 按钮将生成的 DICOM 序列发送到 PACS 系统。
7. 如有需要，点击 "Delete DICOM" 按钮删除输出目录中的生成的 DICOM 序列。
8. (可选的)使用命令行参数运行,可以通过python main.py -h 查看参数详情
## 开发环境
- Python 3.7+
- PyQt5
- pydicom
## 注意事项
- 请确保在使用前已正确配置 PACS 系统的信息。
- 请谨慎操作删除功能，以免误删重要数据。
- 本项目仅用于测试和学习目的，请勿用于生产环境。
- 每次发送之后,如果想继续测试,请先删除原来的数据。