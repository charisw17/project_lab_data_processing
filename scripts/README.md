# Scripts

this is for ...

## How to use

In the terminal run:

```bash
ls *.ipynb | entr jupytext --sync /_
```

this will sync the ``.ipynb`` notebook with its generated ``.py`` file so you can see the real changes and track them in git.
No need to modify the ``.py`` file

If you need to (for some reason) revert back the ``.ipynb`` file from the ``.py`` file - so sync in the other direction.
Run below command once manually. 

```bash
jupytext --to ipynb multiple_file_analysis.py
```
