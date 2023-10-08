import json
#交易日
date_range = get_all_trade_days()
day = '2023-09-22'
preDay = str(date_range[date_range.get_loc(day)-1].date())
nextDay = str(date_range[date_range.get_loc(day)+1].date())
next2Day = str(date_range[date_range.get_loc(day)+2].date())
next3Day = str(date_range[date_range.get_loc(day)+3].date())
followDayList = [nextDay,next2Day,next3Day]

#查询1
queryInfo1 = "沪深所有非st股票" + "day + 收盘价 前复权， 和前120日区间最低价 前复权"
df1 = query_iwencai(queryInfo1)
# df1 = query_iwencai("沪深所有非st股票 20230904 收盘价 前复权， 和前120日区间最低价 前复权")

rowList = []
for index, row in df1.iterrows():
#     print(row['收盘价:前复权']) 
#     print(row['区间最低价:前复权']*1.2)
    if row['收盘价:前复权'] < row['区间最低价:前复权']*1.2:
        rowList.append(row)
#print(rowList)
len(rowList)

df1 = pd.DataFrame(rowList)

#查询2
queryInfo2 = "沪深所有非st股票" + day + "成交量大于" + preDay + "两倍," + day + "涨幅>5%"
df2 = query_iwencai(queryInfo2)
# df2 = query_iwencai("沪深所有非st股票 20230904 成交量大于 20230903 两倍, 20230904 涨幅>5%")

stockList1 = df1['股票代码'].tolist()

stockList2 = df2['股票代码'].tolist()
print(len(stockList2))

print(len(stockList1) )
print(len(stockList2))

intersection_set = set(stockList1).intersection(set(stockList2))

# 将交集转换回列表
intersection_list = list(intersection_set)
len(intersection_list)

intersection_list

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

# json_str = resList.dumps


resJson = json.dumps(resList)
print(resJson)

    # print(newData)
        # dicList.append(itemData)
    # print(dfList)
# print(dicList)
# merged_df = pd.concat(dfList, axis=0)

