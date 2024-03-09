### Structure
#### Directory structure
- The source code for the microservices are stored in the `services` directory
- Simple and complex microservices are stored in `simple` and `complex` directories respectively
    - Each service has its own directory e.g. `simple/schedule`
#### Compose
- The containers are spun up together via the compose.yaml file
- The `.env` file contains important shared environment variables such as the port numbers of each service.
    - These can be used by the `compose.yaml` file and used when setting options for individual containers
    - Example:

    ```yaml
    blocked_slots:
        environment:
            - DB_URI: ${DB_URI}/blocked_slots
        # continued
    ```