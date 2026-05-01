"""校验 N1 redroid 6.18 内核工作流的关键结构与定制配置。"""

from pathlib import Path

import yaml


WORKFLOW_PATH = Path(
    r"D:\code\amlogic-s9xxx-armbian\.github\workflows\compile-kernel-n1-redroid-6.18.yml"
)


def main() -> None:
    """验证工作流名称、关键输入、发布标签与 PSI 定制配置。"""
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    workflow = yaml.load(text, Loader=yaml.BaseLoader)

    assert workflow["name"] == "编译 N1 Redroid 6.18 内核"
    assert workflow["permissions"]["contents"] == "write"
    assert workflow["env"]["KERNEL_VERSION"] == "6.18.y"
    assert workflow["env"]["RELEASE_TAG"] == "kernel_n1_redroid_6.18"
    assert workflow["on"]["workflow_dispatch"]["inputs"]["kernel_source"]["default"] == "unifreq"

    steps = workflow["jobs"]["build"]["steps"]
    compile_step = next(step for step in steps if step["name"] == "编译 N1 Redroid 6.18 内核")
    upload_step = next(step for step in steps if step["name"] == "上传 N1 Redroid 内核到 Release")

    assert compile_step["uses"] == "./"
    assert compile_step["with"]["kernel_version"] == "${{ env.KERNEL_VERSION }}"
    assert compile_step["with"]["kernel_config"] == "${{ env.KERNEL_CONFIG_DIR }}"
    assert compile_step["with"]["kernel_sign"] == "${{ env.KERNEL_SIGN }}"
    assert upload_step["with"]["tag"] == "${{ env.RELEASE_TAG }}"

    assert "CONFIG_PSI" in text
    assert "CONFIG_PSI_DEFAULT_DISABLED" in text
    assert "kernel-config/redroid-psi/config-6.18" in text


if __name__ == "__main__":
    main()
