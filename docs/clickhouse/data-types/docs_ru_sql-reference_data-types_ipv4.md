# IPv4 | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/data-types/ipv4


## IPv4​

IPv4-адреса. Хранятся в 4 байтах в виде UInt32.


### Базовое использование​


```
CREATE TABLE hits (url String, from IPv4) ENGINE = MergeTree() ORDER BY url;

DESCRIBE TABLE hits;

```


```
┌─name─┬─type───┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┐
│ url  │ String │              │                    │         │                  │
│ from │ IPv4   │              │                    │         │                  │
└──────┴────────┴──────────────┴────────────────────┴─────────┴──────────────────┘

```

Или можно использовать домен IPv4 в качестве ключа:


```
CREATE TABLE hits (url String, from IPv4) ENGINE = MergeTree() ORDER BY from;

```

ДоменIPv4поддерживает особый формат ввода — строки IPv4:


```
INSERT INTO hits (url, from) VALUES ('https://wikipedia.org', '116.253.40.133')('https://clickhouse.com', '183.247.232.58')('https://clickhouse.com/docs/en/', '116.106.34.242');

SELECT * FROM hits;

```


```
┌─url────────────────────────────────┬───────────from─┐
│ https://clickhouse.com/docs/en/ │ 116.106.34.242 │
│ https://wikipedia.org              │ 116.253.40.133 │
│ https://clickhouse.com          │ 183.247.232.58 │
└────────────────────────────────────┴────────────────┘

```

Значения хранятся в компактном двоичном формате:


```
SELECT toTypeName(from), hex(from) FROM hits LIMIT 1;

```


```
┌─toTypeName(from)─┬─hex(from)─┐
│ IPv4             │ B7F7E83A  │
└──────────────────┴───────────┘

```

Адреса IPv4 можно сравнивать напрямую с адресами IPv6:


```
SELECT toIPv4('127.0.0.1') = toIPv6('::ffff:127.0.0.1');

```


```
┌─equals(toIPv4('127.0.0.1'), toIPv6('::ffff:127.0.0.1'))─┐
│                                                       1 │
└─────────────────────────────────────────────────────────┘

```

См. также

- Функции для работы с адресами IPv4 и IPv6