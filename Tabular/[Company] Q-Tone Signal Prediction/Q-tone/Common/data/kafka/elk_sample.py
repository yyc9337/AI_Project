# from kafka import KafkaConsumer
from urllib import request
from datetime import datetime
from dateutil.relativedelta import relativedelta
from json import loads
import json
import csv

uri = 'http://61.78.151.69:9200/event/_search?filter_path=hits.**.nmsSystem,hits.**.eventTime,hits.**.probableCause,hits.**.specificProblem,hits.**.eventTarget.instanceId';
interval = 10 * 24 * 60 * 60; # 일/시/분/초/밀리초 10일씩 나눠서 조회
pMonths=3 #3개월치 데이터 조회
pFrom = 0;
pSize = 100000;
eventTimeList = [];
index = 1;
headers = {'Content-Type': 'application/json; chearset=utf-8'};
now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0);
nowTime = int(now.timestamp());
filename = 'quetone_data_' + now.strftime('%Y%m%d') + '.csv';

firstEventTime = int((now - relativedelta(months=pMonths)).timestamp());
eventTime = firstEventTime;

while (eventTime < nowTime):
    startTime = eventTime;
    eventTime = firstEventTime + (interval * index)
    eventTimeList.append({
        "startTime": startTime * 1000,
        "endTime": nowTime * 1000 if eventTime > nowTime else eventTime * 1000
    });
    index += 1;

with open(filename, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow(['큐톤시간', '큐톤타입', '서비스ID'])

    for etl in eventTimeList:
        param = {
            "from": pFrom,
            "size": pSize,
            "sort":{
                "eventTime": "asc"
            },
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "eventTime": {
                                    "gte": etl['startTime'],
                                    "lt": etl['endTime']
                                }
                            }
                        },
                        {
                            "match_phrase": {
                                "nmsSystem": "QUETONE"
                            }
                        },
                        {
                            "query_string": {
                                "default_field": "probableCause",
                                "query": "\"Splice Insert\" OR \"Closed caption detected\""
                            }
                        }
                    ]
                }
            }
        };

        print(param);
        req = request.Request(uri, headers=headers, data=json.dumps(param).encode('utf-8'));
        res = request.urlopen(req);

        dataRes = loads(res.read().decode('utf-8'));

        if dataRes.get("hits") is None:
            continue;

        for data in dataRes.get("hits").get("hits"):
            source = data.get("_source");
            if source.get('nmsSystem') == "QUETONE":
                # 큐톤 타입 추출
                if source.get('probableCause') == "Closed caption detected":
                    if source.get('specificProblem') == "Start":
                        qType = "A";
                    elif source.get('specificProblem') == "Start 2":
                        qType = "B";
                elif source.get('probableCause') == "Splice Insert":
                    qType = "D";

                # 큐톤 서비스ID 추출
                if source.get('eventTarget') is not None:
                    qSvcId = source.get('eventTarget').get('instanceId');
                
                # 큐톤 발생 시간 추출
                qTime = source.get('eventTime');

                if qType is None or qSvcId is None or qTime is None:
                    continue;
                
                spamwriter.writerow([qTime, qType, qSvcId])
                # print (qTime, " / ", qType, " / ", qSvcId);
print('[end]');