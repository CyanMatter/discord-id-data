Users, messages, servers, channels, threads, DMs; Discord provides these objects and more with unique [snowflake IDs](https://discord.com/developers/docs/reference#snowflakes).
The IDs can tell you something about the circumstances of their creation.
This application extracts that information and displays it in a readable manner.

It tells…
- … the time of creation, accurate to a millisecond,
- … the ID of the internal worker that was involved,
- … the ID of the internal process that was involved, and
- … at which place in the queue the process was served during the millisecond of the ID's creation.
