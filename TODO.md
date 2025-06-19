# TODO

- [ ] Implement more robust dashboard frontend using React.
- [ ] Integrate color palette from `config/color_palette.json` into dashboard styling.
- [ ] Write integration tests for message bus and knowledge store.
- [ ] Enhance sample agent and add new agents, such as one that retrieves local weather.
- [ ] Improve error handling and logging; store logs under `~/tmp` or another ignored path.
- [ ] Provide script or CLI options to launch multiple agents simultaneously.

## Event Bus Enhancements

- [ ] Add pagination to the `/messages` endpoint, returning the most recent events capped at 50.
- [ ] Implement optional message TTL to prevent unbounded growth of stored events.
- [ ] Provide an optional queue implementation for polling messages with removal semantics.
- [ ] Support a production-ready bus/queue backend (e.g., Redis or NATS) in place of the in-memory bus.
- [ ] Refactor agent runner and dashboard to inject the chosen bus or queue implementation.
