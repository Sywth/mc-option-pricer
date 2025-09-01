# Black–Scholes Option Pricer + Greeks

Pricer for European call options under Black–Scholes assumptions. 

Deployed live [here](https://bs-option-pricer.streamlit.app/).

### Cloning & Environment
```bash
# clone and create env
git clone https://github.com/Sywth/mc-option-pricer
cd mc_pricer
conda create -n mc_pricer python=3.12
conda activate mc_pricer

# install deps
pip install -r requirements.txt

# run streamlit app
streamlit run app_streamlit.py
```


```bash 
# Update new requirements via pipreqs
pipreqs

# if not already installed; install via 
pip install pipreqs
```