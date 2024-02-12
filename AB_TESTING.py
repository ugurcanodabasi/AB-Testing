#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsx excel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBidding uygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.




#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

df = pd.read_excel("Week4_MeasurementProblems/CASE_STUDY/Part 2 - AB Testing/ab_testing.xlsx")
df.head()

maximum_bidding = pd.read_excel("Week4_MeasurementProblems/CASE_STUDY/Part 2 - AB Testing/ab_testing.xlsx", sheet_name="Control Group")
maximum_bidding.head()
average_bidding = pd.read_excel("Week4_MeasurementProblems/CASE_STUDY/Part 2 - AB Testing/ab_testing.xlsx", sheet_name="Test Group")
average_bidding.head()

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
maximum_bidding.describe().T
maximum_bidding.info()
pd.set_option('display.width', 1000)

average_bidding.describe().T

# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

merge_bidding = pd.concat([maximum_bidding, average_bidding], axis=1)
merge_bidding["Purchase"].mean()

#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.
#H0 : M1 = M2
#H1 : M1!= M2


# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz
maximum_bidding["Purchase"].mean()
average_bidding["Purchase"].mean()


#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################


# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz

#normallik varsayımı
test_stat, pvalue = shapiro(maximum_bidding["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
test_stat, pvalue = shapiro(average_bidding["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#varyans homojenliği
test_stat, pvalue = levene(maximum_bidding["Purchase"], average_bidding["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

test_stat, pvalue = ttest_ind(maximum_bidding["Purchase"],
                              average_bidding["Purchase"], equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.
maximum_bidding["Purchase"].mean()
average_bidding["Purchase"].mean()

# test sonucu p-value değeri 0.34 çıkmıştır. Yani iki grup arasında istatiksel olarak bir fark yoktur.
#satış ortalamalarına baktığımızda average bir tık önde gibi görünse de bunun tesadüf olduğu kanısına varılmıştır.


##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

#ilk olarak iki grup için normallik varsayım analizi yapıldı. average (test grubu) ve maximum (kontrol grubu) için normallik sağlanmıştır.
#akabinde karşılaştırma için homojenlik testine geçilmiştir ve p-value değeri 0.34 bulunmuş olup sonucunda t testinin kullanılmasına karar verilmiştir.



# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.
# test sonucuna göre her iki yöntem için de şu an için sonuçta bir fark görünmemektedir. müşteriye daha kapsamlı bir analiz için farklı verilen eklenmesi ve uzun vadede bir çalışma yapılmasını önerebilirim.
# diğer metrikler de incelenmelidir.
