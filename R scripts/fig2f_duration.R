# STIMULUS DURATION EFFECT 
library(dplyr)
library(ggplot2)
library(readr)

# Get data ----

# Model
mod100 <- readRDS("data/mod100.rds")
mod500 <- readRDS("data/mod500.rds")
mod1000 <- readRDS("data/mod1000.rds")

# Human
hum100 <- readRDS("data/hum100.rds")
hum500 <- readRDS("data/hum500.rds")
hum1000 <- readRDS("data/hum1000.rds")

# Fig 2f: Duration effect ----

## 100 ms ----
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

q1 = ggplot(df1, aes(x = card, y = mean_est)) +
  geom_line(size = 0.5, color = "#C85F48") +
  geom_errorbar(data = df1, aes(x = card, ymin = mean_est - se, ymax = mean_est + se),
                width = 0.1,
                size = 0.1) +
  xlab("Quantity") +
  ylab("Estimate") +
  scale_x_continuous(breaks = c(0,10,20,30,40)) +
  scale_y_continuous(breaks = c(0,20,40,60), limits=c(0,60)) +
  theme_classic() +
  facet_wrap(~type)

## 500 ms ----
df2 = rbind(hum500, mod500)

df2 <- df2 %>% 
  group_by(type, card) %>%
  summarise(
    mean_est = mean(est),
    sd = sd(est),
    se = sd(est) / sqrt(n()),
  ) %>% 
  ungroup() %>% 
  as.data.frame()

df2$type <- factor(df2$type, levels = c("model", "human"))

q2 = q1 + 
  geom_line(data = df2, aes(x = card, y = mean_est),
            size = 0.5,
            color = "#449E88") +
  geom_errorbar(data = df2, aes(x = card, ymin = mean_est - se, ymax = mean_est + se),
                width = 0.1,
                size = 0.1)

## 1000 ms ----
df3 = rbind(hum1000, mod1000)

df3 <- df3 %>% 
  group_by(type, card) %>%
  summarise(
    mean_est = mean(est),
    sd = sd(est),
    se = sd(est) / sqrt(n()),
  ) %>% 
  ungroup() %>% 
  as.data.frame()

df3$type <- factor(df3$type, levels = c("model", "human"))

q3 = q2 +
  geom_line(data = df3, aes(x = card, y = mean_est),
            size = 0.5,
            color = "#6BBAD3") +
  geom_errorbar(data = df3, aes(x = card, ymin = mean_est - se, ymax = mean_est + se),
                width = 0.1,
                size = 0.1)
fig2f = q3 

fig2f

