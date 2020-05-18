from redis import Redis

rd = Redis('localhost', port=6378, db=3, decode_responses=True)

if __name__ == '__main__':
    print(rd.keys('*'))
