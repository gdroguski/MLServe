import redis
import argparse


def main(host: str = '127.0.0.1', port: int = 6379) -> None:
    client = redis.Redis(host=host, port=port)

    client.set('msg_1', 'hello')
    client.set('msg_2', 'bonjour')

    print(client.get('msg_1'))
    print(client.get('msg_2'))
    print('success yay!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'host', help='specify docker-machine host', type=str,
        nargs='?', default='127.0.0.1')

    host: str = parser.parse_args().host
    main(host)
