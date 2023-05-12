from confluent_kafka import Consumer
import numpy as np
import cv2

def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf

def show():
    props = read_ccloud_config(
        '/client.properties')
    props["group.id"] = "python-group-1"
    props["auto.offset.reset"] = "earliest"

    consumer = Consumer(props)
    consumer.subscribe(["frames"])
    print("Processing .. ")
    try:
        while True:
            msg = consumer.poll(1.0)
            print("working")
            if msg is not None and msg.error() is None:
                print(len(msg.value()))
                nparr = np.frombuffer(msg.value(), np.uint8)
                img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.imshow("video", img_np)
            #use below code to control the speed of low
            key = cv2.waitKey(100) & 0xFF
            if key == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

show()
