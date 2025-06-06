# ADJUSTMENT EFFECT ----
library(dplyr)
library(ggplot2)
library(readr)

## Get data ----

mod_flex <- readRDS("data/mod100.rds")
mod_inc <- readRDS("data/mod_inc.rds")

## Supp. Fig. 3a: Estimate flex ----

df1 = rbind(mod_flex, mod_inc)

df1 <- df1 %>% 
  group_by(type, card) %>%
  summarise(
    mean_est = mean(est),
    sd = sd(est),
    se = sd(est) / sqrt(n()),
  ) %>% 
  ungroup() %>% 
  as.data.frame()

suppfig3a = ggplot(df1[df1$type == "model",], aes(x = card, y = mean_est)) +
  geom_line(size = 0.5, color = "#C85F48") +
  geom_errorbar(data = df1[df1$type == "model",], aes(x = card, ymin = mean_est - sd, ymax = mean_est + sd),
                width = 0.1,
                size = 0.1) +
  geom_abline(intercept = 0, slope = 1, linetype = "dashed", color = "black", size = 0.25) +
  xlab("Quantity") +
  ylab("Estimate") +
  scale_x_continuous(breaks = c(0,20,40),limits=c(0,40)) +
  scale_y_continuous(breaks = c(0,20,40,60), limits = c(0,60)) +
  theme_classic() 
suppfig3a

## Supp. Fig. 3b: Estimate inc ----

suppfig3b = ggplot(df1[df1$type == "adj",], aes(x = card, y = mean_est)) +
  geom_line(size = 0.5, color = "#C85F48") +
  geom_errorbar(data = df1[df1$type == "adj",], aes(x = card, ymin = mean_est - sd, ymax = mean_est + sd),
                width = 0.1,
                size = 0.1) +
  geom_abline(intercept = 0, slope = 1, linetype = "dashed", color = "black", size = 0.25) +
  xlab("Quantity") +
  ylab("Estimate") +
  scale_x_continuous(breaks = c(0,20,40),limits=c(0,40)) +
  scale_y_continuous(breaks = c(0,20,40,60), limits = c(0,60)) +
  theme_classic() 
suppfig3b

## Supp. Fig. 3c: CV mult ----

df_cv = df1[df1$type == "model",]
df_cv$cv = df_cv$sd / df_cv$mean_est

suppfig3c = ggplot(df_cv, aes(x = card, y = cv)) +
  geom_line(data = df_cv, size = 0.5, color = "#C85F48") +
  xlab("Quantity") +
  ylab("CoV") +
  scale_x_continuous(breaks = c(0,10,20,30,40),limits=c(1,40)) +
  scale_y_continuous(breaks = c(0,0.2,0.4,0.6),limits=c(0,0.6)) +
  theme_classic() 
suppfig3c

## Supp. Fig. 2d: CV inc ----

df_cv = df1[df1$type == "adj",]
df_cv$cv = df_cv$sd / df_cv$mean_est

suppfig3d = ggplot(df_cv, aes(x = card, y = cv)) +
  geom_line(data = df_cv, size = 0.5, color = "#C85F48") +
  xlab("Quantity") +
  ylab("CoV") +
  scale_x_continuous(breaks = c(0,10,20,30,40),limits=c(1,40)) +
  scale_y_continuous(breaks = c(0,0.2,0.4,0.6),limits=c(0,0.6)) +
  theme_classic() 
suppfig3d
