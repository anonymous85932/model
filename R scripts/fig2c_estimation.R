# MEAN AND SD ESTIMATES
library(dplyr)
library(ggplot2)
library(readr)

# Get data ----

# Model
mod100 <- readRDS("data/mod100.rds")

# Human
hum100 <- readRDS("data/hum100.rds")

# Combine
df1 = rbind(hum100, mod100)

# Graph data
df1 <- df1 %>% 
  group_by(type, card) %>%
  summarise(
    mean_est = mean(est),
    sd = sd(est),
    se = sd(est) / sqrt(n()),
  ) %>% 
  ungroup() %>% 
  as.data.frame()

df1$type <- factor(df1$type, levels = c("model", "human"))

# Fig. 2c: Mean and sd estimates ----

fig2c = ggplot(df1, aes(x = card, y = mean_est)) +
  geom_line(linewidth = 0.5, color = "#C85F48") +
  geom_errorbar(data = df1, aes(x = card, ymin = mean_est - sd, ymax = mean_est + sd),
                width = 0.1,
                size = 0.1) +
  geom_abline(intercept = 0, slope = 1, linetype = "dashed", color = "black", linewidth = 0.25) +
  xlab("Quantity") +
  ylab("Estimate") +
  scale_x_continuous(breaks = c(0,20,40),limits=c(0,40)) +
  scale_y_continuous(breaks = c(0,20,40,60),limits=c(0,60)) +
  xlim(0,40) +
  theme_classic() +
  facet_wrap(~type)
fig2c


