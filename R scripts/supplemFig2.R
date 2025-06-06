# SAMPLING EFFECT ----
library(dplyr)
library(ggplot2)
library(readr)

## Get data ----

mod_mult <- readRDS("data/mod100.rds")
mod_add <- readRDS("data/mod_add.rds")

## Supp. Fig. 2a: Estimate Mult ----

df1 = rbind(mod_mult, mod_add)
df1 <- df1 %>% 
  group_by(type, card) %>%
  summarise(
    mean_est = mean(est),
    sd = sd(est),
    se = sd(est) / sqrt(n()),
  ) %>% 
  ungroup() %>% 
  as.data.frame()

suppfig2a = ggplot(df1[df1$type == "model",], aes(x = card, y = mean_est)) +
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
  
suppfig2a

## Supp. Fig. 2b: Estimate Add ----

suppfig2b = ggplot(df1[df1$type == "add",], aes(x = card, y = mean_est)) +
  geom_line(size = 0.5, color = "#C85F48") +
  geom_errorbar(data = df1[df1$type == "add",], aes(x = card, ymin = mean_est - sd, ymax = mean_est + sd),
                width = 0.1,
                size = 0.1) +
  geom_abline(intercept = 0, slope = 1, linetype = "dashed", color = "black", size = 0.25) +
  xlab("Quantity") +
  ylab("Estimate") +
  scale_x_continuous(breaks = c(0,20,40),limits=c(0,40)) +
  scale_y_continuous(breaks = c(0,20,40,60), limits = c(0,60)) +
  theme_classic() 
suppfig2b

## Supp. Fig. 2c: CV Mult ----

df_cv = df1[df1$type == "model",]
df_cv$cv = df_cv$sd / df_cv$mean_est

suppfig2c = ggplot(df_cv, aes(x = card, y = cv)) +
  geom_line(data = df_cv, size = 0.5, color = "#C85F48") +
  xlab("Quantity") +
  ylab("CoV") +
  scale_x_continuous(breaks = c(0,10,20,30,40),limits=c(1,40)) +
  scale_y_continuous(breaks = c(0,0.2,0.4,0.6),limits=c(0,0.6)) +
  theme_classic() 
suppfig2c

## Supp. Fig. 2d: CV Add ----

df_cv = df1[df1$type == "add",]
df_cv$cv = df_cv$sd / df_cv$mean_est

suppfig2d = ggplot(df_cv, aes(x = card, y = cv)) +
  geom_line(data = df_cv, size = 0.5, color = "#C85F48") +
  xlab("Quantity") +
  ylab("CoV") +
  scale_x_continuous(breaks = c(0,10,20,30,40),limits=c(1,40)) +
  scale_y_continuous(breaks = c(0,0.2,0.4,0.6),limits=c(0,0.6)) +
  theme_classic() 
suppfig2d

