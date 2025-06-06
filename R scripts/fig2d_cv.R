# COEFFICIENT OF VARIANCE
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
df_cv = df1
df_cv$cv = df_cv$sd / df_cv$mean_est

# Fig. 2d: Coefficient of Variance curves ----
fig2d = ggplot(df_cv, aes(x = card, y = cv)) +
  geom_line(data = df_cv[df_cv$type == "human",], size = 0.5, color = "#C85F48") +
  geom_line(data = df_cv[df_cv$type == "model",], size = 0.5, color = "#C85F48") +
  xlab("Quantity") +
  ylab("CoV") +
  scale_x_continuous(breaks = c(0,10, 20,30, 40), limits = c(0,40)) +
  scale_y_continuous(breaks = c(0, 0.2, 0.4, 0.6), limits = c(0,0.6)) +
  theme_classic() +
  facet_wrap(~type)
fig2d

