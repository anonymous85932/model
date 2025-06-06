# ABSOLUTE ERROR
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

# Fig. 2h: Absolute error ----

## 100ms ----

df1 = rbind(hum100, mod100)
df1$error = abs(df1$card - df1$est)

# Grph data
df1 <- df1 %>% 
  group_by(type, card) %>%
  summarise(
    mean_error = mean(error),
    sd = sd(error),
    se = sd(error) / sqrt(n()),
  ) %>% 
  ungroup() %>% 
  as.data.frame()

df1$type <- factor(df1$type, levels = c("model", "human"))

q1 = ggplot(df1, aes(x = card, y = mean_error)) +
  geom_line(size = 0.5, color = "#C85F48") +
  geom_errorbar(data = df1, aes(x = card, ymin = mean_error - se, ymax = mean_error + se),
                width = 0.1,
                size = 0.1) +
  xlab("Quantity") +
  ylab("Absolute Error") +
  scale_x_continuous(breaks = c(0,20,40), limits = c(0,40)) +
  scale_y_continuous(breaks = c(0,20), limits = c(0,20)) +
  theme_classic() +
  
  facet_wrap(~type)

## 500ms ----

df2 = rbind(hum500, mod500)
df2$error = abs(df2$card - df2$est)

df2 <- df2 %>% 
  group_by(type, card) %>%
  summarise(
    mean_error = mean(error),
    sd = sd(error),
    se = sd(error) / sqrt(n()),
  ) %>% 
  ungroup() %>% 
  as.data.frame()

df2$type <- factor(df2$type, levels = c("model", "human"))

q2 = q1 + 
  geom_line(data = df2, aes(x = card, y = mean_error),
            size = 0.5,
            color = "#449E88") +
  geom_errorbar(data = df2, aes(x = card, ymin = mean_error - se, ymax = mean_error + se),
                width = 0.1,
                size = 0.1)

## 1000ms ----

df3 = rbind(hum1000, mod1000)
df3$error = abs(df3$card - df3$est)

df3 <- df3 %>% 
  group_by(type, card) %>%
  summarise(
    mean_error = mean(error),
    sd = sd(error),
    se = sd(error) / sqrt(n()),
  ) %>% 
  ungroup() %>% 
  as.data.frame()

df3$type <- factor(df3$type, levels = c("model", "human"))

q3 = q2 + 
  geom_line(data = df3, aes(x = card, y = mean_error),
            size = 0.5,
            color = "#6BBAD3") +
  geom_errorbar(data = df3, aes(x = card, ymin = mean_error - se, ymax = mean_error + se),
                width = 0.1,
                size = 0.1) +
  xlab("Quantity") +
  ylab("Absolute Error")

fig2h = q3
fig2h

