import json
#交易日
date_range = get_all_trade_days()
day = '2023-09-11'
preDay = str(date_range[date_range.get_loc(day)-1].date())
nextDay = str(date_range[date_range.get_loc(day)+1].date())
next2Day = str(date_range[date_range.get_loc(day)+2].date())
next3Day = str(date_range[date_range.get_loc(day)+3].date())
followDayList = [nextDay,next2Day,next3Day]

#查询1
queryInfo1 = "沪深所有非st股票" + "day + 收盘价 前复权， 和前90日区间最低价 前复权"
df1 = query_iwencai(queryInfo1)
# df1 = query_iwencai("沪深所有非st股票 20230904 收盘价 前复权， 和前120日区间最低价 前复权")

rowList = []
for index, row in df1.iterrows():
#     print(row['收盘价:前复权']) 
#     print(row['区间最低价:前复权']*1.2)
     if float(row['收盘价:前复权']) < float(row['区间最低价:前复权']) * 1.15:
        rowList.append(row)
#print(rowList)
len(rowList)

df1 = pd.DataFrame(rowList)

#查询2
queryInfo2 = "沪深所有非st股票" + day + "成交量大于" + preDay + "两倍," + day + "涨幅>5%"
df2 = query_iwencai(queryInfo2)

# queryInfo2 = "沪深所有非st股票，" + day + "涨幅>5%"
df2 = query_iwencai(queryInfo2)
# df2 = query_iwencai("沪深所有非st股票 20230904 成交量大于 20230903 两倍, 20230904 涨幅>5%")

#查询3
queryInfo3 =  day + " 5日均线斜率>-10," + day + " 10日均线斜率>-10"
df3 = query_iwencai(queryInfo3)

stockList1 = df1['股票代码'].tolist()
stockList2 = df2['股票代码'].tolist()
stockList3 = df3['股票代码'].tolist()

print(len(stockList1) )
print(len(stockList2))
print(len(stockList3))



set1 = set(stockList1)
set2 = set(stockList2)
set3 = set(stockList3)

intersection = set1.intersection(set2, set3)
# 将交集转换回列表
intersection_list = list(intersection)

print(intersection_list)
len(intersection_list)

#后续交易日收盘价

dicList = []
resList = []

for stock in intersection_list:
    dfList = []
    baseCloseDF = get_price(stock, day, day, '1d', ['close'],fq='pre')
    baseClose = baseCloseDF.iloc[0]['close']
    
    for someDay in followDayList:
        someDayCloseDF = get_price(stock, someDay, someDay, '1d', ['close'],fq='pre')
        dfList.append(someDayCloseDF)
    itemData = {'code':stock,'data':dfList}
    newData = {'code':stock}
    for item in itemData['data']:
        # print(item.index[0].strftime('%Y-%m-%d'))
        # print(item.iloc[0])
        tradeDate = item.index[0].strftime('%Y-%m-%d')
    #     # item.iloc[0]
        zhangDieFu = (item.iloc[0]['close'] - baseClose)/baseClose
        zhangDieFu = str(round(zhangDieFu * 100,2) )+"%"
        newData.update({tradeDate: zhangDieFu})
    resList.append(newData)



result_string = ','.join(intersection_list)
result_string

dfExtend = query_iwencai(result_string +' 二级行业板块')
dfExtend

for res in resList:
    searhRes01 = dfExtend.loc[dfExtend['股票代码'] == res['code'], '股票简称'].iloc[0]
    res['股票简称'] = searhRes01
    searhRes02 = dfExtend.loc[dfExtend['股票代码'] == res['code'], '所属同花顺二级行业'].iloc[0]
    res['二级行业'] = searhRes02



#
sum = 0
countAbove0 = 0
for res in resList:
    percentage_decimal = float(res[nextDay].strip('%'))/100
    sum = sum + percentage_decimal
    if percentage_decimal>0:
        countAbove0 = countAbove0 + 1

average1 = sum/len(resList)
winRate1 = countAbove0/len(resList)

sum = 0
countAbove0 = 0
for res in resList:
    percentage_decimal = float(res[next2Day].strip('%'))/100
    sum = sum + percentage_decimal
    if percentage_decimal>0:
        countAbove0 = countAbove0 + 1

average2 = sum/len(resList)
winRate2 = countAbove0/len(resList)

sum = 0
countAbove0 = 0
for res in resList:
    percentage_decimal = float(res[next3Day].strip('%'))/100
    sum = sum + percentage_decimal
    if percentage_decimal>0:
        countAbove0 = countAbove0 + 1

average3 = sum/len(resList)
winRate3 = countAbove0/len(resList)

newData = {nextDay:average1,next2Day:average2,next3Day:average3}
newData2 = {nextDay:winRate1,next2Day:winRate2,next3Day:winRate3}
resList.append(newData)
resList.append(newData2)

resJson = json.dumps(resList)
# print(resJson)
print('---------------')
print(newData)
print(newData2)
