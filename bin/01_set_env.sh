
## Install Miniconda3
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"

## Install numpy, scipy and and dependencies on Python side
conda install -c conda-forge  -y numpy scipy libiconv libxml2 lxml scikit-sparse

## Install R and rpy2
conda install -c r -y r-base=3.5.0
pip install rpy2

## Check R
which -a R
R -e 'sessionInfo()'