# N1 redroid Release 上传 403 调试记录

## Observations

- 失败 run：`25217583575`
- 工作流：`编译 N1 Redroid 6.18 内核`
- 失败步骤：`上传 N1 Redroid 内核到 Release`
- 前置步骤均成功，说明内核编译和产物输出没有问题。
- 失败日志为：
  - `Error 403: Resource not accessible by integration`
  - 对应接口：`POST /repos/{owner}/{repo}/releases`
- 仓库当前 Actions 默认工作流权限为：
  - `default_workflow_permissions: read`
- 当前专用 workflow 没有显式声明 `permissions`。

## Hypotheses

### H1：`GITHUB_TOKEN` 只有只读权限，创建 Release 时被 GitHub 拒绝（ROOT HYPOTHESIS）
- Supports:
  - 失败接口是创建 Release，属于 `contents` 写操作。
  - 仓库 Actions 默认权限被现场查到是 `read`。
  - 当前 workflow 没有声明 `permissions: contents: write`。
  - 报错是典型的 `Resource not accessible by integration`。
- Conflicts:
  - 暂无直接冲突证据。
- Test:
  - 在 workflow 中显式增加 `permissions: contents: write`，重新触发一次同工作流。

### H2：`ncipollo/release-action` 参数不完整，导致不是权限问题而是发布参数错误
- Supports:
  - 失败发生在第三方 action 内部。
- Conflicts:
  - 参数缺失或 tag 冲突通常更接近 `422` 或业务校验错误，不是 `403`。
  - 当前日志已明确指向 GitHub Releases 创建接口的权限拒绝。
- Test:
  - 不改参数，仅补 token 写权限；若成功，则排除该假设。

### H3：Release tag `kernel_n1_redroid_6.18` 的状态异常，导致 GitHub 拒绝写入
- Supports:
  - 上传步骤确实涉及 tag / release 状态。
- Conflicts:
  - tag 或 release 状态异常更常见于已存在、冲突、不可更新等错误，通常不是 integration 权限 403。
  - 日志没有提示 tag 已存在或 release 状态冲突。
- Test:
  - 保持 tag 不变，仅补 token 写权限；若成功，则排除该假设。

## Experiments

### E1：查询 run 失败日志与仓库 Actions 权限
- Change:
  - 不改代码，只读取 run 失败日志和仓库 Actions 默认权限。
- Expected:
  - 若 H1 正确，应看到 Release 创建 403，且仓库默认权限为 `read`。
- Result:
  - 已确认失败步骤为 Release 上传；
  - 已确认错误为 `Error 403: Resource not accessible by integration`；
  - 已确认仓库默认工作流权限为 `read`。
- Conclusion:
  - H1 被显著加强，H2/H3 暂无新增支持证据。

## Root Cause

专用 workflow 未显式申请 `contents: write`，而仓库默认 `GITHUB_TOKEN` 仅有 `read`，导致 Release 创建接口被 GitHub 拒绝。

## Fix

- 在 `compile-kernel-n1-redroid-6.18.yml` 中显式声明 `permissions: contents: write`
- 补充回归校验，确保后续不会再漏掉该权限声明
