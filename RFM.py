###############################################################
# 1. Veri Hazırlama ve Anlama
###############################################################

import datetime as dt
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('display.width', 500)


##: OnlineRetailIIexcelindeki2010-2011verisiniokuyunuz.Oluşturduğunuzdataframe’inkopyasınıoluşturunuz
df_ = pd.read_excel("datasets/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()

##: Veri setinin betimsel istatistiklerini inceleyiniz.
df.head()
df.describe().T
df.shape
df.info()

##: Veri setinde eksik gözlem var mı? Varsa hangi değişkende kaç tane eksik gözlem vardır?
df.isnull().any()
df.isnull().sum()

##: Eksik gözlemleri veri setinden çıkartınız. Çıkarma işleminde ‘inplace=True’ parametresini kullanınız.
df.dropna(inplace=True)

##: Eşsiz ürün sayısı kaçtır?
df["StockCode"].nunique()

##: Hangiüründenkaçartanevardır?
df["StockCode"].value_counts().head()

##: En çok sipariş edilen 5 ürünü çoktan aza doğru sıralayınız.
df.groupby(["StockCode"]).agg({"Quantity": "sum"}).sort_values(["Quantity"], ascending=False).reset_index().head(5)

##: Faturalardaki‘C’iptaledilenişlemlerigöstermektedir.İptaledilenişlemleriverisetindençıkartınız.
df = df[~df["Invoice"].str.contains("C", na=False)]

##: Faturabaşınaeldeedilentoplamkazancıifadeeden‘TotalPrice’adındabirdeğişkenoluşturunuz.
df["TotalPrice"] = df["Price"] * df["Quantity"]


###############################################################
# 2. RFM Metriklerinin Hesaplanması
###############################################################
#: Recency, Frequency ve Monetary tanımlarını yapınız.
#: Müşteri özelinde Recency, Frequency ve Monetary metriklerini groupby, agg ve lambda ile hesaplayınız.
#: Hesapladığınız metrikleri rfm isimli bir değişkene atayınız.
#: Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz.
#: Not 1: recency değeri için bugünün tarihini (2011, 12, 11) olarak kabul ediniz.
#: Not 2: rfm dataframe’ini oluşturduktan sonra veri setini "monetary>0" olacak şekilde filtreleyiniz.

today_date = df["InvoiceDate"].max() + dt.timedelta(days=2)
today_date = today_date.replace(hour=0, minute=0, second=0)


rfm = df.groupby(["Customer ID"]).agg({"InvoiceDate": lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                       "Invoice": lambda Invoice: Invoice.nunique(),
                                       "TotalPrice": lambda TotalPrice: TotalPrice.sum()})

rfm.columns = ("recency", "frequency", "monetary")

rfm = rfm[rfm["monetary"] > 0]


###############################################################
# 3. RFM Skorlarının Oluşturulması ve Tek Bir Değişkene Çevrilmesi
###############################################################
#: Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.
#: Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz.
#: Oluşan 2 farklı değişkenin değerini tek bir değişken olarak ifade ediniz ve RFM_SCORE olarak kaydediniz.
#: Örneğin; Ayrı ayrı değişkenlerde sırasıyla 5, 2 olan recency_score, frequency_score skorlarını RFM_SCORE değişkeni isimlendirmesi ile oluşturunuz.
#: DİKKAT! Monetary skoru dahil etmiyoruz.

rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

rfm["RFM_SCORE"] = rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)


###############################################################
# 3. RFM Skorlarının Segment Olarak Tanımlanması
###############################################################
#: Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlamaları yapınız.
#: Aşağıdaki seg_map yardımı ile skorları segmentlere çeviriniz.

# RFM isimlendirmesi
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)


###############################################################
# 3. Aksiyon Zamanı!
###############################################################
#: Önemli bulduğunuz 3 segmenti seçiniz. Bu üç segmenti;
#: Hem aksiyon kararları açısından,
#: Hem de segmentlerin yapısı açısından (ortalama RFM değerleri) yorumlayınız.
#: "Loyal Customers" sınıfına ait customer ID'leri seçerek excel çıktısını alınız.

rfm[["segment", "recency", "frequency", "monetary"]].groupby(["segment"]).agg(["mean", np.median, "count"])

loyal_customers = rfm[rfm["segment"] == "loyal_customers"]

loyal_customers.to_excel("loyal_customers.xlsx")
