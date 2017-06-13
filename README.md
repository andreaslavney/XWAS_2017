# XWAS_2017
Notes and scripts for conducting X chromosome-wide association studies using the Keinan lab's XWAS 1.1 package
(http://keinanlab.cb.bscb.cornell.edu/content/xwas-v11)

XWAS (chromosome X-Wide Analysis toolSet) is a software suite for the analysis of the X chromosome in association analyses and similar studies, built on plink v1.07. It includes X-specific QC functions and statistical tests that improve power to detect associations compared to methods that treat the X chromosome as an autosome.

The X chromosome has often been excluded from GWAS, which means that in many older data sets it was not analyzed before publication. As a result, X chromosome data sometimes requires additional preprocessing before it can be successfully be run through plink or XWAS.

Notes and example code for recommended plink data pre-processing are available in the Jupyter notebook XWAS_Preprocessing.ipynb. The custom scripts and reference files used in this notebook are available in the directory custom_scripts.

All materials were written by Andrea Slavney for Dr. Alon Keinan's research group at Cornell University (unless otherwise noted).

(Last updated June 13, 2017)

