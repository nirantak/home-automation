# Home Automation

## Home automation tools and scripts

- [Hue Lights](https://github.com/nirantak/home-automation/tree/main/hue)

## Setting Up

Python 3.9+ required

```bash
git clone git@github.com:nirantak/home-automation.git
cd home-automation
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip wheel setuptools
pip install -U -r requirements.txt
# To set up pre-commit hooks, required for contributing code, run:
pre-commit install --install-hooks --overwrite
```
