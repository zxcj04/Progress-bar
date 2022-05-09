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

`| Processing... |██████████████████████████████| 100% - 100 / 100 | total: 2.49s | avg: 40.15/s | left: 0.00s |`