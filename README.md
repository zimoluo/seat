# seat
A seat generator that allows various modifications.

## How to use
This seat generator allows random generation of seats from a set of names with various modifications, including but not limited to random assortment, fixed seat, preferred seating areas, seat mate with or without preference, and rotate options.

All presets for generating a seat pattern is controlled by a `config.json` file. Below is an example of `config.json`. Such a file contains six entries of settings. The tabs `row` and `col` determine the size of the rectangular room. `noSit` stands for the positions that are not available for sitting, such as aisles between seats. `nameList` stands for names to be randomly assigned into seats. `seed` represents the seed for generation; a same seed with the same configuration always produces the same result. `modif` is a list of modifications done to the seat pattern.

```json
{
    "noSit": {
        "mode": "empty"
    },
    "row": 4,
    "col": 3,
    "seed": 0,
    "nameList": [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9"
    ],
    "modif": []
}
```

It's notable that all five entries have their structures; inappropriate writing of the json file will result in error.
* `row`, `col`, and `seed` should be integers. `seed` set to `0` will let the program determine a random seed.
* `nameList` should be a list of strings. Each entry of the list will be a name that appears in the result. A same name appearing twice or more than twice is not supported.
* `noSit` is a dict tab that must contain an entry `mode`. `mode` can be `empty`, `simple`, or `rules`.
* * If `mode` is set to `empty`, then no other configuration is need, and the program will regard it as an empty `noSit` list.
* * If `mode` is `simple`, then write a `config` dict tab within `noSit` and add a `value` list where you should put the specific list of `noSit` coordinates within. For example, `"noSit": {"mode": "simple", "config": {"value": [[0, 1], [0, 2], [1, 2], [2, 3]]}}` will add `(0, 1)`, `(0, 2)`, `(1, 2)`, and `(2, 3)` into the `noSit` list.
* * If `mode` is `rules`, then the `config` should work as a generator that generates a set of `noSit` entries. A list of rules, called `rules`, should be placed under the `config` dict tab. Each rule should be a dict tab that contains three entries: `mode`, `col`, and `row`. `mode` under a rule should be either `add` or `del`. `add` adds the corresponding positions to the `noSit` list, while `del` does the opposite. `col` and `row` specify which array of coordinates should be added. Each can either be an integer or a list of length 2 or 3. An integer stands for the sole value of its; a list of length 2 or 3 essentially works as the `range()` function, there the third argument stands for 'step.' Every generated value in `row` will pair with every value in `col` to form a coordinate and will be added to the `noSit` tab. For example, ```"noSit": {"config": {"rules": [{"col": 0, "mode": "add", "row": [0, 2]}]}}``` will put `(0, 0)` and `(0, 1)` into the list.
* `modif` is a list of modifications that will be done to the random assignment of seats. Different kinds of modification accept different parameters, but all contain a `mode` tag in common. `mode` should be `mate`, `fixed`, `pref`, and `rotate`.
* * `mate` assigns a name with a given mate that would be adjacent to each other in the generated pattern. A `name` and a `mate` tag should be specified under the modification, each giving a name that should be present in `nameList`. Additionally, an optional `pref` tag can be used to determine the preffered seating area of the pair. The structure of `pref` is the same as the `pref` tag with `pref` as `mode`.
* * `pref` works to set a preffered seating area for a name. A `pref` should contain a `mode` tag that is either `simple` or `select`. With `simple`, a `col` and a `row` should be provided under the `pref` tag, each containing another `mode` tag, `any`, `range`, or `scale`. The `col` and `row` tag work similar to those in `noSit`'s rules. `any` stands for all rows or columns; `range` is a range of the bound of the area; `scale` should be a list of two non-negative float numbers less than or equal to `1`, which determine the value by down-scaling the total number of rows or columns. With `select`, a list named `choice` should be present, containing a list of `simple` settings with the `simple` mode not explicitly specified placed under. The program will randomly choose one of the preference settings.
* * `rotate` is a special seating option that selects a pair from a list of names according to current week number. Simply provide a `names` list under the modification and add as many names into it.
* * `fixed` fixes a name on a seat. The coordinate should be given under the `pos` tag as a list of two numbers.

`config.json` should be placed under a folder with custom name under the 'save' folder. The name will be used for naming the generated seat file. The program supports generating `.txt` and `.xlsx` file. To get a `.xlsx` file, a template named `template.xlsx` should also be placed under the folder. `$ ROW` and `$ COL` specify the starting coordinate where the seat pattern will be assigned into the form. `% DAY MONTH YEAR` will let the program print the date of the day the seat is generated. Both modifications are optional.