import { Hono } from 'hono';
import Query from './common/Query';

const app = new Hono();

app.get("/", (c) => {

    return c.json({})
})

const doctorProfileQuery = new Query(async (doctorID))