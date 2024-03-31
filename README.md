# HealMe

![alt text|300](image.png)
Accessing healthcare services in Singapore can be challenging due to long waiting times, limited appointment availability, and fragmented information about clinics services and practitioners. As such, HealMe aims to be an aggregator application aiming to bridge the information gap between clinics and patients and allowing personalized bookings with specific doctors. This simplifies patients’ booking process while increasing clinic efficiency and reducing waiting times, effectively solving our problem statement. We came up with 3 scenarios that would closely demonstrate real world situations of a typical user on our application. The scenarios include: 
- Booking an appointment with a specific doctor 
- Rating a doctor after completing an appointment  
- A doctor canceling a scheduled appointment 

## Running the Project

Navigate to the services directory

```bash
cd services
```
Run the following command to start the services

```bash
docker compose up --build
```

In a separate terminal, navigate to the frontend directory

```bash
cd FrontEnd
```

Install dependencies

```bash
npm install
```

Run the following command to start the frontend on localhost:8080

```bash
npm run serve
```

## Accessing admin dashboards and logs
- Logs are stored in the `app_logs` directory of the services folder
- Kong admin can be accessed at `http://localhost:8001`
- Grafana can be accessed at `http://localhost:3000` with the credentials username: `admin` password: `admin`
