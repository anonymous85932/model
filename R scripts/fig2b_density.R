# ESTIMATION DENSITY PLOT
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

# Get density curves ----
df1$type <- as.factor(df1$type)

df13 = df1 %>% 
  dplyr::filter(card == 1, type == "human")

d = df1[df1$card == 1,]
q1 = ggplot(d, aes(x = est)) +
  geom_histogram(data = d[d$type == "human", ], binwidth = 1, aes(y = ..density..), fill = "#D65740", color = "black", alpha = 0.5, linewidth = 0.5) +
  geom_density(data = d[d$type == "model", ], adjust = 9.5, fill = "#D65740", color = "black", alpha = 0.4, linewidth = 0.5) +
  # For new data: Run the line below to get the max point of the density curve. Fix the "adjust" parameter accordingly.
  # geom_point(aes(x = 1, y = sum(d$est == 1)/nrow(d))) +
  ylim(0,1) +
  xlim(0,40) +
  labs(x = "", y = "")

d = df1[df1$card ==3,]
q3 = q1 +  geom_histogram(data = d[d$type == "human", ], binwidth = 1, aes(y = ..density..), fill = "#449E88", color = "black", alpha = 0.5, linewidth = 0.5) +
  # geom_point(aes(x = 3, y = sum(d$est == 3)/nrow(d))) +
  geom_density(data = d[d$type == "model", ], adjust = 2.5, fill = "#449E88", color = "black", alpha = 0.4, linewidth = 0.5)

d = df1[df1$card ==7,]
q7 = q3 +  geom_histogram(data = d[d$type == "human", ], binwidth = 1, aes(y = ..density..), fill = "#E8A085", color = "black", alpha = 0.5, linewidth = 0.5) +
  # geom_point(aes(x = 7, y = sum(d$est == 7)/nrow(d))) +
  geom_density(data = d[d$type == "model", ], adjust = 1.4, fill = "#E8A085", color = "black", alpha = 0.4, linewidth = 0.5)

d = df1[df1$card ==15,]
q15 = q7 +  geom_histogram(data = d[d$type == "human", ], binwidth = 1, aes(y = ..density..), fill = "#6BBAD3", color = "black", alpha = 0.5, linewidth = 0.5) +
  # geom_point(aes(x = 15, y = sum(d$est == 15)/nrow(d))) +
  geom_density(data = d[d$type == "model", ], adjust = 1,  fill = "#6BBAD3", color = "black", alpha = 0.4, linewidth = 0.5) 

d = df1[df1$card ==30,]
q30 = q15 +  geom_histogram(data = d[d$type == "human", ], binwidth = 1, aes(y = ..density..), fill = "#415485", color = "black", alpha = 0.5, linewidth = 0.5) +
  # geom_point(aes(x = 30, y = sum(d$est == 30)/nrow(d))) +
  geom_density(data = d[d$type == "model", ], adjust =0.3, fill = "#415485", color = "black", alpha = 0.4, linewidth = 0.5) 

# Fig. 2b : Density plot ----

fig2b = q30 +
  theme_classic() +
  labs(x = "Estimate", y = "Density")
fig2b



