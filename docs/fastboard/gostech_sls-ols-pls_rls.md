# RLS | ÐÐ¾ÐºÑÐ¼ÐµÐ½ÑÐ°ÑÐ¸Ñ Fastboard

Source: https://help.fastboard.online/gostech/sls-ols-pls/rls/

**RLS (Row Level Security)**Â - ÑÐ°Ð¼ÑÐ¹ Ð´ÐµÑÐ°Ð»ÑÐ½ÑÐ¹ ÑÑÐ¾Ð²ÐµÐ½Ñ Ð´Ð¾ÑÑÑÐ¿Ð°. ÐÐ½ Ð¿Ð¾Ð·Ð²Ð¾Ð»ÑÐµÑ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÑÐ¼ Ð²Ð¸Ð´ÐµÑÑ ÑÐ°Ð·Ð½ÑÐµ Ð´Ð°Ð½Ð½ÑÐµ Ð² Ð¾Ð´Ð½Ð¸Ñ Ð¸ ÑÐµÑ Ð¶Ðµ Ð³ÑÐ°ÑÐ¸ÐºÐ°Ñ , Ð² Ð·Ð°Ð²Ð¸ÑÐ¸Ð¼Ð¾ÑÑÐ¸ Ð¾Ñ Ð¸Ñ ÑÑÑÑÐ½Ð¾Ð¹ Ð·Ð°Ð¿Ð¸ÑÐ¸.

