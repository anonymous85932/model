# DISTRIBUTION
library(dplyr)
library(ggplot2)
library(readr)

# Get data ----

# Model
mod100 <- readRDS("data/mod100.rds")

# Human
hum100 <- readRDS("data/hum100.rds")

# Combine
mod100$nrow = -nrow(mod100)
hum100$nrow = nrow(hum100)
df1 = rbind(hum100, mod100)

# Graph data
df2 <- df1 %>% 
  group_by(type, est) %>%
  summarise(
    est = est[1],
    n = n()/nrow[1],
  ) %>% 
  ungroup() %>% 
  as.data.frame()

df2$type <- factor(df2$type, levels = c("model", "human"))

# Fig. 2g: Response distribution ----
fig2g <- ggplot(df2, aes(x = est, y = 100*n)) +
  geom_bar(data = df2[df2$type == "model", ], stat = "identity", width = 0.2) +
  geom_bar(data = df2[df2$type == "human", ], stat = "identity", width = 0.2) +
  geom_hline(yintercept = 0, color = "black", size = 0.5) +
  xlab("Estimate") +
  ylab("%") +
  scale_x_continuous(breaks = seq(0, 50, by = 10), limits = c(0, 50)) +
  scale_y_continuous(breaks = seq(-6, 6, by = 2), labels = c("6", "4", "2", "0", "2", "4", "6"), limits = c(-7, 7)) +
  theme_classic()
fig2g


