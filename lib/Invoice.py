import datetime
from collections import OrderedDict
from decimal import Decimal, ROUND_HALF_UP

DEFAULT_TAX_RATE = 0.1
DEFAULT_WITHHOLD_RATE = 0.1021

class Invoice():
    def __init__(
        self, taxRate=DEFAULT_TAX_RATE, withHoldRate=DEFAULT_WITHHOLD_RATE,
        renderFrom=True, includeWithHold=False
    ):
        self.invoiceParameter = OrderedDict()

        now = datetime.datetime.now()
        strDate = now.strftime('%Y-%m-%d')
        unixTime = int(now.timestamp())
        strNumber = "{0}-{1}".format(
            now.strftime('%Y%m%d'),
            str(unixTime % 86400).zfill(5)
        )

        self.invoiceParameter['date'] = strDate
        self.invoiceParameter['number'] = strNumber
        self.invoiceParameter['taxRate'] = Decimal(str(taxRate))
        self.invoiceParameter['withHoldRate'] = Decimal(str(withHoldRate))
        self.invoiceParameter['total'] = Decimal("0")
        self.invoiceParameter['subTotal'] = Decimal("0")
        self.invoiceParameter['renderFrom'] = renderFrom 
        self.invoiceParameter['includeWithHold'] = includeWithHold

    def setTo(
        self,            
        name,
        address="-",
        tel="-",
        fax="-",
        email="-"
    ):
        self.invoiceParameter['to'] = {
            "name": name,
            "address": address,
            "tel": tel,
            "fax": fax,
            "email": email
        }
    
    def setFrom(
        self,            
        name,
        address="-",
        tel="-",
        fax="-",
        email="-"
        
    ):
        self.invoiceParameter['from'] = {
            "name": name,
            "address": address,
            "tel": tel,
            "fax": fax,
            "email": email
        }

    def setBank(
        self,            
        name,
        accountType,
        accountNumber,
        accountHolder
    ):
        self.invoiceParameter['bank'] = {
            "name": name,
            "accountType": accountType,
            "accountNumber": accountNumber,
            "accountHolder": accountHolder
        }
    
    def addDetail(
        self,            
        item,
        unitPrice,
        amount,
        isFixTaxIncluded=False
    ):
        taxRate = self.invoiceParameter['taxRate'] 
        unitPrice = Decimal(str(unitPrice))

        if not "detail" in self.invoiceParameter:
            self.invoiceParameter['detail'] = list()

        if isFixTaxIncluded:
            unitPrice = \
                (unitPrice / (1 + taxRate)).quantize(
                    Decimal('0'), 
                    rounding=ROUND_HALF_UP
                )

        itemTotalPrice = unitPrice * amount

        self.invoiceParameter['detail'].append({
            "item": item,
            "unitPrice": unitPrice,
            "amount": amount,
            "itemTotalPrice": itemTotalPrice,
            "taxRate": taxRate
        })

        self.refreshTotal()

    def refreshTotal(self):

        total = Decimal("0")
        subTotal = Decimal("0")
        taxRate = self.invoiceParameter['taxRate'] 
        withHoldRate = self.invoiceParameter['withHoldRate']
        includeWithHold = self.invoiceParameter['includeWithHold']
        for detail in self.invoiceParameter['detail']:
            subTotal += detail['itemTotalPrice']

        total = (subTotal * (1 + taxRate)).quantize(
                    Decimal('0'), 
                    rounding=ROUND_HALF_UP
                )

        withhold = (subTotal * withHoldRate).quantize(
                    Decimal('0'),
                    rounding=ROUND_HALF_UP
                )

        if (includeWithHold): 
            self.invoiceParameter['total'] = total - withhold
        else: 
            self.invoiceParameter['total'] = total

        self.invoiceParameter['subTotal'] = subTotal

    def getInvoiceParameter(self):
        return self.invoiceParameter