![RLS](https://help.fastboard.online/assets/images/photo_2025-08-11_16-53-12-81d0cdfaf00d83448c07d787cb176d5d.jpg)

ÐÐ¾Ð»Ð¸ÑÐ¸ÐºÐ° Ð½Ð°ÑÑÑÐ¾Ð¹ÐºÐ¸ Ð´Ð¾ÑÑÑÐ¿Ð°: Ð¾Ð³ÑÐ°Ð½Ð¸ÑÐ¸Ð²Ð°ÑÑÐ°Ñ. ÐÑ ÑÐºÐ°Ð·ÑÐ²Ð°ÐµÑÐµ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÐµÐ¹ / ÐÐ, ÐºÐ¾ÑÐ¾ÑÑÐ¼ Ð½ÑÐ¶Ð½Ð¾ Ð¾Ð³ÑÐ°Ð½Ð¸ÑÐ¸ÑÑ Ð´Ð¾ÑÑÑÐ¿.

ÐÐ°Ð¿ÑÐ¸Ð¼ÐµÑ, ÐµÑÑÑ ÑÐ°ÐºÐ¾Ð¹ Ð¿ÑÐ¾ÑÑÐ¾Ð¹ Ð¾ÑÑÑÑ Ð¿Ð¾ Ð¿ÑÐ¾Ð´Ð°Ð¶Ð°Ð¼:

![ÐÑÑÐµÑ Ð¿Ð¾ Ð¿ÑÐ¾Ð´Ð°Ð¶Ð°Ð¼](https://help.fastboard.online/assets/images/unnamed-7baa694d36b7382e797430168991db4f.png)

Ð Ð²Ð°Ð¼ Ð½ÑÐ¶Ð½Ð¾ ÑÐ´ÐµÐ»Ð°ÑÑ, ÑÑÐ¾Ð±Ñ ÑÐµÐ³Ð¸Ð¾Ð½Ð°Ð»ÑÐ½ÑÐµ Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑÑ Ð²Ð¸Ð´ÐµÐ»Ð¸ ÑÐ¾Ð»ÑÐºÐ¾ ÑÐ²Ð¾Ð¸ Ð¿ÑÐ¾Ð´Ð°Ð¶Ð¸, Ð° Ð¾ÑÑÐ°Ð»ÑÐ½ÑÑ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÐµÐ¹ Ð½Ðµ Ð¾Ð³ÑÐ°Ð½Ð¸ÑÐ¸Ð²Ð°ÑÑ.

ÐÐ»Ñ ÑÑÐ¾Ð³Ð¾ Ð¼Ñ Ð¿ÐµÑÐµÑ Ð¾Ð´Ð¸Ð¼ Ð² Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑ Ð´Ð°Ð½Ð½ÑÑ Ð¸ Ð½Ð°ÑÑÑÐ°Ð¸Ð²Ð°ÐµÐ¼ Ð½Ð°ÑÑ Ð¼Ð¾Ð´ÐµÐ»Ñ. ÐÑÐ¸ Ð½Ð°Ð²ÐµÐ´ÐµÐ½Ð¸Ð¸ Ð½Ð° Ð¼Ð¾Ð´ÐµÐ»Ñ Ð´Ð°Ð½Ð½ÑÑ Ð² Ð¿Ð°Ð½ÐµÐ»Ð¸ Ð½Ð°Ð¶Ð¸Ð¼Ð°ÐµÐ¼ Ð½Ð° Ð¸ÐºÐ¾Ð½ÐºÑ Ð½Ð°ÑÑÑÐ¾Ð¹ÐºÐ¸ Ð´Ð¾ÑÑÑÐ¿Ð°:

![ÐÐ¾Ð´ÐµÐ»Ñ](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAI0AAABMCAIAAADfiKPjAAAGbUlEQVR4Xu2b7WtbVRjA9zfIcEwEwQ9BVzrQMFHEUbBs1lGHHxQtCN0HLfohX+ZEVyHQudp9GBU1outU2pmSvqyGrsSNda2xWbNlLcuKfYG+TJfaru3uublppHQU9Ln3yT25zUnT5eatJzmXH5dzzz3npH1+ec4599Lumr0bEux8dimRqGDnIzzxgfDEB8ITHwhPfCA88YHwxAfCEx8IT3wgPPGB8MQHwhMfCE98IDzxgfDEB8ITHwhPfCA85Yrp2XtnmlvhzN4yQX48hW1OyXolvKlyRq52StWDCtM458zfIdUuyQI/Ug+5tph4N1uMT8zaG8/Bmb1lgvx5sjiJeyleGRggloJ4ksP1LlIfjCiR1eCAZOmTl9k22YBTT6SuT6oLRGhNvUuyeXRPcsRzVbKCy3ZSNxiej/dSv/UaxIOVstJ2iZRDjYu0Ta9qzRRHN20WG9BDR2aZkCu65SCW5yCn9ZGzDa+e3HeItUeewxqt7O4nGM3JQcnSIwelqDIfbujWdYbkmlgQ1e5aIeL5jVRcCc/Lq/O3yEsuMqRWgifSNKEOC+Ns72mUWLrlScMPJjxR1HB0LKoTzvm/4TLi1nJLj6bS3C3Vj8UaL98glkvaXKQuYAmewiecpC2ELdVejhm14IgVNnmKZ9hVmqAaOfMEWwawQvndOwKe4GysNL2tyJsnNZSwJlUMhJUlua5dXat0T7G7scY0jtPy4dgEpUdT23pQAYBtNGoQliyfpHBDFzTDGXLz+MaRswHs7kBMnNM/xM860Ibt+Cjk1ZMa6E7Z7SO49zPkU2ziUgz5pBY8uEXUoynLal4aNiP0rltWy0k8sXNgztan4sknUHK+R7K6SNOUWk8jmGR9ktUssY3iviO+PsGEqa1PUWVFcXjkoQfR5dvE2iUHtA9K4knLJzqpqmj7Pdstsd9LQnxmWw4Qix7WeDSZ/Z5xgYmBk9Vi2IH7PWh5XcE17ERM56OtT/D8NC7XiOenrACB1tYeHfARX1T4QHjig5LwVATw+H5PkCnCEx8IT3wgPPGB8MQHwhMfmPSU+LKglGCjkQeEp7Rho5EHTHpi/3FekDlsnCkmPQnyjPDEB8ITHwhPfCA88UGpewr9c/9yv//sN+1I56/9UMM2Kzh58gS/P0ShpdWdlSiMT87haMM3xzIckOpB8JJtVnDy4QkCam88h1GALy/bYFtADCjBMojBv7GCYc0NuCKFJVkBxsZnYByfP4iXAJSh5u69BbyElmz3gpBzTygJo4yq2DapoX/8hn1BDJTxFpbTTalmRzsdMzXQku1eEHLrCSXROQrK6X79sRfkE6YRXGINujHn6Y/rt50dl6Hjjxd6twLuQhtoyXYvCDn0hJIgxLhQ27WZim2WGtYTLk6oH89sr20xymahn8XeKhS58kQlKdrqYk6SoocMldDIwoAwGmB6e2b0NBKcvDnyJxTgDGWldDxlSxICUYOQQVJiWLFMwQxje6XG6OnnX/q+/6kHCnCGslIinnIhiYYMB2cxt+yVrqfsSsJoImjLru3vjW0gpi3aBj2tCbCkPeGvh1/tzCUp2o4cVyAMKJTt+o7cCH5WWrNfSXuiTzYYhQwl4SC4/KADfPzCS+Tb71orD71V9XpN7fufpRXWkvZkXDwylKToWYLg5hvzycj+5yq9Xr/H0299ocp0PsF57q8FKMCZ1hSzJ3xRRjdmmQPj0GQyXlJ2P/7MxsbG+vrDPU+UrTwg7AhbgV+CrX7OIveUfx7bbflPO6DA3k0BmsAXJSz4uMb2KiAl6knRUgqyn5XUoj0+pzWL5oHi8VR7zPZB3XHv0A3fcMDvH2Ubc03xeOrs6nW2XwRVFa++ebDiaNOZr8FW0QgrHk+0sLa2FgotlJUfBFvA6cav2I7cUWyennraSmui0X8XFu7vK3uZ7cgdRevJKIztyB1F4gmen7Bw4MXDwtNOgT7SUk8wv2FBUSJYGBj0CU8Fo6Or942j70H2nPz8S7BFPaU4hKcCAJIgUSBpPj35xe49zwpPO5SqI+8M+QIowOv1P3+gcrOUJIfwVACczov7yl9ZWlpBB7SQ4hCeCkPDqbNVR95dX3+YKCTZob5K31vGDsId/HkCjn9sBxKdJDvwxQQ7Andw6Qn48KNP2i50Jmphjs6u3tpjNrY7d/DqyTcc2Pvk/qmp6UQzm49Dr73df22I7c4d/wNIOGw62mhxjQAAAABJRU5ErkJggg==)

**Ð Ð¿ÐµÑÐ²ÑÑ Ð¾ÑÐµÑÐµÐ´Ñ Ð±ÑÐ´ÐµÑ ÑÐ°ÑÑÐ¼Ð¾ÑÑÐµÐ½ Ð¾Ð´Ð¸Ð½ Ð¸Ð· Ð²Ð°ÑÐ¸Ð°Ð½ÑÐ¾Ð² ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸ Ð´Ð°Ð½Ð½Ð¾Ð³Ð¾ ÑÑÐ½ÐºÑÐ¸Ð¾Ð½Ð°Ð»Ð°. ÐÐ¾ÑÐ»Ðµ ÑÑÐ¾Ð³Ð¾ Ð±ÑÐ´ÑÑ ÑÐ°Ð·ÑÑÑÐ½ÐµÐ½Ñ Ð¿ÑÐ¸Ð½ÑÐ¸Ð¿Ñ ÐµÐ³Ð¾ ÑÐ°Ð±Ð¾ÑÑ, Ð° ÑÐ°ÐºÐ¶Ðµ Ð¿ÑÐµÐ´ÑÑÐ°Ð²Ð»ÐµÐ½Ñ Ð´Ð¾ÑÑÑÐ¿Ð½ÑÐµ Ð²Ð¾Ð·Ð¼Ð¾Ð¶Ð½Ð¾ÑÑÐ¸.**

Ð ÐºÐ°ÑÐµÑÑÐ²Ðµ Ð¿ÑÐ¸Ð¼ÐµÑÐ° Ð±ÑÐ´ÐµÑ Ð¸ÑÐ¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÑÑÑ Ð¿Ð¾Ð»Ðµ **Â«Ð ÐµÐ³Ð¸Ð¾Ð½Â»** Ð¸Ð· ÑÐ¿ÑÐ°Ð²Ð¾ÑÐ½Ð¸ÐºÐ° **Â«ÐÐ°Ð³Ð°Ð·Ð¸Ð½ÑÂ»**.

**ÐÑÐ¸Ð¼ÐµÑ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸:**

![ÐÑÐ¸Ð¼ÐµÑ ÑÐµÐ°Ð»Ð¸Ð·Ð°ÑÐ¸Ð¸ ](https://help.fastboard.online/assets/images/unnamed-2--c17dc88943e57b761646f2b81f5f2fb7.png)

Ð¡Ð¾Ð·Ð´Ð°ÑÐ¼ Ð¿ÑÐ°Ð²Ð¸Ð»Ð¾ Ð¸ Ð½Ð°Ð·ÑÐ²Ð°ÐµÐ¼ ÐµÐ³Ð¾:

![ÐÐ°Ð¸Ð¼ÐµÐ½Ð¾Ð²Ð°Ð½Ð¸Ðµ Ð¿ÑÐ°Ð²Ð¸Ð»Ð° ](https://help.fastboard.online/assets/images/unnamed-3--96e5d0124b6d3e197d221a03eb9b7067.png)

ÐÐ¾ÑÐ»Ðµ ÑÐµÐ³Ð¾ Ð¾ÑÐºÑÑÐ²Ð°ÐµÑÑÑ Ð¾ÐºÐ½Ð¾ Ð½Ð°ÑÑÑÐ¾Ð¹ÐºÐ¸ Ð¿ÑÐ°Ð²Ð¸Ð»Ð° RLS

![ÐÐºÐ½Ð¾ Ð ÐÐ¡](https://help.fastboard.online/assets/images/unnamed-4--e88d9dcb636b3bda51f6ed25650b9e4a.png)

**ÐÐ»Ð¾ÐºÐ¸ ÐÐ¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ð¸ Ð¸ ÐÑÑÐ¿Ð¿Ñ** Ð¾ÑÐ²ÐµÑÐ°ÑÑ Ð·Ð° ÑÐµÑ , Ð½Ð° ÐºÐ¾Ð³Ð¾ Ð¼Ñ Ð½Ð°ÐºÐ»Ð°Ð´ÑÐ²Ð°ÐµÐ¼ Ð¾Ð³ÑÐ°Ð½Ð¸ÑÐµÐ½Ð¸Ðµ Ð½Ð° Ð´Ð°Ð½Ð½ÑÑ .

**ÐÐ»Ð¾Ðº ÐÐµÑÐµÐ¼ÐµÐ½Ð½ÑÐµ** Ð¿Ð¾Ð·Ð²Ð¾Ð»ÑÐµÑ Ð¿ÑÐ¸Ð²ÑÐ·Ð°ÑÑ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÑÐ¼ / ÐÐ Ð¸Ñ Ð·Ð½Ð°ÑÐµÐ½Ð¸Ñ Ð´Ð»Ñ Ð´Ð°Ð»ÑÐ½ÐµÐ¹ÑÐµÐ³Ð¾ Ð¸ÑÐ¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°Ð½Ð¸Ñ Ð² ÑÑÐ»Ð¾Ð²Ð¸Ð¸ Ð¾ÑÐ¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ Ð¾ÑÐ´ÐµÐ»ÑÐ½ÑÑ ÑÑÑÐ¾Ðº Ð´Ð°Ð½Ð½ÑÑ .

**ÐÐ»Ð¾Ðº Ð¤Ð¸Ð»ÑÑÑ** â Ð½ÐµÐ¿Ð¾ÑÑÐµÐ´ÑÑÐ²ÐµÐ½Ð½Ð¾ Ð¾Ð¿Ð¸ÑÑÐ²Ð°ÐµÑ Ð¿ÑÐ°Ð²Ð¸Ð»Ð¾.

ÐÐµÑÐ²ÑÐ¼ ÑÐ°Ð³Ð¾Ð¼ Ð´Ð¾Ð±Ð°Ð²Ð»ÑÐµÐ¼ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÐµÐ¹, ÐºÐ¾ÑÐ¾ÑÑÑ Ð¼Ñ Ñ Ð¾ÑÐ¸Ð¼ Ð¾Ð³ÑÐ°Ð½Ð¸ÑÐ¸ÑÑ Ð² Ð´Ð°Ð½Ð½ÑÑ : Ð½Ð°Ð¿ÑÐ¸Ð¼ÐµÑ, ÑÐµÐ³Ð¸Ð¾Ð½Ð°Ð»ÑÐ½ÑÐµ Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑÑ.

![Ð ÐµÐ³Ð¸Ð¾Ð½Ð°Ð»ÑÐ½ÑÐµ Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑÑ](data:image/png;base64,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)

ÐÑÐµ Ð¿ÑÐ¾ÑÐ¸Ðµ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ð¸ Ð½Ð¸ÐºÐ°Ðº Ð½Ðµ Ð±ÑÐ´ÑÑ Ð¾Ð³ÑÐ°Ð½Ð¸ÑÐµÐ½Ñ.

ÐÐ°ÑÐµÐ¼ ÑÐ¾Ð·Ð´Ð°ÑÐ¼ Ð¿ÐµÑÐµÐ¼ÐµÐ½Ð½ÑÑ `manager_regions`. ÐÐ½Ð°ÑÐµÐ½Ð¸Ðµ Ð¿Ð¾ ÑÐ¼Ð¾Ð»ÑÐ°Ð½Ð¸Ñ â Ð¿ÑÑÑÐ°Ñ ÑÑÑÐ¾ÐºÐ° .

![Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ Ð¿ÐµÑÐµÐ¼ÐµÐ½Ð½Ð¾Ð¹](https://help.fastboard.online/assets/images/unnamed-6--a1b1963ea4340d62c6a2fba8c4677769.png)

ÐÐ¾ÑÐ»Ðµ ÑÐµÐ³Ð¾ Ð·Ð°Ð´Ð°ÑÐ¼ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÑÐ¼ Ð¸Ñ Ð·Ð½Ð°ÑÐµÐ½Ð¸Ñ. ÐÑÐ±Ð¸ÑÐ°ÐµÐ¼ moscow_manager Ð¸ Ð¿ÑÐ¾Ð¿Ð¸ÑÑÐ²Ð°ÐµÐ¼ ÐµÐ³Ð¾ ÑÐµÐ³Ð¸Ð¾Ð½ ÐÐ¾ÑÐºÐ²Ð°.Â

ÐÐ½Ð°ÑÐµÐ½Ð¸Ñ Ð´Ð¾Ð»Ð¶Ð½Ñ Ñ ÑÐ¾ÑÐ½Ð¾ÑÑÑÑ ÑÐ¾Ð²Ð¿Ð°Ð´Ð°ÑÑ Ñ ÑÐµÐ¼Ð¸, ÑÑÐ¾ Ð»ÐµÐ¶Ð°Ñ Ð² Ð´Ð°Ð½Ð½ÑÑ .

![ÐÐ¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ð¸](https://help.fastboard.online/assets/images/unnamed-7--42deac0c765031fcda3c3e001fe9ae30.png)

ÐÐ»Ñ rostov_manager Ð·Ð½Ð°ÑÐµÐ½Ð¸Ðµ, ÑÐ¾Ð¾ÑÐ²ÐµÑÑÑÐ²ÐµÐ½Ð½Ð¾, Ð Ð¾ÑÑÐ¾Ð².

Ð, Ð½Ð°ÐºÐ¾Ð½ÐµÑ, ÑÐ°Ð¼Ð¾ Ð¿ÑÐ°Ð²Ð¸Ð»Ð¾: `WHERE shops.region in ( {{manager_regions}} )`

ÐÑÐ¾Ð²ÐµÑÐ¸Ð¼, ÐºÐ°Ðº ÑÐ°Ð±Ð¾ÑÐ°ÐµÑ Ð¿ÑÐ°Ð²Ð¸Ð»Ð¾.

Ð¢Ð°Ðº ÑÑÐ¾ Ð²ÑÐ³Ð»ÑÐ´Ð¸Ñ Ñ Ð¾Ð±ÑÑÐ½Ð¾Ð³Ð¾ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ, Ð´Ð»Ñ ÐºÐ¾ÑÐ¾ÑÐ¾Ð³Ð¾ Ð½ÐµÑ Ð¿ÑÐ°Ð²Ð¸Ð»Ð°:

![ÐÑÐ¸Ð¼ÐµÑ Ð³ÑÐ°ÑÐ¸ÐºÐ°](https://help.fastboard.online/assets/images/unnamed-8--ef4e5626784a125b6d300ca6e7ada98c.png)

Ð¢Ð°Ðº ÑÑÐ¾ Ð²ÑÐ³Ð»ÑÐ´Ð¸Ñ Ð¿Ð¾Ð´ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÐµÐ¼ moscow_region:

![ÐÑÐ¸Ð¼ÐµÑ 2](https://help.fastboard.online/assets/images/unnamed-9--0d36abce1f736cc5d8ecf23b67a1f37f.png)

ÐÐ¸Ð´Ð¸Ð¼, ÑÑÐ¾ Ð·Ð½Ð°ÑÐµÐ½Ð¸Ñ Ð²ÑÐµÑ Ð³ÑÐ°ÑÐ¸ÐºÐ¾Ð² Ð¸Ð·Ð¼ÐµÐ½Ð¸Ð»Ð¸ÑÑ, Ð² ÑÐ¸Ð»ÑÑÑÐµ Ð¾ÑÑÐ°Ð»ÑÑ ÑÐ¾Ð»ÑÐºÐ¾ ÑÐµÐ³Ð¸Ð¾Ð½ ÐÐ¾ÑÐºÐ²Ð°, Ð° ÑÐµÐ¹ÑÐ¸Ð½Ð³, Ð¿Ð¾Ð¼Ð¸Ð¼Ð¾ ÑÐ¸Ð»ÑÑÑÐ°ÑÐ¸Ð¸ Ð¿Ð¾ ÐÐ¾ÑÐºÐ²Ðµ, Ð°Ð²ÑÐ¾Ð¼Ð°ÑÐ¸ÑÐµÑÐºÐ¸ Ð¿ÐµÑÐµÑÑÐ» Ð½Ð° ÑÐ»ÐµÐ´ÑÑÑÐ¸Ð¹ ÑÑÐ¾Ð²ÐµÐ½Ñ drill_down â ÑÑÐ°Ð·Ñ Ð´Ð¾ Ð¼Ð°Ð³Ð°Ð·Ð¸Ð½Ð¾Ð².

ÐÐ¾ rostov_manager Ð°Ð½Ð°Ð»Ð¾Ð³Ð¸ÑÐ½Ð¾:

![Ð¿ÑÐ¸Ð¼ÐµÑ 3 ](https://help.fastboard.online/assets/images/unnamed-10--8fae73c3b95c29b39e3d81088404b370.png)

**ÐÐ°Ðº ÑÑÐ¾ ÑÐ°Ð±Ð¾ÑÐ°ÐµÑ?**

ÐÐ° ÐºÐ°Ð¶Ð´ÑÐ¹ Ð·Ð°Ð¿ÑÐ¾Ñ Ð¾Ñ Ð²Ð¸Ð·ÑÐ°Ð»ÑÐ½ÑÑ ÐºÐ¾Ð¼Ð¿Ð¾Ð½ÐµÐ½ÑÐ¾Ð² Ð½Ð°ÐºÐ»Ð°Ð´ÑÐ²Ð°ÐµÑÑÑ ÑÑÐ»Ð¾Ð²Ð¸Ðµ, Ð¾Ð¿Ð¸ÑÐ°Ð½Ð½Ð¾Ðµ Ð² Ð¿ÑÐ°Ð²Ð¸Ð»Ðµ


```
WHERE shops.region in ( {{manager_regions}} )
```

ÐÐ° Ð¾ÑÐ½Ð¾Ð²Ð°Ð½Ð¸Ð¸ ÑÐµÐºÑÑÐµÐ¹ ÑÑÑÑÐ½Ð¾Ð¹ Ð·Ð°Ð¿Ð¸ÑÐ¸ Ð²Ð¼ÐµÑÑÐ¾ Ð²ÑÐµÑ Ð¿ÐµÑÐµÐ¼ÐµÐ½Ð½ÑÑ Ð¿Ð¾Ð´ÑÑÐ°Ð²Ð»ÑÑÑÑÑ Ð¸Ñ Ð·Ð½Ð°ÑÐµÐ½Ð¸Ñ. ÐÐ° Ð¿ÑÐ¸Ð¼ÐµÑÐµ Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑÐ° ÐÐ¾ÑÐºÐ¾Ð²ÑÐºÐ¸Ñ Ð¼Ð°Ð³Ð°Ð·Ð¸Ð½Ð¾Ð² ÑÑÐ¾


```
WHERE shops.region in ( âÐÐ¾ÑÐºÐ²Ð°â )
```

Ð¢Ð°ÐºÐ¸Ð¼ Ð¾Ð±ÑÐ°Ð·Ð¾Ð¼ ÐºÐ°Ð¶Ð´ÑÐ¹ Ð¸Ð· Ð¿ÐµÑÐµÑÐ¸ÑÐ»ÐµÐ½Ð½ÑÑ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÐµÐ¹ Ð±ÑÐ´ÑÑ Ð²Ð¸Ð´ÐµÑÑ ÑÐ¾Ð»ÑÐºÐ¾ ÑÐ²Ð¾Ð¸ Ð´Ð°Ð½Ð½ÑÐµ. ÐÑÐµ Ð¿ÑÐ¾ÑÐ¸Ðµ Ð¿Ð¾ ÑÐ¼Ð¾Ð»ÑÐ°Ð½Ð¸Ñ Ð²Ð¸Ð´ÑÑ Ð²ÑÐµ Ð´Ð°Ð½Ð½ÑÐµ.

ÐÐ°ÐºÐ¸Ðµ ÐµÑÑ ÐµÑÑÑ Ð²Ð¾Ð·Ð¼Ð¾Ð¶Ð½Ð¾ÑÑÐ¸ RLS?

Ð ÑÐ¾ÑÐ¼Ðµ Ð½Ð°ÑÑÑÐ¾Ð¹ÐºÐ¸ Ð¿ÑÐ°Ð²Ð¸Ð»Ð° Ð²Ñ Ð¿Ð¸ÑÐµÑÐµ Ð¿ÑÐ¾Ð¸Ð·Ð²Ð¾Ð»ÑÐ½ÑÐ¹ SQL (ÑÐ·ÑÐº ÑÑÑÑÐºÑÑÑÐ¸ÑÐ¾Ð²Ð°Ð½Ð½ÑÑ Ð·Ð°Ð¿ÑÐ¾ÑÐ¾Ð²), Ð¾Ð³ÑÐ°Ð½Ð¸ÑÐ¸Ð²Ð°ÑÑÑ Ð»Ð¸ÑÑ ÐµÐ³Ð¾ ÑÐ¸Ð½ÑÐ°ÐºÑÐ¸ÑÐ¾Ð¼ Ð¸ ÑÐ²Ð¾Ð¸Ð¼ Ð²Ð¾Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸ÐµÐ¼. ÐÐ°Ð¶Ð½Ð¾ Ð»Ð¸ÑÑ Ð¿Ð¾Ð¼Ð½Ð¸ÑÑ Ð¾ ÑÐ¾Ð¼, ÑÑÐ¾ Ð¿ÐµÑÐµÐ¼ÐµÐ½Ð½ÑÐµ â ÑÑÐ¾ Ð¿ÑÐ¾ÑÑÐ°Ñ Ð¿Ð¾Ð´ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð·Ð½Ð°ÑÐµÐ½Ð¸Ð¹, Ð° ÑÐ°ÐºÐ¶Ðµ Ð¾ ÐºÐ°Ð²ÑÑÐºÐ°Ñ , ÐºÐ¾Ð³Ð´Ð° ÑÐ°Ð±Ð¾ÑÐ°ÐµÑÐµ Ñ ÑÐµÐºÑÑÐ¾Ð²ÑÐ¼Ð¸ Ð·Ð½Ð°ÑÐµÐ½Ð¸ÑÐ¼Ð¸.

Ð Ð½Ð°ÑÐµÐ¼ ÑÐ»ÑÑÐ°Ðµ Ð¼Ñ ÑÑÐ°Ð·Ñ Ð·Ð°Ð»Ð¾Ð¶Ð¸Ð»Ð¸ Ð»Ð¾Ð³Ð¸ÐºÑ, ÐºÐ¾Ð³Ð´Ð° Ð¿Ð¾Ð´ ÑÐ¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸ÐµÐ¼ Ð¾Ð´Ð½Ð¾Ð³Ð¾ Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑÐ° Ð¼Ð¾Ð¶ÐµÑ Ð±ÑÑÑ Ð½ÐµÑÐºÐ¾Ð»ÑÐºÐ¾ ÑÐµÐ³Ð¸Ð¾Ð½Ð¾Ð², Ð¿Ð¾ÑÑÐ¾Ð¼Ñ Ð¸ÑÐ¿Ð¾Ð»ÑÐ·ÑÐµÑÑÑ Ð¾Ð¿ÐµÑÐ°ÑÐ¾Ñ IN.Â Ð Ð¿ÑÐ¾ÑÑÐ¾Ð¼ ÑÐ»ÑÑÐ°Ðµ Ð¼Ð¾Ð¶Ð½Ð¾ Ð¸ÑÐ¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÑ `WHERE shops.region = {{manager_region}}`

Ð Ð°Ð·Ð±ÐµÑÑÐ¼ Ð½ÐµÑÐºÐ¾Ð»ÑÐºÐ¾ Ð²Ð°ÑÐ¸Ð°ÑÐ¸Ð¹ Ð½Ð°ÑÐµÐ¹ Ð·Ð°Ð´Ð°ÑÐ¸:

- ÐÑÐ»Ð¸ Ð² ÑÐ¿ÑÐ°Ð²Ð¾ÑÐ½Ð¸ÐºÐµ Ð¼Ð°Ð³Ð°Ð·Ð¸Ð½Ð¾Ð² ÑÐ¶Ðµ Ð¿ÑÐ¾Ð¿Ð¸ÑÐ°Ð½ Ð¸Ñ Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑ, Ð¿ÑÐ°Ð²Ð¸Ð»Ð¾ Ð¼Ð¾Ð¶Ð½Ð¾ Ð¾Ð¿Ð¸ÑÐ°ÑÑ ÑÐ»ÐµÐ´ÑÑÑÐ¸Ð¼ Ð¾Ð±ÑÐ°Ð·Ð¾Ð¼ `WHERE shops.manager = {{manager}}`, Ð·Ð°Ð´Ð°Ð² Ð¿ÑÐµÐ´Ð²Ð°ÑÐ¸ÑÐµÐ»ÑÐ½Ð¾ Ð·Ð½Ð°ÑÐµÐ½Ð¸Ñ Ð¿ÐµÑÐµÐ¼ÐµÐ½Ð½Ð¾Ð¹ Ð´Ð»Ñ ÐºÐ°Ð¶Ð´Ð¾Ð³Ð¾ Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑÐ°
- ÐÑÐ»Ð¸ Ñ Ð²Ð°Ñ Ð±Ð¾Ð»ÐµÐµ ÑÐ»Ð¾Ð¶Ð½Ð°Ñ Ð¸ÐµÑÐ°ÑÑ Ð¸Ñ, Ð½Ð°Ð¿ÑÐ¸Ð¼ÐµÑ Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑÑ Ð¼Ð°Ð³Ð°Ð·Ð¸Ð½Ð¾Ð² Ð¸ ÑÐµÐ³Ð¸Ð¾Ð½Ð°Ð»ÑÐ½ÑÐµ Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑÑ
![ÐÐµÑÐ°ÑÑ Ð¸Ñ ](https://help.fastboard.online/assets/images/unnamed-11--e3df5645dc1ab50440a6113c8cf0f570.png)

Ð¥Ð¾ÑÐ¾ÑÐ¸Ð¼ Ð²Ð°ÑÐ¸Ð°Ð½ÑÐ¾Ð¼ Ð±ÑÐ´ÐµÑ ÑÐ¾Ð·Ð´Ð°ÑÑ 2 Ð¿ÑÐ°Ð²Ð¸Ð»Ð°: Ð´Ð»Ñ Ð¾Ð±ÑÑÐ½ÑÑ Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑÐ¾Ð² Ð¸ Ð´Ð»Ñ ÑÐµÐ³Ð¸Ð¾Ð½Ð°Ð»ÑÐ½ÑÑ . ÐÑ Ð»Ð¾Ð³Ð¸ÐºÐ° ÑÑ Ð¾Ð¶Ð° Ñ Ð¿.1. Ð ÑÑÐ¾Ð¼ ÑÐ»ÑÑÐ°Ðµ Ð´Ð»Ñ ÐºÐ°Ð¶Ð´Ð¾Ð³Ð¾ Ð¸Ð· Ð½Ð¸Ñ Ð±ÑÐ´ÐµÑ ÑÐ°Ð±Ð¾ÑÐ°ÑÑ ÑÐ²Ð¾Ñ Ð¿ÑÐ°Ð²Ð¸Ð»Ð¾.

Ð¢Ð°ÐºÐ¶Ðµ Ð¼Ð¾Ð¶Ð½Ð¾ Ð¾Ð¿Ð¸ÑÐ°ÑÑ Ð²ÑÑ Ð² Ð¾Ð´Ð½Ð¾Ð¼:

- Ð¾Ð¿Ð¸ÑÑÐ²Ð°ÐµÐ¼ 2 Ð¿ÐµÑÐµÐ¼ÐµÐ½Ð½ÑÐµ: manager Ð¸ `region_manager`. Ð£ Ð¾Ð±ÑÑÐ½ÑÑ Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑÐ¾Ð² Ð±ÑÐ´ÐµÑ Ð·Ð°Ð¿Ð¾Ð»Ð½ÐµÐ½Ð° ÑÐ¾Ð»ÑÐºÐ¾ Ð¿ÐµÑÐ²Ð°Ñ, Ñ ÑÐµÐ³Ð¸Ð¾Ð½Ð°Ð»ÑÐ½ÑÑ â Ð²ÑÐ¾ÑÐ°Ñ. *ÐÐ°Ð¿ÑÐ¸Ð¼ÐµÑ,* Ñ Ð¡Ð¼Ð¸ÑÐ½Ð¾Ð²Ð° (Ð¼Ð°Ð³Ð°Ð·Ð¸Ð½ Ð10)
![2](https://help.fastboard.online/assets/images/unnamed-12--4fdfbb093abb8d0dca952c2da389a0e5.png)

![3](https://help.fastboard.online/assets/images/unnamed-13--7e7b4b4581bd935173c8967009668b57.png)

- ÑÐ¸Ð»ÑÑÑ Ð·Ð°Ð´Ð°ÑÐ¼ Ð²ÑÑÐ°Ð¶ÐµÐ½Ð¸ÐµÐ¼ `WHERE manager = '{{manager}}' or region_manager = '{{region_manager}}'`
Ð¢Ð°ÐºÐ¸Ð¼ Ð¾Ð±ÑÐ°Ð·Ð¾Ð¼, Ñ Ð¡Ð¼Ð¸ÑÐ½Ð¾Ð²Ð° ÑÐ¸Ð»ÑÑÑ Ð¿ÑÐ¸Ð¼ÐµÑ Ð²Ð¸Ð´: `WHERE manager = 'Ð¡Ð¼Ð¸ÑÐ½Ð¾Ð²' or region_manager = ''` Ð Ñ.Ðº. Ð¿ÑÑÑÑÑ ÑÐµÐ³Ð¸Ð¾Ð½Ð°Ð»ÑÐ½ÑÑ Ð¼ÐµÐ½ÐµÐ´Ð¶ÐµÑÐ¾Ð² Ð² Ð´Ð°Ð½Ð½ÑÑ Ð½ÐµÑ, Ð¾Ð½ ÑÐ²Ð¸Ð´Ð¸Ñ Ð´Ð°Ð½Ð½ÑÐµ ÑÐ¾Ð»ÑÐºÐ¾ Ð¿Ð¾ ÑÐ²Ð¾ÐµÐ¼Ñ Ð¼Ð°Ð³Ð°Ð·Ð¸Ð½Ñ.

ÐÑ ÑÐ°Ð·Ð¾Ð±ÑÐ°Ð»Ð¸ Ð½ÐµÑÐºÐ¾Ð»ÑÐºÐ¾ Ð±Ð¸Ð·Ð½ÐµÑ-ÐºÐµÐ¹ÑÐ¾Ð², ÑÐµÐ¿ÐµÑÑ **ÑÐ°ÑÑÐ¼Ð¾ÑÑÐ¸Ð¼ ÑÐµÑ Ð½Ð¸ÑÐµÑÐºÐ¸Ðµ Ð²Ð¾Ð·Ð¼Ð¾Ð¶Ð½Ð¾ÑÑÐ¸:**

- ÐÐ¾Ð¶Ð½Ð¾ Ð·Ð°Ð´Ð°Ð²Ð°ÑÑ Ð½ÐµÑÐºÐ¾Ð»ÑÐºÐ¾ Ð¿ÑÐ°Ð²Ð¸Ð» Ð½Ð° Ð¾Ð´Ð½Ñ Ð¸ ÑÑ Ð¶Ðµ Ð¼Ð¾Ð´ÐµÐ»Ñ Ð´Ð°Ð½Ð½ÑÑ . ÐÑÐ»Ð¸ Ð¾Ð´Ð¸Ð½ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ ÑÐ¸Ð³ÑÑÐ¸ÑÑÐµÑ Ð² Ð½ÐµÑÐ¾Ð»ÑÐºÐ¸Ñ Ð¿ÑÐ°Ð²Ð¸Ð»Ð°Ñ , Ð´Ð»Ñ Ð½ÐµÐ³Ð¾ Ð±ÑÐ´ÑÑ Ð¿ÑÐ¸Ð¼ÐµÐ½ÐµÐ½Ñ Ð²ÑÐµ Ð¾Ð³ÑÐ°Ð½Ð¸ÑÐµÐ½Ð¸Ñ
- ÐÑÐ°Ð²Ð¸Ð»Ð° Ð¼Ð¾Ð¶Ð½Ð¾ ÑÐºÑÐ¿Ð¾ÑÑÐ¸ÑÐ¾Ð²Ð°ÑÑ/Ð¸Ð¼Ð¿Ð¾ÑÑÐ¸ÑÐ¾Ð²Ð°ÑÑ Ð² csv/xlsx. ÐÐ¾Ð¼Ð¾Ð³Ð°ÐµÑ Ð¿ÐµÑÐµÐ½Ð¾ÑÐ¸ÑÑ Ð»Ð¾Ð³Ð¸ÐºÑ Ð¼ÐµÐ¶Ð´Ñ Ð¿ÑÐ¾ÐµÐºÑÐ°Ð¼Ð¸
![Ð­ÐºÑÐ¿Ð¾ÑÑ ](https://help.fastboard.online/assets/images/unnamed-14--152dde0618ce3a621fc3106798e20181.png)

**Ð£ ÑÐ°Ð·ÑÐ°Ð±Ð¾ÑÑÐ¸ÐºÐ¾Ð² Ð¿ÑÐ¾ÐµÐºÑÐ° ÐµÑÑÑ Ð²Ð¾Ð·Ð¼Ð¾Ð¶Ð½Ð¾ÑÑÑ ÑÐµÑÑÐ¸ÑÐ¾Ð²Ð°ÑÑ ÑÐ°Ð±Ð¾ÑÑ RLS, Ð½Ðµ Ð·Ð°Ð¿ÑÐ°ÑÐ¸Ð²Ð°Ñ Ð´Ð¾ÑÑÑÐ¿Ñ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÐµÐ¹ Ð¸ Ð½Ðµ ÑÐ¾Ð·Ð´Ð°Ð²Ð°Ñ ÑÐµÑÑÐ¾Ð²ÑÐµ Ð£Ð. ÐÐ»Ñ ÑÑÐ¾Ð³Ð¾ Ð¿ÑÐµÐ´ÑÑÐ¼Ð¾ÑÑÐµÐ½ Ð¿ÑÐµÐ´Ð¿ÑÐ¾ÑÐ¼Ð¾ÑÑ RLS â Ð¿ÑÐ¾ÑÑÐ¾ Ð²ÐºÐ»ÑÑÐ¸ÑÐµ ÐµÐ³Ð¾ Ð² Ð½Ð°ÑÑÑÐ¾Ð¹ÐºÐ°Ñ Ð¿ÑÐ¾ÐµÐºÑÐ° Ð¸ Ð²ÑÐ±ÐµÑÐ¸ÑÐµ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ, Ð¿Ð¾Ð´ ÐºÐ¾ÑÐ¾ÑÑÐ¼ Ñ Ð¾ÑÐ¸ÑÐµ Ð¿ÑÐ¾Ð²ÐµÑÐ¸ÑÑ ÑÐ°Ð±Ð¾ÑÑ Ð¿ÑÐ°Ð²Ð¸Ð».**

![](https://help.fastboard.online/assets/images/unnamed-15--ea88538d19e2d183832f267e83b369de.png)

**Ð­ÑÐ¾ ÑÐ¸Ð»ÑÐ½Ð¾ ÑÐ¾ÐºÑÐ°ÑÐ¸Ñ Ð²ÑÐµÐ¼Ñ Ð¾ÑÐ»Ð°Ð´ÐºÐ¸. Ð ÑÐµÐ»ÑÑ Ð±ÐµÐ·Ð¾Ð¿Ð°ÑÐ½Ð¾ÑÑÐ¸ Ð¿ÑÐµÐ´Ð¿ÑÐ¾ÑÐ¼Ð¾ÑÑ RLS ÑÐ°Ð±Ð¾ÑÐ°ÐµÑ ÑÐ¾Ð»ÑÐºÐ¾ Ð´Ð»Ñ Ð°Ð´Ð¼Ð¸Ð½Ð¸ÑÑÑÐ°ÑÐ¾ÑÐ¾Ð², Ð° ÑÐ°ÐºÐ¶Ðµ ÑÐ°Ð·ÑÐ°Ð±Ð¾ÑÑÐ¸ÐºÐ¾Ð², Ð½Ðµ Ð¾Ð³ÑÐ°Ð½Ð¸ÑÐµÐ½Ð½ÑÑ Ð½Ð°ÑÑÑÐ¾ÐµÐ½Ð½ÑÐ¼Ð¸ Ð¿ÑÐ°Ð²Ð¸Ð»Ð°Ð¼Ð¸.**
