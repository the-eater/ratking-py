# ratking | `rk`

Eater's all purpose package manager

---

The purpose of this package manager is to create a _generic_ package manager, 
that can be easily extended for domain specific tasks,
without having to reinvent a whole new package manager stack

Packages are from here on called `Ra's

Current supported repositories are:

| name | uri | description | 
| --- | --- | --- |
| FlatFileRepository | `flat:<toml file>` | A simple toml file with several rats defined
| MemoryRepository | none | A simple in memory repository
| ComposerRepository | `composer:<composer server>` | Works with [composer](https://getcomposer.org/) package server

# versions and constraints

Versions are always a very complex matter, in ratking's case it gets a bit worse because
we can't just say semver it is. because that would mean we would reject a set of rats.
this is why ratking uses a _very_ lax version of semver, basically anything goes as long as it starts with number.

constrains on the other hand work mostly as how you would expect, whatever you do expect.
 
As an example, writing a constraint for matching v5 to v8 and v10 may be written as the following
 
- `v5 to v8 and v10`
- `(gte 5 and lte 8) or 10`
- `==v5 || >= v5 && <= 8` 

You can find the grammar for the constraints in [version_selector.ebnf](resources/version_selector.ebnf)

# todo

- Create example domain specific package manager
- 