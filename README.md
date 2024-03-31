# HealMe

Accessing healthcare services in Singapore can be challenging due to long waiting times, limited appointment availability, and fragmented information about clinics services and practitioners. As such, HealMe aims to be an aggregator application aiming to bridge the information gap between clinics and patients and allowing personalized bookings with specific doctors. This simplifies patients’ booking process while increasing clinic efficiency and reducing waiting times, effectively solving our problem statement. We came up with 3 scenarios that would closely demonstrate real world situations of a typical user on our application. The scenarios include: 
- Booking an appointment with a specific doctor 
- Rating a doctor after completing an appointment  
- A doctor canceling a scheduled appointment 

## Folder structure (important folders)
```
├── Frontend
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
