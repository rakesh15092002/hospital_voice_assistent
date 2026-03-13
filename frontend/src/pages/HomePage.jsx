import Navbar from "../components/common/Navbar";
import VoiceRoom from "../components/voice/VoiceRoom";

const HomePage = () => {
  return (
    <div style={{ minHeight: "100vh", background: "#f0f4ff" }}>
      {/* Top navbar */}
      <Navbar />

      {/* Main voice UI */}
      <VoiceRoom />
    </div>
  );
};

export default HomePage;