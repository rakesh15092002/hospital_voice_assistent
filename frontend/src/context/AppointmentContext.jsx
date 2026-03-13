import { createContext, useContext, useState, useCallback } from "react";
import {
  getMyAppointments,
  bookAppointment,
  cancelAppointment,
} from "../api/appointment";

// Create context
const AppointmentContext = createContext();

export const AppointmentProvider = ({ children }) => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all appointments of logged in user
  const fetchAppointments = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getMyAppointments();
      setAppointments(data);
    } catch (err) {
      setError("Failed to fetch appointments");
    } finally {
      setLoading(false);
    }
  }, []);

  // Book a new appointment
  const book = async (doctor_id, slot_id) => {
    try {
      setError(null);
      const data = await bookAppointment(doctor_id, slot_id);
      await fetchAppointments();
      return data;
    } catch (err) {
      setError("Failed to book appointment");
      throw err;
    }
  };

  // Cancel an existing appointment
  const cancel = async (appointment_id) => {
    try {
      setError(null);
      await cancelAppointment(appointment_id);
      await fetchAppointments();
    } catch (err) {
      setError("Failed to cancel appointment");
      throw err;
    }
  };

  return (
    <AppointmentContext.Provider
      value={{ appointments, loading, error, fetchAppointments, book, cancel }}
    >
      {children}
    </AppointmentContext.Provider>
  );
};

// Custom hook to use AppointmentContext anywhere
export const useAppointment = () => useContext(AppointmentContext);