# seat
A seat generator that allows various modifications.

## Manual
This seat generator allows random generation of seats from a set of names with various modifications, including but not limited to random assortment, fixed seat, preferred seating areas, seat mate with or without preference, and rotate options.

All presets for generating a seat pattern is controlled by a `config.json` file. Below is an example of `config.json`. Such a file contains six entries of settings. The tabs `row` and `col` determine the size of the rectangular room. `noSit` stands for the positions that are not available for sitting, such as aisles between seats. `nameList` stands for names to be randomly assigned into seats. `seed` represents the seed for generation; a same seed with the same configuration always produces the same result. `modif` is a list of modifications done to the seat pattern.

```json
{
    "col": 11,
    "modif": [
        {
            "mate": "边麓元",
            "mode": "pref",
            "name": "廖从云"
        },
        {
            "mode": "pref",
            "name": "王昊天",
            "mate": "丁鹏元"
        },
        {
            "mate": "赖思轩",
            "mode": "pref",
            "name": "骆子墨",
            "pref": {
                "mode": "rules",
                "rules": [
                    {
                        "col": {
                            "mode": "all"
                        },
                        "mode": "add",
                        "row": {
                            "mode": "scale",
                            "value": [
                                0.7,
                                1
                            ]
                        }
                    }
                ]
            }
        },
        {
            "mate": "邱晨朔",
            "mode": "pref",
            "name": "范青桐"
        },
        {
            "mode": "pref",
            "name": "张宸瑞",
            "pref": {
                "mode": "rules",
                "rules": [
                    {
                        "col": {
                            "mode": "all"
                        },
                        "mode": "add",
                        "row": {
                            "mode": "scale",
                            "value": [
                                0,
                                0.3
                            ]
                        }
                    }
                ]
            }
        },
        {
            "mode": "pref",
            "name": "张扬",
            "pref": {
                "mode": "rules",
                "rules": [
                    {
                        "col": {
                            "mode": "all"
                        },
                        "mode": "add",
                        "row": {
                            "mode": "scale",
                            "value": [
                                0.7,
                                1
                            ]
                        }
                    }
                ]
            }
        },
        {
            "mode": "rotate",
            "names": [
                "蔡朋骏",
                "迟涵予",
                "白宇轩"
            ]
        },
        {
            "mode": "rotate",
            "names": [
                "詹悦",
                "黄婧涵",
                "林彦含"
            ]
        },
        {
            "mode": "pref",
            "name": "李星宸",
            "pref": {
                "mode": "rules",
                "rules": [
                    {
                        "col": {
                            "mode": "range",
                            "value": [
                                3,
                                11
                            ]
                        },
                        "mode": "add",
                        "row": {
                            "mode": "range",
                            "value": [
                                0,
                                3
                            ]
                        }
                    }
                ]
            }
        },
        {
            "mode": "pref",
            "name": "龚搏扬",
            "pref": {
                "mode": "rules",
                "rules": [
                    {
                        "col": {
                            "mode": "all"
                        },
                        "mode": "add",
                        "row": {
                            "mode": "range",
                            "value": [
                                0,
                                1
                            ]
                        }
                    }
                ]
            }
        },
        {
            "mode": "pref",
            "name": "曾韦翔",
            "pref": {
                "mode": "rules",
                "rules": [
                    {
                        "col": {
                            "mode": "range",
                            "value": [
                                5,
                                11
                            ]
                        },
                        "mode": "add",
                        "row": {
                            "mode": "range",
                            "value": [
                                1,
                                3
                            ]
                        }
                    }
                ]
            }
        },
        {
            "mate": "杜心扬",
            "mode": "pref",
            "name": "章淏博",
            "pref": {
                "mode": "rules",
                "rules": [
                    {
                        "col": {
                            "mode": "all"
                        },
                        "row": {
                            "mode": "scale",
                            "value": [
                                0.99,
                                1
                            ]
                        },
                        "mode": "add"
                    }
                ]
            }
        }
    ],
    "nameList": [
        "龚搏扬",
        "骆子墨",
        "章淏博",
        "边麓元",
        "廖从云",
        "林彦含",
        "李星宸",
        "曾韦翔",
        "蔡朋骏",
        "吴周毅",
        "白宇轩",
        "王昊天",
        "赖思轩",
        "郑俊永",
        "杨熙宇",
        "张宸瑞",
        "詹悦",
        "黄婧涵",
        "陈元畅",
        "程启航",
        "丁鹏元",
        "迟涵予",
        "张扬",
        "龙飞宇",
        "邱晨朔",
        "杜心扬",
        "范青桐",
        "卢逸",
        "陈李石农",
        "石清泓"
    ],
    "noSit": {
        "rules": [
            {
                "col": {
                    "mode": "direct",
                    "value": [
                        0,
                        1
                    ]
                },
                "mode": "add",
                "row": {
                    "mode": "range",
                    "value": [
                        0,
                        1
                    ]
                }
            },
            {
                "col": {
                    "mode": "direct",
                    "value": [
                        2,
                        5,
                        8
                    ]
                },
                "mode": "add",
                "row": {
                    "mode": "range",
                    "value": [
                        0,
                        4,
                        1
                    ]
                }
            }
        ],
        "mode": "rules"
    },
    "row": 4,
    "seed": 20220925
}
```

