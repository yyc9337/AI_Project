from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer(
    'alarm-topic',
    bootstrap_servers="61.78.151.68:9092",
    group_id='ai2-group',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: loads(x.decode('utf-8'))
);

for msg in consumer:
    qSvcId = None;
    qType = None;
    qTime = None;

    if msg.value.get('nmsSystem') == "QUETONE":
        # 큐톤 타입 추출
        if msg.value.get('probableCause') == "Closed caption detected":
            if msg.value.get('specificProblem') == "Start":
                qType = "A";
            elif msg.value.get('specificProblem') == "Start 2":
                qType = "B";
        elif msg.value.get('probableCause') == "Splice Insert":
            qType = "D";

        # 큐톤 서비스ID 추출
        if msg.value.get('eventTarget') is not None:
            qSvcId = msg.value.get('eventTarget').get('instanceId');
        
        # 큐톤 발생 시간 추출
        qTime = msg.value.get('eventTime');

        if qType is None or qSvcId is None or qTime is None:
            continue;
        
        print (qTime, " / ", qType, " / ", qSvcId);

print('[end]');