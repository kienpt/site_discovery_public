mkdir data_pdf
Rscript plot_harvestrate.r data/ads_harvestrate.csv data_pdf/ads_harvestrate.pdf "ATF Ads Domain"
Rscript plot_harvestrate.r forum/forum_harvestrate.csv data_pdf/forum_harvestrate.pdf "ATF Forum Domain"
