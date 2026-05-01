# N1 6.18 Redroid 内核 GitHub Actions 计划

## 待办清单

- [x] 新增专用 GitHub Actions 工作流：为 N1 / redroid 场景编译 `6.18.y` 内核，避免改动现有通用 `compile-kernel.yml`
- [x] 在工作流中于编译前拉取上游 `stable` 的 `config-6.18`，并仅覆盖：
  - `CONFIG_PSI=y`
  - `CONFIG_PSI_DEFAULT_DISABLED=n`
- [x] 让工作流通过现有复合 Action 的 `kernel_config` 参数注入运行时生成的配置模板，复用当前内核编译链路
- [x] 为该专用产物设置独立的 Release Tag：`kernel_n1_redroid_6.18`，避免覆盖现有 `kernel_stable`
- [x] 补充最小必要说明，明确该工作流用于 N1 redroid / Docker 场景
- [x] 执行受影响范围内的最小充分验证：YAML 结构检查、关键脚本路径核对、Git diff 复核

## 方案说明

### 目标

通过 GitHub Actions 产出适用于 N1（`s905d`）redroid Docker 准备场景的 `6.18.y` 内核，并确保 PSI 相关配置在最终模板中生效。

### 现状

- 仓库已经存在通用内核编译工作流 `D:\code\amlogic-s9xxx-armbian\.github\workflows\compile-kernel.yml`
- 该工作流已经支持 `6.18.y`
- 复合 Action 已支持通过 `kernel_config` 注入自定义 `config-*` 模板
- 本仓库当前 `D:\code\amlogic-s9xxx-armbian\compile-kernel\tools\config` 目录为空，仅有 `.gitkeep`

### 推荐方案

新增一个**专用工作流**，在运行时下载上游 `config-6.18` 到工作区，再只改 PSI 两项配置，然后把该目录作为 `kernel_config` 传给现有 Action。

### 取舍说明

- 不直接修改现有通用工作流：避免影响已有稳定内核发布链路
- 不把完整 `config-6.18` 静态提交进仓库：避免引入大体积、高维护成本的配置快照
- 不改底层编译脚本：当前需求只需一个定制构建入口，运行时生成配置更小、更稳

### 计划修改文件

- `D:\code\amlogic-s9xxx-armbian\.github\workflows\` 下新增 1 个专用工作流文件
- 如有必要，补充 1 处中文说明文档

## 复盘小结

本次按“新增专用工作流 + 运行时生成配置模板”完成交付，未改动底层通用编译逻辑；验证已覆盖 YAML 结构、关键字段与补丁格式检查。
