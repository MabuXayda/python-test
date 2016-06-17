# -*- coding: utf-8 -*-
#%%
raw = pd.read_csv(DIR + "z_train/reuseTime.csv")


#%%
#col = ["ReuseCount","ReuseAvg","ReuseMax"]
df = raw

#active = pd.merge(df, uAct[["CustomerId","Churn"]], on = "CustomerId", how = "right")
churn = pd.merge(df, uChu[["CustomerId","Churn"]], on = "CustomerId", how = "right")
churn = churn[churn["ReuseCount"] != "null"]

#df = pd.concat([active,churn])
#df = df[df["ReuseCount"] != "null"]


#%% VISUALIZE
df[col] = df[col].astype(int)
plt.figure()
bp = df.groupby("Churn").boxplot(column = col, figsize = (10,10))
plt.ylim(-10, 300)
plt.savefig(DIR + "visualize/reuseTime_pandas_boxplot.png")

#%%
temp = pd.melt(df, id_vars=["CustomerId","Churn"], value_vars = col, var_name = "Type", value_name = "Value")
temp["Value"] = temp["Value"].astype(int)
plt.figure()
bp = sns.swarmplot(x = "Type", y="Value", data = temp, hue = "Churn")
plt.ylim(-10, 300)
#plt.savefig(DIR + "visualize/reuseTime_sns_boxplot.png")
