import { expect, test } from "bun:test";
import { isDoctorIDValid } from "../src/utils";

test("doctorValid", async () => {
  const doctorID = "1234";

  // mock global fetch
  // @ts-ignore
  global.fetch = async (url: string) => {
    return {
      status: 200,
      json: async () => {
        return {
          doctor: {
            id: doctorID,
            name: "Dr. John Doe",
          },
        };
      },
    } as any;
  };

  const response = await isDoctorIDValid(doctorID);
  expect(response).toBe(true);

  // mock global fetch
  // @ts-ignore
  global.fetch = async (url: string) => {
    return {
      status: 404,
      json: async () => {
        return {};
      },
    } as any;
  };

  const response2 = await isDoctorIDValid(doctorID);
  expect(response2).toBe(false);
});