var tableRows = {};

function requestAndSaveToJson(date, callback) {
  var xhr = new XMLHttpRequest();
  xhr.withCredentials = true;

  xhr.open('post', 'http://www.iwencai.com/customized/chart/get-robot-data');

  xhr.setRequestHeader('content-type', 'application/json');

  var body = {
    "source": "Ths_iwencai_Xuangu",
    "version": "2.0",
    "query_area": "",
    "block_list": "",
    "add_info": "{\"urp\":{\"scene\":1,\"company\":1,\"business\":1},\"contentType\":\"json\",\"searchInfo\":true}",
    "question": date + " 二级板块指数 涨停家数排序",
    "perpage": "100",
    "page": 1,
    "secondary_intent": "zhishu",
    "log_info": "{\"input_type\":\"typewrite\"}",
    "rsh": "530256177"
  };

  xhr.send(JSON.stringify(body));

  xhr.onload = function () {
    res = JSON.parse(xhr.response);
    items = res.data.answer[0].txt[0].content.components[0].data.datas;
        
      items = items.filter(item=>{
            return item.指数简称!='ST板块' && item.指数简称!='融资融券'
            && item.指数简称!="国企改革"
            && item.指数简称!="深股通"
            && item.指数简称!="标普道琼斯A股"
        })
    var keyss = Object.keys(items[0]);
    var theKey = "";

    for (var i = 0; i < keyss.length; i++) {
      if (keyss[i].indexOf('涨停家数[') != -1) {
        theKey = keyss[i];
      }
    }

    for (var j = 0; j < items.length; j++) {
      if (!tableRows[date]) {
        tableRows[date] = [];
      }

      var newItem = {
        '日期': date,
        '指数简称': '',
      };

      newItem['指数简称'] = items[j]['指数简称'];
      newItem[theKey] = items[j][theKey];
      tableRows[date].push(newItem);
    }

    // 执行回调函数以通知数据已准备好
    if (typeof callback === 'function') {
      callback();
    }
  };
}

// 获取多个日期的数据
var dates = ["2023-09-04", "2023-09-05", "2023-09-06", "2023-09-07",
               "2023-09-08", "2023-09-11", "2023-09-12", "2023-09-13",
               "2023-09-14", "2023-09-15", "2023-09-18", "2023-09-19",
               "2023-09-20", "2023-09-21","2023-09-22"];

var completedRequests = 0;

// 排序函数：按日期的顺序
dates.sort(function(a, b) {
  return new Date(a) - new Date(b);
});

function handleAllRequestsCompleted() {
  completedRequests++;
  if (completedRequests === dates.length) {
    // 所有请求都已完成
    let CsvString = [];

    // 添加数据行
    for (var date of dates) {
      const rowData = tableRows[date].map((item, index) => {
        const values = Object.values(item);
        // 只在第一列保留日期，其余列移除日期
        if (index > 0) {
          values.shift();
        }
        return values.join(',');
      }).join(',');
      CsvString.push(rowData);
    }

    // 加上 CSV 文件头标识
    CsvString = 'data:application/vnd.ms-excel;charset=utf-8,\uFEFF' + encodeURIComponent(CsvString.join('\r\n'));

    // 通过创建a标签下载
    const link = document.createElement('a');
    link.href = CsvString;
    // 对下载的文件命名
    link.download = `修改.csv`;
    // 模拟点击下载
    link.click();
    // 移除a标签
    link.remove();
  }
}

for (var i = 0; i < dates.length; i++) {
  requestAndSaveToJson(dates[i], handleAllRequestsCompleted);
}




