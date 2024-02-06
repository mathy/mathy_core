## [0.9.4](https://github.com/mathy/mathy_core/compare/v0.9.3...v0.9.4) (2024-02-06)


### Features

* **rules:** add MultiplicativeInverse rule ([#19](https://github.com/mathy/mathy_core/issues/19)) ([40a2d88](https://github.com/mathy/mathy_core/commit/40a2d887b11908a59516d9372f38070356a18d32))

## [0.9.3](https://github.com/mathy/mathy_core/compare/v0.9.2...v0.9.3) (2024-01-15)


### Bug Fixes

* **rule:** RestateSubtraction failed to produce simple forms ([#18](https://github.com/mathy/mathy_core/issues/18)) ([71467c2](https://github.com/mathy/mathy_core/commit/71467c29c5555aabaeecfce4662592e91166bcc2))

## [0.9.2](https://github.com/mathy/mathy_core/compare/v0.9.1...v0.9.2) (2023-12-15)

### Bug Fixes

- **typing:** proper generic type for BinaryTreeNode ([6ec236e](https://github.com/mathy/mathy_core/commit/6ec236e0b70e47b9f8e03a3f0ac54d872c3c0fb4))

## [0.9.1](https://github.com/mathy/mathy_core/compare/v0.9.0...v0.9.1) (2023-11-29)

### Features

- **ci:** add python build matrix ([#11](https://github.com/mathy/mathy_core/issues/11)) ([3625238](https://github.com/mathy/mathy_core/commit/3625238a7922aba686c66158a839fbe6013b84a4))

# [0.9.0](https://github.com/mathy/mathy_core/compare/v0.8.6...v0.9.0) (2023-11-29)

### Features

- **ci:** add cron job for CI build ([0a4e833](https://github.com/mathy/mathy_core/commit/0a4e83350bed9c2e654981ea7cd56b55d326cd1c))
- **package:** remove pydantic dependency ([66c983f](https://github.com/mathy/mathy_core/commit/66c983f252d22a2d0a9287b2de1f2ad70bcc85ad))

**BREAKING CHANGES**

- **package:** MathyTermTemplate is no longer a pydantic model. It's now a dataclass

## [0.8.6](https://github.com/mathy/mathy_core/compare/v0.8.5...v0.8.6) (2022-09-24)

### Features

- **pyright:** update lib to be type complete ([0df1e22](https://github.com/mathy/mathy_core/commit/0df1e220d0235fd29bbd877ffe34fb79a8e1e448))

## [0.8.5](https://github.com/mathy/mathy_core/compare/v0.8.4...v0.8.5) (2022-09-24)

### Bug Fixes

- updating typings to satisfy latest mypy/pyright ([619ab12](https://github.com/mathy/mathy_core/commit/619ab12677372d0d6cc50196309adf026bc64e9d))

## [0.8.4](https://github.com/mathy/mathy_core/compare/v0.8.3...v0.8.4) (2021-04-06)

### Bug Fixes

- **pypi:** include json expectations in package ([2888a84](https://github.com/mathy/mathy_core/commit/2888a844a5e8bba938115a4ea2d2068ab5b9654d))

## [0.8.3](https://github.com/mathy/mathy_core/compare/v0.8.2...v0.8.3) (2021-03-25)

### Features

- **parser:** add support for FactorialExpression nodes ([f08d0e1](https://github.com/mathy/mathy_core/commit/f08d0e191c77f49c11a0fa78b43d3449f94b5bd0))
- **rules:** add BalancedMoveRule for moving terms to the other side of equations ([c16f98d](https://github.com/mathy/mathy_core/commit/c16f98d4ae6d33e4e05f38980038e951a7e0c047))
- **testing:** check equation node transforms during testing ([771a40a](https://github.com/mathy/mathy_core/commit/771a40a83c54e637c01adcfd63ed314f417091db))

## [0.8.2](https://github.com/mathy/mathy_core/compare/v0.8.1...v0.8.2) (2020-11-03)

### Features

- **rules:** add RestateSubtractionRule ([#5](https://github.com/mathy/mathy_core/issues/5)) ([5587d23](https://github.com/mathy/mathy_core/commit/5587d2308a8fe9e48e7680e122196d571349aa16))

## [0.8.1](https://github.com/mathy/mathy_core/compare/v0.8.0...v0.8.1) (2020-09-13)

### Bug Fixes

- **layout:** assert after setting x ([d8741ef](https://github.com/mathy/mathy_core/commit/d8741ef740f016c2430079164073cb376fecafd3))

# [0.8.0](https://github.com/mathy/mathy_core/compare/v0.7.21...v0.8.0) (2020-09-13)

### Code Refactoring

- **datasets:** drop datasets submodule from library ([dd0c76a](https://github.com/mathy/mathy_core/commit/dd0c76ab31280479af5374b127c0d71217a6a5bb))

**BREAKING CHANGES**

- **datasets:** the mathy_core.datasets submodule has been removed

## [0.7.21](https://github.com/mathy/mathy_core/compare/v0.7.20...v0.7.21) (2020-09-06)

### Bug Fixes

- **MathExpression:** add optional r_index int ([6ded18e](https://github.com/mathy/mathy_core/commit/6ded18e02bae8fa09a656da779dd132440001d92))

## [0.7.20](https://github.com/mathy/mathy_core/compare/v0.7.19...v0.7.20) (2020-08-23)

### Bug Fixes

- **requirements:** drop unused package dependencies ([542515a](https://github.com/mathy/mathy_core/commit/542515a5089c2a3179a3c8b07aae0a6b98e7bfb9))

### Features

- **problems:** generate associative grouping augmentations with probability ([da7ddd0](https://github.com/mathy/mathy_core/commit/da7ddd0a44c92b5c4e702a6f4f6fe6bf6135b8f1))

## [0.7.19](https://github.com/mathy/mathy_core/compare/v0.7.18...v0.7.19) (2020-07-24)

### Bug Fixes

- **testing:** move test json files into package dir ([fe7c3ca](https://github.com/mathy/mathy_core/commit/fe7c3ca2505bb012daa4b9bef64dd8ae34d3c6ba))

## [0.7.18](https://github.com/mathy/mathy_core/compare/v0.7.17...v0.7.18) (2020-07-20)

### Features

- **package:** lol, do export everything ([9e64199](https://github.com/mathy/mathy_core/commit/9e64199290aa2e871faa775cf2ff004673d1da3f))

## [0.7.17](https://github.com/mathy/mathy_core/compare/v0.7.16...v0.7.17) (2020-07-20)

### Bug Fixes

- **package:** don't export names in the package root ([f8e02e0](https://github.com/mathy/mathy_core/commit/f8e02e0b13f26b47a9ca9d7a4de5eae64de152fe))

## [0.7.16](https://github.com/mathy/mathy_core/compare/v0.7.15...v0.7.16) (2020-07-19)

### Bug Fixes

- **ci:** run semantic-release before pypi deploy ([4919971](https://github.com/mathy/mathy_core/commit/4919971f4efcd19b42745696593d610a69bfd286))

## [0.7.15](https://github.com/mathy/mathy_core/compare/v0.7.14...v0.7.15) (2020-07-19)

### Performance Improvements

- drop the freed disk space build action ([4d939be](https://github.com/mathy/mathy_core/commit/4d939be5019ca2b4dfb967f92fc271e19b02b715))
