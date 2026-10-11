# simple-exe-dev

A simple way to use [exe.dev](https://exe.dev/docs/what-is-exe) by leveraging
unix building blocks.

## Building blocks

Rather than one monolithic server, apps should be built as many separate but
complimentary modular parts.

For example, if an app requires scheduled tasks in the background, they should
be written as simple python scripts and called via systemd, instead of being
a direct part of the server.

Operation type | Use
-------------- | ---
Scheduled tasks | systemd

## Integrations

[exe.dev integrations](https://exe.dev/docs/integrations.md) should be built as
self-contained as possible so they can be used from a script or from the web
server.

They live in the `exedev` package, one module per integration, using only the
standard library:

```python
from exedev import notify, reflection

notify.send("Done", f"Task finished on {reflection.get_info().name}")
```

## CSS

Styles use [Tailwind CSS](https://tailwindcss.com). The source is
`src/simple_exe_dev/styles/input.css`; the built file is not committed.

Icons are [Lucide](https://lucide.dev/icons/), via the
[Iconify Tailwind plugin](https://iconify.design/docs/usage/css/tailwind/tailwind4/):

```html
<span class="icon-[lucide--bell]"></span>
```

## Running

Requires [uv](https://docs.astral.sh/uv/), [npm](https://www.npmjs.com/) and
[just](https://just.systems/).

```sh
just run
```

This installs dependencies, then serves the app in dev mode.
