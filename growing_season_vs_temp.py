"""
Analia Cabello Cano
Data present challenge

Has there been an increase in temperature trend for the growing season of Salix arctica?
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load the temperature data onto a pandas data frame
temp_data = pd.read_csv("data/qhi_temp_2017.csv")
temp_data.rename({"year": "Year"}, axis=1, inplace=True)

# Load the phenology data onto a pandas data frame
phen_data = pd.read_csv("data/qhi_phen_with_before_2017.csv")
phen_data.drop(["P1", "P3", "P4", "P6", "P7", "P1_before", "P3_before", "P4_before", "P6_before", "P7_before"], axis=1, inplace=True)
phen_data.dropna(subset=["P2", "P5"], inplace=True)
# There is only one data sample for 2001 so I am going to remove it as it is not very reliable to use the info of
# just one flower of Salix arctica
phen_data = phen_data[phen_data["Year"] > 2001]

# I select only the Salix arctica data
s_arctica = phen_data[phen_data["Spp"] == "SALARC"].copy()

# In order for the interval censoring analysis to work, we must have two columns of "response" data - one contains the
# "lower bound" - PX_before (i.e., the last day on which an event was observed to have NOT yet occurred) and an
# "upper bound" - PX (i.e., the first day on which an even was observed to have occurred). So we know that the event of
# interest happened somewhere between the upper bound and the lower bound.

# 2 - is for the leaves coming out
# 5 - is for senescence

# Rounding up to the nearest interger
# I took the values to be the mean between PX_before and PX
s_arctica["P2_mean"] = round((s_arctica["P2"]+ s_arctica["P2_before"])/2)
s_arctica["P5_mean"] = round((s_arctica["P5"]+ s_arctica["P5_before"])/2)
s_arctica["Growing_season_len"] = s_arctica["P5_mean"] - s_arctica["P2_mean"]

# Creating a new data frame with the key values I am going to need
s_arctica_summary = s_arctica[["Year", "P2_mean", "P5_mean", "Growing_season_len"]].groupby("Year").mean()
s_arctica_summary.reset_index(inplace=True)


# Merging the temperature data and the summary data
plot_vals_rough = pd.merge(temp_data, s_arctica_summary, how="outer", on="Year")

# I take only the the values for the temperature for the days that lie in the growing season
plot_1 = plot_vals_rough[(plot_vals_rough["doy"] >= plot_vals_rough["P2_mean"]) & (plot_vals_rough["doy"] <= plot_vals_rough["P5_mean"])].copy()

fig_1 = sns.jointplot(x="doy", y="temp", data=plot_1, hue="Year")
fig_1.set_axis_labels(xlabel="Day of the year", ylabel="Temperature in Celsius (only during growing season)")
plt.suptitle("Temperature recorded for growing season days", x=0.5, y=1)
fig_1.savefig("figures/figure_1.png")

# I calculate the average temperature for each growing season each year for the next plot
plot_2 = pd.DataFrame(plot_1.groupby("Year")["temp"].mean())
plot_2.reset_index(inplace=True)


fig_2, ax_2 = plt.subplots(figsize=(10, 7))
ax_2 = sns.barplot(x="Year", y="temp", data=plot_2)
ax_2.set(xlabel="Year", ylabel="Average temperature during growing season /Celsius", title="Average temperature during growing season each year")
fig_2.savefig("figures/figure_2.png")

fig_3, ax_3 = plt.subplots()
x = plot_2["Year"]
y = plot_2["temp"]
ax_3.bar(x, y, color="lightblue", zorder=0)
sns.regplot(x=x, y=y, ax=ax_3)
ax_3.set_ylim(0, None)
ax_3.set(xlabel="Year", ylabel="Average temperature during growing season /Celsius", title="Average temperature during growing season each year")
fig_3.savefig("figures/figure_3.png")

plt.show()

# I export the data frames to use them in R
plot_1.to_csv("my_data_frames/growing_season_data.csv", index=False)
plot_2.to_csv("my_data_frames/year_vs_avg_temp.csv", index=False)






