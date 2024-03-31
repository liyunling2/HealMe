import { RabbitMQConnection } from "./amqp";

export default async function notify(context: { data: BlockedSlotType, status: number }, mqConnection: RabbitMQConnection) {
    console.log("Notifying");
    const { data, status } = context;
  
    if (status !== 201)
      return;
  
    const { doctorID, slotNo, date } = data;
  
    let doctorEmail: string = "";
  
    try {
      // doctorEmail = await fetchDoctorWithParams(new URLSearchParams({ doctorID })).then(data => (data as { email: string }).email);
      doctorEmail = data.email
    }
    catch (error) {
      console.error(error);
      return;
    }
  
    const timeNum =  7 + (slotNo - 1) * 0.5;
    const toTimeStr = (timeNum: number) => `${Math.floor(timeNum)}:${timeNum % 1 == 0 ? "00" : "30"}`;
  
    console.log("sending to ", doctorEmail);
    await mqConnection.connect();
    await mqConnection.channel.basicPublish(
      'direct_exchange',
      'email.notification.request',
      Buffer.from(JSON.stringify({
        from: "healmeesd@gmail.com",
        to: doctorEmail,
        subject: "You have created a blocked slot",
        content: {
            title: "Blocked Slot Created",
            message: `You have blocked out a slot on ${date.slice(0, -13)} from ${toTimeStr(timeNum)} to ${toTimeStr(timeNum + 0.5)}`
        }
      })
      ))
    console.log("published")
  }
  