It's notable that all five entries have their structures; inappropriate writing of the json file will result in error.
* `row`, `col`, and `seed` should be integers. `seed` set to `0` will let the program determine a random seed.
* `nameList` should be a list of strings. Each entry of the list will be a name that appears in the result. A same name appearing twice or more than twice is not supported.
* `noSit` determines the coordinates that cannot be sit. This tag is a coordinate provider, which must contain a `mode`.
* * If `mode` is set to `empty`, then no other configuration is need, and the program will regard it as an empty `noSit` list.
* * If `mode` is `simple`, then add a `value` list where you should put the specific list of `noSit` coordinates within. For example, `"noSit": {"mode": "simple", "value": [[0, 1], [0, 2], [1, 2], [2, 3]]}` will add `(0, 1)`, `(0, 2)`, `(1, 2)`, and `(2, 3)` into the `noSit` list.
* * If `mode` is `rules`, then a list of rules, called `rules`, should be placed under the dict tab. Each rule should be a dict tab that contains three entries: `mode`, `col`, and `row`. `mode` under a rule should be either `add`, `del`, or `invert`. `add` adds the corresponding positions to the `noSit` list, while `del` does the opposite; `invert` inverts all coordinates (which is to exclude all the existing coordinates in the list and include all the remaining ones). `col` and `row` specify which array of coordinates should be added. Each of the two should be a dict tab with `mode` and `value`. `mode` supports `direct`, `range`, `all`, and `scale`. `direct` is followed by an integer or a list of integers; `range` is the same as python's `range()` function; `all` does not need a specific `value`, but will cover all possible coordinates; `scale` is followed by two float numbers between `0.0` and `1.0`, indicating the multiplier on the maximum coordinate. For example, ```"noSit": {"config": {"rules": [{"col": {"mode": "direct", "value": 0}, "mode": "add", "row": {"mode": "range", "value": [0, 2]}}]}}``` will put `(0, 0)` and `(0, 1)` into the list.
* `modif` is a list of modifications that will be done to the random assignment of seats. Different kinds of modification accept different parameters, but all contain a `mode` tag in common. `mode` should be `mate`, `fixed`, `pref`, and `rotate`.
* * `pref` works to assigned a preffered seating area or a mate for a name. If a `mate` is provided, then the name in the mate will appear by either side of the name. The `pref` space is a coordinate provider, which should act the same as `noSit`'s.
* * `rotate` is a special seating option that selects a pair from a list of names according to current week number. Simply provide a `names` list under the modification and add as many names into it.
* * `fixed` fixes a name on a seat. `fixed` tag has a higher priority than all other modifications, so this mode should be preferred when applicable. The coordinate should be given under the `pos` tag as a list of two numbers.

`config.json` should be placed under a folder with custom name under the 'save' folder. The name will be used for naming the generated seat file. The program supports generating `.txt` and `.xlsx` file. To get a `.xlsx` file, a template named `template.xlsx` should also be placed under the folder. `$ ROW` and `$ COL` specify the starting coordinate where the seat pattern will be assigned into the form. `% DAY MONTH YEAR` will let the program print the date of the day the seat is generated. Both modifications are optional.
