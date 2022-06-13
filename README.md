# Simple Library for Progress Bar

## Install
- With pipenv
    - Add private source to Pipfile
    ```
    [[source]]
    url = "http://192.168.100.236/pypi/simple"
    verify_ssl = false
    name = "home"
    ```
    - `pipenv install aclprogressbar`

## Usage

### Import
`from progress import ProgressBar`

### Use

```python
with ProgressBar(total=100, width=30, prefix="Processing...") as bar:
    bar.update(add=1)
```

### Example

```python
with ProgressBar(total=100, width=30, prefix="Processing...") as bar:
    for _ in range(total):
        bar.update(add=1)
        time.sleep(0.05)
```

## Result

`| Testing... |██████████████████████████████| 100% - 100 / 100 | TTL / ETA: 2.49s / 0.00s | AVG: 40.13/s |`

### 已支援中文 prefix

`| 處理中... |██████████████████████████████| 100% - 100 / 100 | TTL / ETA: 2.49s / 0.00s | AVG: 40.13/s |`

### 若 width == -1 則會填滿整個 terminal 長度

![](https://i.imgur.com/0NRVWob.png)