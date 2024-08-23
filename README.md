# rss-shim

rss-shim is a web server to provide RSS feeds for data that do not already have one.

## Installation

Build the Docker image and deploy it where desired:

```bash
docker build -t rss-shim .
```

## Usage

Currently, the server provides a single feed, `feed.rss`, from port 80. I will be changing this in the future.

## Contributing

This project uses various code quality tooling, all of which is automatically installed with the rest of the development requirements.

All checks can be run with `make check`, and some additional automatic changes can be run with `make fix`.

To test GitHub Actions workflows locally, install [`act`](https://github.com/nektos/act) and run it with `act`.

Feel free to improve shims I already have, but you are likely better off contributing to larger, existing projects, such as [RSS-Bridge](https://github.com/RSS-Bridge/rss-bridge). I will not accept shims for services I do not use, so create an issue first if you want to implement one.

## License

[CC0 1.0 Universal](https://choosealicense.com/licenses/cc0-1.0/)

This program exists to make existing data easier to access. In the spirit of that, I am not limiting usage of it whatsoever. However, I would appreciate attribution if anyone uses any part of this repository.

The license applies retroactively to versions of the repository without any license information.
