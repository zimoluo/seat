## 2022.4.27

* Added a function to prevent the program from undergoing dead loop. Now it raises an error whenever it detects a potential dead loop.
* * When a dead loop is encountered, the program automatically restarts.

* Added support for forbidden list generator.
* * The `forbidden` key in `seat_initialization.json` now only supports a compound tag.
* * The compound tag accepts two keys: `mode` and `config`.
* * * `mode` can be either `given` or `generator`.
* * * * `given` functions the same as the old `forbidden` input, with `config` being exactly the same.
* * * * `generator` is organized by `rules`. Each `rule` can be set a `mode` and a `content`.
* * * * The `mode` in a `rule` can be `add`, `iter`, or `remove`.
* * * * * `add` allows single or multiple positions to be directly added to the forbidden list. Note that the list automatically cancels repeated positions.
* * * * * `iter` allows a iteration generator with `row` and `col`. Both `row` and `col` accept a `mode` that can be either `range` or `given`. With `range` mode, the `content` accepts `lower_bound` and `upper_bound`; with `given` mode, the `content` accepts a list of numbers.
* * * * * `remove` accepts a list of positions as `content`. All positions mentioned in the `remove` list will be removed from the current forbidden list.
* * * * Rules are executed by the order they are written.

* Fixed various bugs.

* Added many annotations for eligibility.
