# Clustering predicted structures at the scale of the known protein universe
## Interactive supplementary

Alternatively, you install the web app locally by forking the [repository](https://github.com/jurgjn/af-protein-universe) and [setting up a conda environment](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html) as follows:
```
$ git clone git@github.com:jurgjn/af-protein-universe.git
$ cd af-protein-universe/
$ mamba create -p streamlit-env python numpy matplotlib seaborn
$ mamba run -p ./streamlit-env pip install -r requirements.txt
```

After that, run the web app locally with:
```
$ conda run -p ./streamlit-env streamlit run app_pockets.py
```
