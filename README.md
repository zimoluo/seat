# seat
A seat generator that allows various modifications.

## How to use
This seat generator allows random generation of seats from a set of names with various modifications, including but not limited to random assortment, fixed seat, preference set, seat mate with or without preference, and special seating options.

Options on the seat generator are achieved by `.json` configuration files. There are three config files: `seat_initialization.json` that controls the size of the classroom, the given name list, and a 'forbidden' seats list, `seat_modification.json` that manipulates the fixed seat, seating preference, and seat mate functions, and `special_seating.json` that regulates special seating. Special seating is a special function that regulates a set of names into a certain pair of two according to the current week number.

```json
{
    "forbidden": [
        [
            0,
            0
        ],
        [
            0,
            2
        ],
        [
            0,
            5
        ],
        [
            0,
            8
        ],
        [
            1,
            2
        ],
        [
            1,
            5
        ],
        [
            1,
            8
        ],
        [
            2,
            2
        ],
        [
            2,
            5
        ],
        [
            2,
            8
        ],
        [
            3,
            2
        ],
        [
            3,
            8
        ]
    ],
    "row": 4,
    "col": 11,
    "name_list": [
        "龚搏扬", "骆子墨", "章淏博", "边麓元", "廖从云", "袁伟伦",
        "林彦含", "李星宸", "曾韦翔", "蔡朋骏", "吴周毅", "白宇轩",
        "王昊天", "赖思轩", "郑俊永", "金建烨", "杨熙宇", "张宸瑞",
        "詹悦", "黄婧涵", "陈元畅", "程启航", "丁鹏元", "迟涵予",
        "张扬", "龙飞宇", "邱晨朔", "杜心扬", "范青桐", "卢逸",
        "陈李石农", "石清泓"
    ]
}
```

The configuration above is the `seat_initialization.json` file used for C5's seating. The `forbidden` key controls the forbidden list of the seat; `row` key controls the maximum row number; `col` key determines the maximum column number; and `name_list` is the provided list of names. Note that name list cannot exceed `row * col - len(forbidden)`.

```json
{
    "fixed": [
        
    ],
    "mate": [
        {
            "name_1": "廖从云",
            "name_2": "边麓元",
            "pref": "FRONT CLOSE"
        },
        {
            "name_1": "袁伟伦",
            "name_2": "章淏博"
        },
        {
            "name_1": "骆子墨",
            "name_2": "赖思轩",
            "pref": "BACK CLOSE"
        }
    ],
    "pref": [
        {
            "name": "张宸瑞",
            "pref": "FRONT MIDDLE_COL CLOSE"
        },
        {
            "name": "郑俊永",
            "pref": "MIDDLE_COL VERY_CLOSE"
        },
        {
            "name": "陈李石农",
            "pref": "FRONT CLOSE"
        },
        {
            "name": "李星宸",
            "pref": {
                "row_lower": 0,
                "row_upper": 3,
                "col_lower": 3,
                "col_upper": 11
            }
        },
        {
            "name": "龚搏扬",
            "pref": "FRONT MIDDLE_COL VERY_CLOSE"
        },
        {
            "name": "张扬",
            "pref": "BACK VERY_CLOSE"
        },
        {
            "name": "曾韦翔",
            "pref": [
                [
                    1,
                    3
                ],
                [
                    5,
                    11
                ]
            ]
        }
    ],
    "override": [
        {
            "name": "易诗兰",
            "row": 0,
            "col": 0
        }
    ]
}
```

The configuration code above is `seat_modification` file. `fixed` controls the given name with a fixed position; `mate` binds two names into a pair of seat mates; `pref` allows a single person to choose seating preference; `override` is a special utility that allows a certain text to appear on a fixed position without modifying the original seat pattern.

```json
[
    {
        "is_shuffled": true,
        "name_list": [
            "林彦含",
            "黄婧涵",
            "詹悦"
        ]
    },
    {
        "is_shuffled": true,
        "name_list": [
            "白宇轩",
            "蔡朋骏",
            "迟涵予"
        ]
    }
]
```

The `special_seating` config allows a set of names to be arranged in a pair of two with members selected from the set according to week numbers. If `is_shuffled` is set to `false` or is left undefined, the program will shuffle the name list upon the first time it reads the name set, before setting the parameter to `true`.

That's it! All you have to do is to set up your own preference in three config files. Then, click the `main.py` file to generate a seat pattern.

This generator also has an experimental function, which is to generate an excel version of the seat pattern. Currently, it relies on a fixed template, which is designed only for C5.
