# INDIVIDUAL EXAMPLE PLOTS
library(dplyr)
library(ggplot2)
library(readr)

# Get data ----
df1 <- readRDS("data/hum100.rds")

# Get sample of 25 individuals ----
ids = unique(df1$id)[1:25]
reduced_df = df1 %>% filter(id %in% ids)

suppfig4 = ggplot(reduced_df, aes(x = card, y = est)) +
  geom_point(size = 0.2) +
  ylab("Estimate") +
  xlab("Quantity") +
  geom_abline(intercept = 0, slope = 1, size=0.1, linetype = "dashed") +
  facet_wrap(~id, ncol = 5, scales = "fixed")
suppfig4
