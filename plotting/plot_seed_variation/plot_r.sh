# PREC
Rscript plot_prec.r data/prec_ATF-Ads-DMOZ.csv data_figures/prec_ATF-Ads-DMOZ.pdf "Combination" ""
Rscript plot_prec_smallfont.r data/prec_ATF-Forum-DMOZ.csv data_figures/prec_ATF-Forum-DMOZ.pdf "Combination" ""
Rscript plot_prec.r data/prec_SEC-DMOZ.csv data_figures/prec_SEC-DMOZ.pdf "Combination" ""
Rscript plot_prec_smallfont.r data/prec_Escort-DMOZ.csv data_figures/prec_Escort-DMOZ.pdf "Combination" ""

cp data_figures/prec_ATF-* ~/workspace/website-discovery/paper/figures/seed_variation/
