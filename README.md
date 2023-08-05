# InvoiceGen

## Usage
Create following yaml file.

invoice.yml
```yml
# Tax rate. 
tax_rate: 0.1
# Withholding tax rate.
withhold_rate: 0.1021
# Render contact information of issuer.
render_from: yes
# Include withholding tax.
include_withhold: yes

# Invoice to info.
to:
  name: 法律事務所Steadiness 御中
  address: 〒108-0073<br>東京都港区三田2丁目2番15号<br>三田綱町デュープレックスR’s 3階
  tel: 03-6435-8073
  fax: 03-6435-8075
  email: karasawa-munou@mail.steadiness-law.jp 
 
# Invoice issuer info.
from: 
  name: 長谷川 亮太
  address: 〒270-2203 千葉県松戸市六高台2丁目78-3
  tel: 03‑6657‑5440
  fax: "-"
  email: info@chongryon.tokyo 

# Payment info.
bank:
  name: 糖質銀行 岩倉支店(700)
  type: 普通
  number: 19680418
  holder: イワマ ヨシカズ

# Details.
details:
  - descr: ガリガリ君ソーダ
    unit_price: 70
    amount: 286
    isFixTaxIncluded: no

  - descr: オランジーナ 420ml
    unit_price: 140
    amount: 89
    isFixTaxIncluded: no

  - descr: 国営セコム ビル(テナント借り)建物警備サービス 月額基本料金
    unit_price: 12800
    amount: 1
    isFixTaxIncluded: no
```

Execute python script.
```
python invoke.py ./invoice.yml
```

HTML file is generated for following path. You can print it with enable **background graphics**.
```
html/invoice.html
```

### Dependency
- PyYAML
- jinja2
