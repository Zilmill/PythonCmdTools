# PythonCmdTools
常用的一些批处理等

## 使用

> 基于 https://github.com/tiangolo/typer 使用

```bash
# 确认python 和 pip 版本为3.x

# 安装
pip install "typer[all]"

```

```python
# 示例

import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
```

### rename1 批量修改名称等
