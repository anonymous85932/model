# OUTLIER PLOTS
library(dplyr)
library(ggplot2)
library(readr)

# Get data ----

## 100 ms ----
df100 <- readRDS("data/hum100_raw.rds")
outliers100 = c(21152, 20897, 20890, 21179, 21106, 21009, 20987, 20851, 20846, 20824, 20819)
df100 = df100 %>% 
  filter(item == 'experiment',
         id %in% outliers100) %>% 
  select(card, est, id)
df100$type = "100 ms"

## 500 ms ----
df500 <- readRDS("data/hum500_raw.rds")
outliers500 = c(21123)
df500 = df500 %>% 
  filter(item == 'experiment',
         id %in% outliers500) %>% 
  select(card, est, id)
df500$type = "500 ms"

## 1000 ms ----
df1000 <- readRDS("data/hum1000_raw.rds")
outliers1000 = c(20954)
df1000 = df1000 %>% 
  filter(item == 'experiment',
         id %in% outliers1000) %>% 
  select(card, est, id)
df1000$type = "1000 ms"

## Ref 10 ----
df_ref10 <- readRDS("data/hum_ref10_raw.rds")
outliers_ref10 = c(21436, 21446, 21687, 21666, 21766)
df_ref10 = df_ref10 %>% 
  filter(id %in% outliers_ref10) %>% 
  select(card, est, id)
df_ref10$type = "ref 10"

# Add ref 50
df_ref50 <- readRDS("data/hum_ref50_raw.rds")
outliers_ref50 = c(21242, 21310, 21489, 21695, 21305, 21244)
df_ref50 = df_ref50 %>% 
  filter(id %in% outliers_ref50) %>% 
  select(card, est, id)
df_ref50$type = "ref 50"

# Combine
df1 = rbind(df100, df500, df1000, df_ref10, df_ref50)
ids = unique(df1$id)

# Plot
suppfig5 = ggplot(df1, aes(x = card, y = est)) +
  geom_point(size = 0.2) +
  scale_x_continuous(n.breaks = 6) + 
  scale_y_continuous(n.breaks = 4) + 
  ylab("Estimate") +
  xlab("Quantity") +
  facet_wrap(~id, ncol = 5, scales = "free") 
suppfig5
