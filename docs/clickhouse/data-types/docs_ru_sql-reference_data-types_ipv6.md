# IPv6 | ClickHouse Docs

Source: https://clickhouse.com/docs/ru/sql-reference/data-types/ipv6


## IPv6​

IPv6-адреса. Хранятся в 16 байтах в виде UInt128 в формате big-endian.


### Базовое использование​


```
CREATE TABLE hits (url String, from IPv6) ENGINE = MergeTree() ORDER BY url;

DESCRIBE TABLE hits;

```


```
┌─name─┬─type───┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┐
│ url  │ String │              │                    │         │                  │
│ from │ IPv6   │              │                    │         │                  │
└──────┴────────┴──────────────┴────────────────────┴─────────┴──────────────────┘

```

Или вы можете использовать доменIPv6в качестве ключа:


```
CREATE TABLE hits (url String, from IPv6) ENGINE = MergeTree() ORDER BY from;

```

ДоменIPv6поддерживает произвольный ввод строк в формате IPv6:


```
INSERT INTO hits (url, from) VALUES ('https://wikipedia.org', '2a02:aa08:e000:3100::2')('https://clickhouse.com', '2001:44c8:129:2632:33:0:252:2')('https://clickhouse.com/docs/en/', '2a02:e980:1e::1');

SELECT * FROM hits;

```


```
┌─url────────────────────────────────┬─from──────────────────────────┐
│ https://clickhouse.com          │ 2001:44c8:129:2632:33:0:252:2 │
│ https://clickhouse.com/docs/en/ │ 2a02:e980:1e::1               │
│ https://wikipedia.org              │ 2a02:aa08:e000:3100::2        │
└────────────────────────────────────┴───────────────────────────────┘

```

Значения хранятся в компактном двоичном формате:


```
SELECT toTypeName(from), hex(from) FROM hits LIMIT 1;

```


```
┌─toTypeName(from)─┬─hex(from)────────────────────────┐
│ IPv6             │ 200144C8012926320033000002520002 │
└──────────────────┴──────────────────────────────────┘

```

Адреса IPv6 можно напрямую сравнивать с адресами IPv4:


```
SELECT toIPv4('127.0.0.1') = toIPv6('::ffff:127.0.0.1');

```


```
┌─equals(toIPv4('127.0.0.1'), toIPv6('::ffff:127.0.0.1'))─┐
│                                                       1 │
└─────────────────────────────────────────────────────────┘

```

См. также

- Функции для работы с IP-адресами IPv4 и IPv6