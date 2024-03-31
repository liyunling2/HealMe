# HealMe

Accessing healthcare services in Singapore can be challenging due to long waiting times, limited appointment availability, and fragmented information about clinics services and practitioners. As such, HealMe aims to be an aggregator application aiming to bridge the information gap between clinics and patients and allowing personalized bookings with specific doctors. This simplifies patients’ booking process while increasing clinic efficiency and reducing waiting times, effectively solving our problem statement. We came up with 3 scenarios that would closely demonstrate real world situations of a typical user on our application. The scenarios include: 
- Booking an appointment with a specific doctor 
- Rating a doctor after completing an appointment  
- A doctor canceling a scheduled appointment 

## Folder structure (important folders)
```
├── FrontEnd
    └── healme (frontend client code)
└── services
    ├── complex (complex microservices source code)
    ├── simple (simple microservices source code)
    ├── amqp (amqp configuration)
    ├── app_logs (log files)
    ├── db (mysql image configuration)
    ├── kong (kong configuration)
    └── seed.sql (dummy data seed file)
```


## Running the Project

Navigate to the services directory

```bash
cd services
```
Run the following command to start the services

```bash
docker compose up --build
```
Seed data in the database

```bash
docker exec -i services-db-1  mysql -u root --password=root < seed.sql
``` 

In a separate terminal, navigate to the frontend directory

```bash
cd FrontEnd/healme
```

Install dependencies

```bash
npm install
```

Run the following command to start the frontend on `localhost:8080`

```bash
npm run serve
```

## Accessing admin dashboards and logs
- Logs are stored in the `app_logs` directory of the services folder
- Kong admin can be accessed at `http://localhost:8001`
- Grafana can be accessed at `http://localhost:3000` with the credentials username: `admin` password: `admin`
- RabbitMQ can be accessed at `http://localhost:15672` with the credientials username: `guest` password: `guest`


## Ensure that the following ports are inactive before you run the deployment to avoid any port conflicts
- 50000/tcp for services-create_blocked_slot
- 9999/tcp for services-get_doctor_schedule
- 5006/tcp for services-log
- 50003/tcp for services-get_doctor_profile_with_rating
- 5007/tcp for services-manage_booking
- 5002/tcp for services-clinic
- 5003/tcp for services-profile
- 5001/tcp for services-blocked_slots
- 5004/tcp for services-rating
- 5005/tcp for services-booking
- 3000/tcp for grafana/grafana-oss:10.2.3 (Common for web interfaces, including Grafana)
- 5672/tcp and 15672/tcp for rabbitmq (Commonly used by RabbitMQ and other messaging systems)
- 9090/tcp for prom/prometheus:v2.49.1 (Common for Prometheus server)
- 8000-8004/tcp and 8443-8447/tcp for kong (API Gateway ports, may conflict with other web services)
- 5008/tcp for services-notification
