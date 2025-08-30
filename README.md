# Monte Carlo Option Pricer + Greeks

Monte Carlo pricer for European call options under Black–Scholes with:
- Antithetic & control-variate variance reduction
- Pathwise / CRN-bump Greeks ($\Delta$, $\Gamma$, $\nu$)

Deployed live here: [Streamlit App](https://YOUR-DEPLOYED-LINK)


## Quick start

### Cloning & Environment
```bash
# clone and create env
git clone https://github.com/YOUR-USERNAME/mc_pricer.git
cd mc_pricer
conda create -n mc_pricer python=3.12
conda activate mc_pricer

# install deps
pip install -r requirements.txt

# run streamlit app
streamlit run app_streamlit.py
```


### Adding Changes  
```bash 
# Update new requirements 
pip freeze > requirements.txt
```