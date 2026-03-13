import { createContext, useContext, useState, useCallback } from "react";
import {
  getMyAppointments,
  bookAppointment,
  cancelAppointment,
} from "../api/appointment";

const AppointmentContext = createContext();

export const useAppointment = () => useContext(AppointmentContext);

export const AppointmentProvider = ({ children }) => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Fetch all appointments
  const fetchAppointments = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const data = await getMyAppointments();
      setAppointments(data);
    } catch (err) {
      setError("Failed to load appointments.");
    } finally {
      setLoading(false);
    }
  }, []);

  // Book new appointment
  const book = async (appointmentData) => {
    const data = await bookAppointment(appointmentData);
    await fetchAppointments();
    return data;
  };

  // Cancel appointment
  const cancel = async (id) => {
    await cancelAppointment(id);
    await fetchAppointments();
  };

  return (
    <AppointmentContext.Provider
      value={{ appointments, loading, error, fetchAppointments, book, cancel }}
    >
      {children}
    </AppointmentContext.Provider>
  );
};