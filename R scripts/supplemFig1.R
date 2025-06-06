# LONG TERM MEMORY EFFECT ----
library(dplyr)
library(ggplot2)
library(readr)

## Get data ----

df_mem1 <- readRDS("data/mod_ltm1.rds")
df_mem2 <- readRDS("data/mod_ltm2.rds")
df_mem3 <- readRDS("data/mod_ltm3.rds")
df_mem4 <- readRDS("data/mod_ltm4.rds")
df_mem5 <- readRDS("data/mod_ltm5.rds")
df_mem6 <- readRDS("data/mod_ltm6.rds")

## Supp. Fig. 1a: LTM effect ----

q1 = ggplot(df_mem1, aes(x = card, y = est)) +
  geom_line(linewidth = 0.5, color = "#D65740") +
  geom_abline(intercept = 0, slope = 1, linetype = "dashed", size = 0.25) +
  xlim(0,40) +
  ylim(0,40) +
  theme_classic() +
  ylab("Estimate") +
  xlab("Quantity")

q2 = q1 + 
  geom_line(data = df_mem2, aes(x = card, y = est),
            linewidth = 0.5,
            color = "#6BBAD3")

q3 = q2 + 
  geom_line(data = df_mem3, aes(x = card, y = est),
            linewidth = 0.5,
            color = "#449E88")

q4 = q3 + 
  geom_line(data = df_mem4, aes(x = card, y = est),
            linewidth = 0.5,
            color = "#415485")

q5 = q4 + 
  geom_line(data = df_mem5, aes(x = card, y = est),
            linewidth = 0.5,
            color = "#E8A085")

q6 = q5 + 
  geom_line(data = df_mem6, aes(x = card, y = est),
            linewidth = 0.5,
            color = "#7D3C98")
q6

# SHORT TERM MEMORY EFFECT ----

## Get data ----

df_stm0 <- readRDS("data/mod_stm0.rds")
df_stm7 <- readRDS("data/mod_stm7.rds")
df_stmInf <- readRDS("data/mod_stmInf.rds")


## Supp. Fig. 1a: LTM effect ----

q1 = ggplot(df_stm0, aes(x = card, y = est)) +
  geom_line(linewidth = 0.5, color = "#D65740") +
  geom_abline(intercept = 0, slope = 1, linetype = "dashed", size = 0.25) +
  xlim(0,40) +
  ylim(0,40) +
  theme_classic() +
  ylab("Estimate") +
  xlab("Quantity")

q2 = q1 + 
  geom_line(data = df_stm7, aes(x = card, y = est),
            linewidth = 0.5,
            color = "#6BBAD3")

suppfig1 = q2 + 
  geom_line(data = df_stmInf, aes(x = card, y = est),
            linewidth = 0.5,
            color = "#7D3C98")
suppfig1

