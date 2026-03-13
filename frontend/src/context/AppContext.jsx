import { AuthProvider } from "./AuthContext";
import { AppointmentProvider } from "./AppointmentContext";

// Wrap all providers in one place
// This is used in main.jsx only once
const AppContext = ({ children }) => {
  return (
    <AuthProvider>
      <AppointmentProvider>
        {children}
      </AppointmentProvider>
    </AuthProvider>
  );
};

export default AppContext;