# ANCHOR & ADJUSTMENT PLOT 

library(dplyr)
library(ggplot2)
library(readr)

# Get data ----

# Model
mod100 <- readRDS("data/mod100.rds")
mod_ref10 <- readRDS("data/mod_ref10.rds")
mod_ref50 <- readRDS("data/mod_ref50.rds")

# Human
hum100 <- readRDS("data/hum100.rds")
hum_ref10 <- readRDS("data/hum_ref10.rds")
hum_ref50 <- readRDS("data/hum_ref50.rds")

# Fig. 3: Anchor effect ----

## no reference ----

df1 = rbind(hum100, mod100)

df1 <- df1 %>% 
  group_by(type, card) %>%
  summarise(
    mean_est = mean(est),
    sd = sd(est),
    se = sd(est) / sqrt(n()),
  ) %>% 
  ungroup() %>%
  mutate(est = mean_est) %>%
  as.data.frame()

df1$type <- factor(df1$type, levels = c("model", "human"))

q1 = ggplot(df1, aes(x = card, y = est)) +
  geom_line(size = 0.5, color = "#C85F48") +
  geom_errorbar(data = df1, aes(x = card, ymin = mean_est - se, ymax = mean_est + se),
                width = 0.1,
                size = 0.1) +
  xlab("Quantity") +
  ylab("Estimate") +
  scale_x_continuous(breaks = c(0,20,40)) +
  scale_y_continuous(breaks = c(0,20,40,60), limits = c(0,60)) +
  theme_classic() +
  facet_wrap(~type)

## reference 50 ----

df2 = rbind(hum_ref50, mod_ref50)

df2 <- df2 %>% 
  group_by(type, card) %>%
  summarise(
    mean_est = mean(est),
    sd = sd(est),
    se = sd(est) / sqrt(n()),
  ) %>% 
  ungroup() %>%
  mutate(est = mean_est) %>%
  as.data.frame()

df2$type <- factor(df2$type, levels = c("model", "human"))

q2 = q1 + 
  geom_line(data = df2, aes(x = card, y = est),
              linewidth = 0.5,
              color = "#6BBAD3") +
  geom_errorbar(data = df2, aes(ymin = est - se, ymax = est + se), width = 0.1, size =  0.1) +
  theme(strip.background = element_blank(), strip.text = element_blank())

## reference 10 ----

df3 = rbind(hum_ref10, mod_ref10)

df3 <- df3 %>% 
  group_by(type, card) %>%
  summarise(
    mean_est = mean(est),
    sd = sd(est),
    se = sd(est) / sqrt(n()),
  ) %>% 
  ungroup() %>%
  mutate(est = mean_est) %>%
  as.data.frame()

df3$type <- factor(df3$type, levels = c("model", "human"))

q3 = q2 + 
  geom_line(data = df3, aes(x = card, y = est),
            linewidth = 0.5,
            color = "#449E88") +
  geom_abline(intercept = 0, slope = 1, linetype = "dashed", size = 0.25) +
  geom_errorbar(data = df3, aes(ymin = est - se, ymax = est + se), width = 0.1, size = 0.1) +
  facet_wrap(~type, ncol = 2, scales = "free_y")
fig3 = q3
fig3

