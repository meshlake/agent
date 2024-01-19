## 本地开发环境

1. 创建虚拟环境

```shell
python3 -m venv venv
```

2. 激活虚拟环境

```shell
source venv/bin/activate
```

3. 安装依赖

```shell
pip3 install -r requirements.txt
```

## 如果更新了依赖记得更新 requirements.txt

```shell
pip3 freeze > requirements.txt
```

## 本地运行

```shell
cd main
python3 index.py
```
