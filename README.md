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
