# -*- coding: utf-8 -*-
#%% LOAD DATA
raw = pd.read_csv(DIR + "test/logIdCount.csv")
raw = raw.replace("null", "0", regex=True)
raw = raw[raw.columns.values].astype(int)

#%%
df = raw 
describe = df.drop("CustomerId", axis = 1).describe().astype(int).transpose()
#describe.to_csv(DIR + "describe.csv")

#%% MAIN DATA
#col_error = [11,14,20,30]
#col_IPTV = [40,41,43,45,46,47,48,49,410,411,412,413,414,42,44,451,461,415,416]
#col_pay = [411,132,143,166,151]
#col_select = [41,42,52,55,15,512,57,51,18,50,40,45,54,12,16,53,13]
#col = map(str,col_pay)
#col_final = ["CustomerId"] + col
#df = raw[col_final]

col_error = ['11','20','30']
col_IPTV_fav = ['47','48','49']
col_Movie_fav = ['58','59','141','143','163','164']
col_Sport_fav = ['68','681','69','70']
col_Sub_cancel = ['142','165']
#%%
df["error"] = df[col_error].sum(axis = 1)
df["IPTV_fav"] = df[col_IPTV_fav].sum(axis = 1)
df["Movie_fav"] = df[col_Movie_fav].sum(axis = 1)
df["Sport_fav"] = df[col_Sport_fav].sum(axis = 1)
df["Sub_cancel"] = df[col_Sub_cancel].sum(axis = 1)

active = pd.merge(df[["CustomerId","error","IPTV_fav","Movie_fav","Sport_fav","Sub_cancel"]], 
                  uActNew[["CustomerId","Churn"]], on = "CustomerId", how = "right")
churn = pd.merge(df[["CustomerId","error","IPTV_fav","Movie_fav","Sport_fav","Sub_cancel"]], 
                 uChuNew[["CustomerId","Churn"]], on = "CustomerId", how = "right")
#active = pd.merge(df, uAct[["CustomerId","Churn"]], on = "CustomerId", how = "right")
#churn = pd.merge(df, uChu[["CustomerId","Churn"]], on = "CustomerId", how = "right")
#df = pd.concat([active,churn])
                 

#%% CLUSTER DATA
kmeans = KMeans(n_clusters = 8)
kmeans.fit(df.ix[:,0:17])
result = pd.DataFrame(data=kmeans.labels_, columns = ["cluster"], index = df.index)
joined = df.join(result, how = "inner")
joined.sort(["cluster"], inplace = True)

test1 = joined[joined.StopMonth == 3]
print joined["cluster"].value_counts()
print test1["cluster"].value_counts()


#%% SAMPLE DATA
df_sam1 = df[df["StopMonth"] == 0].sample(n = 4000)
df_sam2 = df[df["StopMonth"] == 3]
df_sam = pd.concat([df_sam1,df_sam2])
df_sam["Churn"] = df_sam["StopMonth"].map({0:"False", 3 : "True"})
df_sam.drop("StopMonth", axis =1 , inplace = True)

df_sam.to_csv(DIR + "train.csv", index = False)