import API from "./axios";

export const getMyAppointments = async () => {
  const response = await API.get("/appointments/me");
  return response.data;
};

export const bookAppointment = async (doctor_id, slot_id) => {
  const response = await API.post("/appointments/", { doctor_id, slot_id });
  return response.data;
};

export const cancelAppointment = async (appointment_id) => {
  const response = await API.patch(`/appointments/${appointment_id}/cancel`);
  return response.data;
};

export const getAppointmentById = async (appointment_id) => {
  const response = await API.get(`/appointments/${appointment_id}`);
  return response.data;
};