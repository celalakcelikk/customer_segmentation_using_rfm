# Customer Segmentation using RFM (RFM kullanarak Müşteri Segmentasyonu)
<p align="center">
  <img src="https://github.com/celalakcelikk/customer_segmentation_using_rfm/blob/main/media/rfm1.png" alt="rfm"/>
<p>
  
## İş Problemi
Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istemektedir.

Şirket, ortak davranışlar sergileyen müşteri segmentleri özelinde pazarlama çalışmaları yapmanın gelir artışı sağlayacağını düşünmektedir.

Örneğin şirket için çok kazançlı olan müşterileri elde tutmak için farklı kampanyalar, yeni müşteriler için farklı kampanyalar düzenlenmek istenmektedir.

Müşterileri **RFM yöntemi** ile segmentlere ayırınız.

## Veri Seti Hikayesi
* **Online Retail II** isimli veri seti İngiltere merkezli online bir satış mağazasının 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içermektedir.
* Bu şirketin ürün kataloğunda hediyelik eşyalar yer almaktadır. 
* Şirketin müşterilerinin büyük çoğunluğu kurumsal müşterilerdir.

## Veri Seti Değişkenleri
* **Invoice:** Fatura Numarası. Eğer bu kod C ile başlıyorsa işlemin iptal edildiğini ifade eder.
* **StockCode:** Ürün kodu. Her bir ürün için eşsiz numara.
* **Description:** Ürün ismi 
* **Quantity:** Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
* **InvoiceDate:** Fatura tarihi 
* **UnitPrice:** Fatura fiyatı (Sterlin)
* **CustomerID:** Eşsiz müşteri numarası 
* **Country:** Ülke ismi
