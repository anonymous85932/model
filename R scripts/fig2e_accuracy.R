# ACCURACY
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

# Get accuracy
df1$accuracy = ifelse(df1$est == df1$card, 1, 0)

# Graph data
df1 <- df1 %>% 
  group_by(type, card) %>%
  summarise(
    mean_accuracy = mean(accuracy),
    sd = sd(accuracy),
    se = sd(accuracy) / sqrt(n()),
  ) %>% 
  ungroup() %>% 
  as.data.frame()

df1$type <- factor(df1$type, levels = c("model", "human"))

# Fig. 2e: Accuracy ----

fig2e = ggplot(df1, aes(x = card, y = mean_accuracy)) +
  geom_line(size = 0.5, color = "#C85F48") +
  geom_errorbar(data = df1, aes(x = card, ymin = mean_accuracy - se, ymax = mean_accuracy + se),
                width = 0.1,
                size = 0.1) +
  xlab("Quantity") +
  ylab("Accuracy") +
  scale_x_continuous(breaks = c(0,10,20,30,40),limits=c(0,40)) +
  scale_y_continuous(breaks = c(0,0.25,0.50,0.75,1),limits=c(0,1)) +
  theme_classic() +
  facet_wrap(~type)
fig2e

