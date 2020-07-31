import redis,pickle

class Redis:
    @staticmethod
    def connect():
        r = redis.Redis(host='localhost', port=6379, db=0)
        return r

    #将内存数据二进制通过序列号转为文本流，再存入redis
    @staticmethod
    def set_pickle_data(r,key,data,ex=None):
        r.set(key,pickle.dumps(data),ex)

    # 将文本流从redis中读取并反序列化，返回返回
    @staticmethod
    def get_pickle_data(r,key):
        data = r.get(key)
        if data is None:
            return None
        return pickle.loads(data)

    @staticmethod
    def set_data(r, key, data, ex=None):
        r.set(key, data, ex)

    @staticmethod
    def get_data(r, key):
        data = r.get(key)
        if data is None:
            return None
        return data





